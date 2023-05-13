from time import sleep

import serial

from psychoscripts import defaults
from psychoscripts.utils.servo_arduino import move_piezo

# configure serial port
servo_serial = serial.Serial(defaults.SERIAL_PORT_SERVO, defaults.BOUD_RATE)
sleep(defaults.SERIAL_CONN_PAUSE_S)  #  wait for serial connection to be established

# move_piezo(servo_serial, 100, 2)

move_piezo(servo_serial, 175, 2, 2)

# close the serial port:
servo_serial.close()
