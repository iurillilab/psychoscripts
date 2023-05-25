from dataclasses import dataclass
from time import sleep
from psychopy import core, visual, logging

import numpy as np
import serial

from psychoscripts import defaults
from psychoscripts.utils.logging import PsychopyLogger, CornerLogger
from psychoscripts.utils.opto_arduino import logged_laser_pulses
from psychoscripts.utils.servo_arduino import logged_move_piezo

from psychoscripts.utils.visual_screen import get_default_psychopy_win

#@dataclass
#class VisualStimulationParams:
    #ci

@dataclass
class LaserStimulationParams:
    pulse_duration_ms: int = 10  # Duration of the laser pulse
    frequency: int = 20  # Frequency of the laser pulses


@dataclass
class ExpParams:
    servo_contact_position: int = 165  # loom position to contact whiskers
    servo_distant_position: int = 130  # loom position to avoid contact with  whiskers
    proximity_duration_ms: int = 20000  # Time of position hold by the 3D stimulus
    pre_stimulus_laser_ms: int = 500  # Time laser is on before stimulus onset
    fraction_laser_on: float = 0.5  # Fraction of stimuli during which the laser is on
    n_looms: int = 5  # Number of looming stimuli for each final position
    between_looms_pause_s: int = 40  # Pause between looming stimuli

window = get_default_psychopy_win()

logger = PsychopyLogger()
corner_logger = CornerLogger(window, logger)
# configure serial port
servo_serial = serial.Serial(defaults.SERIAL_PORT_SERVO, defaults.BOUD_RATE)
# sleep(defaults.SERIAL_CONN_PAUSE_S)

opto_serial = serial.Serial(defaults.SERIAL_PORT_OPTO, defaults.BOUD_RATE)
sleep(defaults.SERIAL_CONN_PAUSE_S)  #  wait for serial connection to be established

circle = visual.Circle(window, color=(-1, -1, -1))
# move_piezo(servo_serial, 100, 2)


servo_trials = []
for i in range(ExpParams.n_looms):
    for laser in [True, False]:
        for trial_type in ["visual", "servo"]:
            for position in (
                ExpParams.servo_distant_position,
                ExpParams.servo_contact_position,
            ):
                servo_trials.append(
                    dict(trial_type=trial_type, laser=laser, position=position)
                )

print(len(servo_trials))

np.random.shuffle(servo_trials)


final_angle = 100
motion_speed_deg_s = defaults.MOTION_SPEED_DEG_S
diameter = defaults.SERVO_BALL_SIZE_CM

y_pos = defaults.SERVO_Y_POS_ANGLE_DEG
r = defaults.SERVO_RADIUS_CM
pv = defaults.HEAD_SERVO_CENTER_CM
qpv_deg = defaults.SERVO_CENTER_ANGLE_DEG


def _get_projection_angle_and_size(angle_position):
    projection_angle = qpv_deg - (
        np.arctan(r * np.sin(angle_position) / (pv + r * np.cos(angle_position)))) * 180 / np.pi

    # Get angular size from diameter and distance:
    distance = np.sqrt((pv ** 2 + r ** 2 + 2 * pv * r * np.cos(angle_position)))
    angular_size = np.arctan(diameter / (2 * distance)) * 2 * 180 / np.pi

    return projection_angle, angular_size


trial_clock = core.Clock()
start_t = trial_clock.getTime()

def _update_monitor():
    circle.draw()
    corner_logger.patch.draw()
    window.flip()

trial_clock = core.Clock()
logger.log_string("Started servo_looming script")
for trial in servo_trials:
    print(trial)
    logger.log_string("Trial: " + str(trial))

    if trial["laser"]:
        # Total time the laser is on, including pre-moving time and time to travel and travel back:
        laser_on_time_total = (
                ExpParams.pre_stimulus_laser_ms
                + ExpParams.proximity_duration_ms
                + defaults.SERVO_DEFAULT_MS_PER_DEG * trial["position"] * 2
        )

        logged_laser_pulses(
            logger,
            opto_serial,
            LaserStimulationParams.frequency,
            LaserStimulationParams.pulse_duration_ms,
            laser_on_time_total,
        )
        # Wait for the pre-moving time:
        sleep(ExpParams.pre_stimulus_laser_ms / 1000)

    if trial["trial_type"] == "servo":
        print("moving to position", trial["position"])
        logged_move_piezo(
            logger,
            servo_serial,
            trial["position"],
            defaults.SERVO_DEFAULT_MS_PER_DEG,
            ExpParams.proximity_duration_ms,
        )
        sleep(ExpParams.proximity_duration_ms / 1000)

    elif trial["trial_type"] == "visual":
        final_angle = trial["position"]
        angular_distance = final_angle
        motion_duration_s = angular_distance / motion_speed_deg_s

        trial_clock.reset()

        corner_logger.toggle_state()
        while trial_clock.getTime() < motion_duration_s:
            angle_position = (angular_distance * trial_clock.getTime() / motion_duration_s) / 180 * np.pi
            projection_angle, angular_size = _get_projection_angle_and_size(angle_position)
            logging.log(level=logging.EXP, msg=f"pos={projection_angle}, trial={angular_size}")
            circle.size = (angular_size, angular_size)
            circle.pos = (projection_angle, y_pos)

            _update_monitor()
        corner_logger.toggle_state()
        _update_monitor()
        sleep(ExpParams.proximity_duration_ms / 1000)
        trial_clock.reset()

        corner_logger.toggle_state()
        while trial_clock.getTime() < motion_duration_s:
            angle_position = (trial["position"] - angular_distance * trial_clock.getTime() / motion_duration_s) / 180 * np.pi
            projection_angle, angular_size = _get_projection_angle_and_size(angle_position)

            circle.size = (angular_size, angular_size)
            circle.pos = (projection_angle, y_pos)

            _update_monitor()
        corner_logger.toggle_state()
        _update_monitor()

    sleep(ExpParams.between_looms_pause_s)

# move_piezo(servo_serial, ExpParams.servo_distant_position, ExpParams.servo_looming_speed_ms, 1000)

# close the serial ports:
servo_serial.close()
opto_serial.close()
