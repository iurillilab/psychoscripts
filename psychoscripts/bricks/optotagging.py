from time import sleep

import serial

from psychoscripts import defaults
from psychoscripts.utils.logging import PsychopyLogger
from psychoscripts.utils.opto_arduino import logged_laser_pulses

logger = PsychopyLogger()
logger.log_string("Started optotagging script")

# configure serial port
opto_serial = serial.Serial(defaults.SERIAL_PORT_OPTO, defaults.BOUD_RATE)
sleep(defaults.SERIAL_CONN_PAUSE_S)  # wait for serial connection to be established

# move_piezo(servo_serial, 100, 2)

logged_laser_pulses(logger, opto_serial, 2, 4, 3000)
logger.log_string("Opto pulses sent")

# close the serial port:
opto_serial.close()
