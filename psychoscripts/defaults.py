# Read a config file from the user home directory and use it to set the default values, if available
import os
import warnings
from pathlib import Path

# Data logging:
LOG_FOLDER = Path(r"E:\Luigi")
if not LOG_FOLDER.exists():
    raise ValueError("LOG_FOLDER points to an invalid directory|")
DEFAULT_TIMESTAMPING = "%Y.%m.%d-%H.%M.%S"
try:
    MOUSE_ID = os.environ["MOUSE_ID"]
except KeyError:
    warnings.warn("No mouse ID set in the environment!", RuntimeWarning)
    MOUSE_ID = "M1"  # "no_mouse_id"

# Corner logging:
HEADER_PULSES_N = 10
CORNER_COLORS = {False: (-1, -1, -1), True: (1, 1, 1)}
CORNER_SQUARE_SIZE = (0.2, 0.2)
CORNER_SQUARE_POS = (0.8, -0.75)
N_REPS_LOGGING = 2
AFTER_LOGGING_PAUSE_MS = 100

# Visual stimuli:
MONITOR = "BENQ"
MONITOR_ID = 0
MONITOR_DISTANCE_CM = 25.0
WARP_CORRECTION: str = "spherical"
SCREEN_RATIO: float = 16 / 9
FULLSCREEN: bool = True


# Serial connections
SERIAL_PORT_OPTO = "COM18"
SERIAL_PORT_SERVO = "COM29"
BOUD_RATE = 9600

# Servo ball stimulus
SERVO_BALL_SIZE_CM = 3
SERVO_DEFAULT_MS_PER_DEG = 4
MOTION_SPEED_DEG_S = 1000 / SERVO_DEFAULT_MS_PER_DEG

# Setup geometry
SERVO_RADIUS_CM = 15
HEAD_SERVO_CENTER_CM = 17
SERVO_BALL_SIZE_CM = 3
SERVO_CENTER_ANGLE_DEG = 25
SERVO_Y_POS_ANGLE_DEG = -8

# Serial connections params
SERIAL_CONN_PAUSE_S = 5  # pause after establishing serial connection
