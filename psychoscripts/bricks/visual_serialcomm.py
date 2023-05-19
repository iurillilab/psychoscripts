from psychopy import core, visual

from psychoscripts.utils.visual_screen import get_default_psychopy_win
from psychoscripts.utils.logging import create_psychopy_logger
from psychoscripts.utils.logging import CornerLogger
EXP_NAME = "isi_sweeps"


window = get_default_psychopy_win()

data_logger = create_psychopy_logger()

# Draw the stimuli and update the window
corner_logger = CornerLogger(window, data_logger)
corner_logger.log_string(EXP_NAME)

window.close()
core.quit()
