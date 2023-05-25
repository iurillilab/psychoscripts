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
    warper_correction: str = "spherical"
    ball_distance: float = 25.0
    n_reps: int = 2
    units: str = "deg"
    dot_size: tuple = (3, 3)
    dot_drift_coef: float = 0.1


params = ExpParams()
window = get_default_psychopy_win()

data_logger = PsychopyLogger()
corner_logger = CornerLogger(window, data_logger)

# Draw the stimuli and update the window
circle = visual.Circle(window, size=params.dot_size, color=(-1, -1, -1))


start_angle = 0
final_angle = 100
motion_speed_deg_s = defaults.MOTION_SPEED_DEG_S
diameter = defaults.SERVO_BALL_SIZE_CM

angular_distance = final_angle - start_angle
motion_duration_s = angular_distance / motion_speed_deg_s

y_pos = defaults.SERVO_Y_POS_ANGLE_DEG
r = defaults.SERVO_RADIUS_CM
pv = defaults.HEAD_SERVO_CENTER_CM
qpv_deg = defaults.SERVO_CENTER_ANGLE_DEG


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
