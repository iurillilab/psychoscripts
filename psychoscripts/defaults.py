# Read a config file from the user home directory and use it to set the default values, if available
import os

# Data logging:
# LOG_FOLDER = r"C:\Users\SNeurobiology\Desktop\jaw_opening"
LOG_FOLDER = r"/Users/vigji/Desktop"
DEFAULT_TIMESTAMPING = "%Y.%m.%d-%H.%M.%S"
try:
    MOUSE_ID = os.environ["MOUSE_ID"]
except KeyError:
    MOUSE_ID = "no_mouse_id"

# Visual stimuli:
MONITOR = "Philips"

# Serial connections
SERIAL_PORT_OPTO = "COM28"
SERIAL_PORT_SERVO = "COM29"
BOUD_RATE = 9600

# Serial connections params
SERIAL_CONN_PAUSE_S = 5  # pause after establishing serial connection
