from dataclasses import dataclass
from time import sleep

import numpy as np
import serial

from psychoscripts import defaults
from psychoscripts.utils.logging import PsychopyLogger
from psychoscripts.utils.opto_arduino import logged_laser_pulses
from psychoscripts.utils.servo_arduino import logged_move_piezo

logger = PsychopyLogger()
# configure serial port
servo_serial = serial.Serial(defaults.SERIAL_PORT_SERVO, defaults.BOUD_RATE)
# sleep(defaults.SERIAL_CONN_PAUSE_S)

opto_serial = serial.Serial(defaults.SERIAL_PORT_OPTO, defaults.BOUD_RATE)
sleep(defaults.SERIAL_CONN_PAUSE_S)  #  wait for serial connection to be established

# move_piezo(servo_serial, 100, 2)


@dataclass
class LaserStimulationParams:
    pulse_duration_ms: int = 10  # Duration of the laser pulse
    frequency: int = 20  # Frequency of the laser pulses


@dataclass
class ExpParams:
    servo_contact_position: int = 170  # loom position to contact whiskers
    servo_distant_position: int = 100  # loom position to avoid contact with  whiskers
    proximity_duration_ms: int = 30000  # Time of position hold by the 3D stimulus
    pre_stimulus_laser_ms: int = 500  # Time laser is on before stimulus onset
    fraction_laser_on: float = 0.5  # Fraction of stimuli during which the laser is on
    n_looms: int = 2  # Number of looming stimuli for each final position
    between_looms_pause_s: int = 60  # Pause between looming stimuli


servo_trials = []
for i in range(ExpParams.n_looms):
    for laser in [True]:
        for position in (
            ExpParams.servo_distant_position,
            ExpParams.servo_contact_position,
        ):
            servo_trials.append(
                dict(trial_type="servo", laser=laser, position=position)
            )

np.random.shuffle(servo_trials)


logger.log_string("Started servo_looming script")
for trial in servo_trials:
    print(trial)
    logger.log_string("Trial: " + str(trial))
    if trial["trial_type"] == "servo":
        if trial["laser"]:
            # Total time the laser is on, including pre-moving time and time to travel and travel back:
            laser_on_time_total = (
                ExpParams.pre_stimulus_laser_ms
                + ExpParams.proximity_duration_ms
                + ExpParams.servo_looming_speed_ms * trial["position"] * 2
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

        print("moving to position", trial["position"])
        logged_move_piezo(
            logger,
            servo_serial,
            trial["position"],
            defaults.SERVO_DEFAULT_MS_PER_DEG,
            ExpParams.proximity_duration_ms,
        )
        sleep(ExpParams.proximity_duration_ms / 1000)

    sleep(ExpParams.between_looms_pause_s)

# move_piezo(servo_serial, ExpParams.servo_distant_position, ExpParams.servo_looming_speed_ms, 1000)

# close the serial ports:
servo_serial.close()
opto_serial.close()
