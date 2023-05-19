from time import sleep

import serial

from psychoscripts import defaults
from psychoscripts.utils.opto_arduino import laser_pulses

# configure serial port
opto_serial = serial.Serial(defaults.SERIAL_PORT_OPTO, defaults.BOUD_RATE)
sleep(defaults.SERIAL_CONN_PAUSE_S)  # wait for serial connection to be established

# move_piezo(servo_serial, 100, 2)

while True:
    a = input()

    laser_pulses(opto_serial, 5, 100, 5000)

    if a == "q":
        break


# close the serial port:
opto_serial.close()
