from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import sleep

import nidaqmx
import numpy as np
from psychopy import core, visual
from psychopy.visual import Circle, GratingStim
from psychopy.visual.windowwarp import Warper
from psychoscripts.utils.logging import CornerLogger, PsychopyLogger
from psychopy import core, logging, visual


from psychoscripts import defaults
from psychoscripts.utils.visual_screen import get_default_psychopy_win


@dataclass
class ExpParams:
    n_reps: int = 20
    units: str = "deg"
    dot_size: tuple = (3, 1)
    dot_drift_coef: float = 0.1


params = ExpParams()
window = get_default_psychopy_win()

data_logger = PsychopyLogger()
corner_logger = CornerLogger(window, data_logger)

# Draw the stimuli and update the window
circle = visual.Circle(window, size=params.dot_size, color=(-1, -1, -1))


trials = []
for i in range(ExpParams.n_reps):
    for laser in [True, False]:
            trials.append(
                dict(tlaser=laser)
            )
np.random.shuffle(trials)

trial_clock = core.Clock()
start_t = trial_clock.getTime()

elapsed = 0
while trial_clock.getTime() - start_t < motion_duration_s:
    angle_position = (start_angle + angular_distance * elapsed / motion_duration_s) / 180 * np.pi

    projection_angle = qpv_deg - (np.arctan(r * np.sin(angle_position) / (pv + r * np.cos(angle_position)))) * 180 / np.pi

    # Get angular size from diameter and distance:
    distance = np.sqrt((pv**2 + r**2 + 2 * pv * r * np.cos(angle_position)))
    angular_size = np.arctan(diameter / (2 * distance)) * 2 * 180 / np.pi
    circle.size = (angular_size, angular_size)
    circle.pos = (projection_angle, y_pos)
    circle.draw()
    window.flip()
    elapsed = trial_clock.getTime() - start_t


sleep(5)

window.close()
core.quit()
