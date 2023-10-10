from time import sleep

import serial

from psychoscripts import defaults
from psychoscripts.utils.servo_arduino import _move_piezo

# configure serial port
servo_serial = serial.Serial(defaults.SERIAL_PORT_SERVO, defaults.BOUD_RATE)
sleep(defaults.SERIAL_CONN_PAUSE_S)  #  wait for serial connection to be established

# move_piezo(servo_serial, 100, 2)

_move_piezo(servo_serial, 163, 2, 500)

# close the serial port:
servo_serial.close()
