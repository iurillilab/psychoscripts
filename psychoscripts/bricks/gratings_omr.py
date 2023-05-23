from psychopy import core, event, visual

from psychoscripts.utils.logging import PsychopyLogger
from psychoscripts.utils.visual_screen import get_default_psychopy_win

window = get_default_psychopy_win()
logger = PsychopyLogger()

# INITIALISE SOME STIMULI
grating1 = visual.GratingStim(
    window, color=[1.0, 1.0, 1.0], size=(90, 90), units="deg", sf=0.2, ori=0
)

trialClock = core.Clock()
t = 0
while t < 30:  # quits after 20 secs
    t = trialClock.getTime()

    grating1.setPhase(-1 * t)  # drift at 1Hz
    grating1.draw()  # redraw it
    window.flip()  # update the screen
