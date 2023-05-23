from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import sleep

import nidaqmx
import numpy as np
from psychopy import core, visual
from psychopy.visual import Circle, GratingStim
from psychopy.visual.windowwarp import Warper

from psychoscripts import defaults
from psychoscripts.utils.visual_screen import get_default_psychopy_win


@dataclass
class ExpParams:
    warper_correction: str = "spherical"
    ball_distance: float = 25.0
    n_reps: int = 2
    units: str = "deg"
    dot_size: tuple = (3, 3)
    dot_drift_coef: float = 0.1


params = ExpParams()
window = get_default_psychopy_win()

# Draw the stimuli and update the window
circle = visual.Circle(window, size=params.dot_size, color=(-1, -1, -1))

pos = 0
vel = 0
starting_pos = 0
trial_clock = core.Clock()

start_distance = defaults.MONITOR_DISTANCE_CM
final_position = 10
motion_speed_cm_s = defaults.MOTION_SPEED_CM_S
diameter = defaults.SERVO_BALL_SIZE_CM

distance = start_distance - final_position
motion_duration_s = distance / motion_speed_cm_s

start_t = trial_clock.getTime()
elapsed = 0
while trial_clock.getTime() - start_t < motion_duration_s:
    position = start_distance - distance * elapsed / motion_duration_s
    # Get angular size from diameter and distance:
    angular_size = np.arctan(diameter / (2 * position)) * 2 * 180 / np.pi
    circle.size = (angular_size, angular_size)
    circle.draw()
    window.flip()
    elapsed = trial_clock.getTime() - start_t
print(elapsed, angular_size)

sleep(2)

window.close()
core.quit()
