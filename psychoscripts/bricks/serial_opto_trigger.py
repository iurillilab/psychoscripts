from time import sleep

import serial

from psychoscripts import defaults
from psychoscripts.utils.opto_arduino import _laser_pulses

# configure serial port
opto_serial = serial.Serial(defaults.SERIAL_PORT_OPTO, defaults.BOUD_RATE)
sleep(defaults.SERIAL_CONN_PAUSE_S)  # wait for serial connection to be established

# move_piezo(servo_serial, 100, 2)

_laser_pulses(opto_serial, 2, 4, 5000)

# close the serial port:
opto_serial.close()
