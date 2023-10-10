import time

from psychopy import core, visual, logging


from psychoscripts import defaults
import serial

from dataclasses import dataclass
from psychoscripts.utils.visual_screen import get_default_psychopy_win
from psychoscripts.utils.opto_arduino import logged_laser_pulses
from psychoscripts.utils.logging import PsychopyLogger, CornerLogger


@dataclass
class LaserStimulationParams:
    pulse_duration_ms: int = 10  # Duration of the laser pulse
    frequency: int = 20  # Frequency of the laser pulses

@dataclass
class ExpParams:
    warper_correction: str = "spherical"
    ball_distance: float = 25.0
    n_reps: int = 10
    n_back_and_forth: int = 10
    motion_duration_s: float = 1
    motion_amplitude: float = 30
    units: str = "deg"
    dot_size: tuple = (8, 4)
    dot_drift_coef: float = 0.1
    center_x: float = -30
    inter_rep_pause = 30
    pre_stimulus_laser_ms: int = 2000  # Time laser is on before stimulus onset


params = ExpParams

# Create a suitable psychopy window with some params:
window = get_default_psychopy_win()

logger = PsychopyLogger()
corner_logger = CornerLogger(window, logger)

# Draw the stimuli and update the window
circle = visual.Circle(window, size=params.dot_size, color=(-1, -1, -1))

opto_serial = serial.Serial(defaults.SERIAL_PORT_OPTO, defaults.BOUD_RATE)
time.sleep(defaults.SERIAL_CONN_PAUSE_S)  # wait for serial connection to be established


trial_clock = core.Clock()

def _update_monitor():
    circle.draw()
    corner_logger.patch.draw()
    window.flip()


logging.log(level=logging.EXP, msg=f"Begin experiment. Params: {params}. Laser params: {LaserStimulationParams}")
vel = params.motion_amplitude / params.motion_duration_s
for n_rep in range(params.n_reps):

    logging.log(level=logging.EXP, msg=f"laser={n_rep % 2 == 0}")

    pos = params.center_x
    sign = 1

    prev_incr = 0
    circle.opacity = 1

    time.sleep(params.inter_rep_pause / 2 - ExpParams.pre_stimulus_laser_ms / 1000)

    if n_rep % 2 == 0:
        # Total time the laser is on, including pre-moving time and time to travel and travel back:
        laser_on_time_total = (
                ExpParams.pre_stimulus_laser_ms
                + (params.motion_duration_s * params.n_back_and_forth) * 1000
        )

        logged_laser_pulses(
            logger,
            opto_serial,
            LaserStimulationParams.frequency,
            LaserStimulationParams.pulse_duration_ms,
            laser_on_time_total,
        )

    # Wait for the pre-moving time:
    time.sleep(ExpParams.pre_stimulus_laser_ms / 1000)
    trial_clock.reset()
    prev_t = trial_clock.getTime()
    corner_logger.toggle_state()
    _update_monitor()
    while trial_clock.getTime() < (params.motion_duration_s * params.n_back_and_forth):
        mod = trial_clock.getTime() % params.motion_duration_s
        if mod < prev_incr:
            sign = -sign

        prev_incr = mod

        dt = trial_clock.getTime() - prev_t
        prev_t = trial_clock.getTime()
        pos = pos + sign * vel * dt
        circle.pos = (pos, 0)
        circle.draw()
        window.flip()
        _update_monitor()
    corner_logger.toggle_state()

    circle.opacity = 0
    _update_monitor()
    time.sleep(params.inter_rep_pause / 2)
