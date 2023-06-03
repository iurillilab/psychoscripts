from psychopy import core, event, visual

from psychoscripts.utils.logging import PsychopyLogger
from psychoscripts.utils.visual_screen import get_default_psychopy_win

from dataclasses import dataclass

from psychopy import core, logging, visual
from psychoscripts.utils.logging import CornerLogger, PsychopyLogger



@dataclass
class GratingsParams:
    n_reps: int = 4
    spatial_freq: float = 0.02
    speed_deg_s: float = 1
    drifting_time: float = 20.0

window = get_default_psychopy_win()
logger = PsychopyLogger()

data_logger = PsychopyLogger()
corner_logger = CornerLogger(window, data_logger)

grating1 = visual.GratingStim(
    window, color=[1.0, 1.0, 1.0], size=(90, 90), units="deg",
    sf=GratingsParams.spatial_freq, ori=0
)

trialClock = core.Clock()

for i in range(GratingsParams.n_reps):
    print(i)
    for direction in [1, -1]:
        corner_logger.toggle_state()
        trialClock.reset()
        while trialClock.getTime() < GratingsParams.drifting_time:  # quits after 20 secs
            data_logger.log_string(f"Moving: {direction}")

            grating1.setPhase(direction * GratingsParams.speed_deg_s * trialClock.getTime())  # drift at 1Hz
            grating1.draw()  # redraw it
            corner_logger.patch.draw()
            window.flip()  # update the screen
