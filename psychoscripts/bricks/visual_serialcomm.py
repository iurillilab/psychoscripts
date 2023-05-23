from psychopy import core, visual

from psychoscripts.utils.logging import CornerLogger, PsychopyLogger
from psychoscripts.utils.visual_screen import get_default_psychopy_win

EXP_NAME = "isi_sweeps"


window = get_default_psychopy_win()

data_logger = PsychopyLogger()

# Draw the stimuli and update the window
corner_logger = CornerLogger(window, data_logger)
corner_logger.log_string(EXP_NAME)

window.close()
core.quit()
