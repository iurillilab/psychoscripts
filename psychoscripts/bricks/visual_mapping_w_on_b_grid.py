from pathlib import Path

from psychopy import core, logging, visual
from psychopy.visual.windowwarp import Warper

from dataclasses import dataclass
from datetime import datetime

from psychoscripts import defaults
from psychoscripts.utils.logging import create_psychopy_logger, CornerLogger
from psychoscripts.utils.visual_screen import get_default_psychopy_win

import numpy as np

EXP_NAME = __file__.split("/")[-1].split(".")[0]


@dataclass
class ExpParams:
    n_reps: int = 1
    grid_n: int = 4


params = ExpParams()

data_logger = create_psychopy_logger()

# Create a suitable psychopy window with some params:
window = get_default_psychopy_win()




# Draw the stimuli and update the window
square_size = (1 / params.grid_n, 1 / params.grid_n * defaults.SCREEN_RATIO)
patch = visual.Rect(window, size=square_size, color=(-1, -1, -1), units="norm")

corner_logger = CornerLogger(window, data_logger)
corner_logger.log_string(EXP_NAME[:5])


pos = 0
vel = 0
starting_pos = 0
trial_clock = core.Clock()

start = trial_clock.getTime()

x_pos_arr = np.arange(-1 + square_size[0] / 2, 1, square_size[0])[1:-1]
y_pos_arr = np.arange(-1 + square_size[1] / 2, 1 + square_size[1] / 2, square_size[1])
print(square_size)
print(x_pos_arr)
print(y_pos_arr)

positions_x, positions_y = [arr.flatten() for arr in np.meshgrid(x_pos_arr, y_pos_arr)]

sorting_vals = np.concatenate([np.arange(len(positions_x))] * params.n_reps)
np.random.shuffle(sorting_vals)

positions_indices = np.arange(params.grid_n * params.grid_n)
print(len(positions_x), len(positions_indices))

dur = 0.5

idx = 0
prev_idx = 0
while trial_clock.getTime() < 10:
    idx = np.floor(trial_clock.getTime() / dur).astype(int)

    sorted_idx = sorting_vals[idx]
    patch.pos = (positions_x[sorted_idx], positions_y[sorted_idx])

    patch.draw()

    if idx != prev_idx:
        corner_logger.toggle_state()
        prev_idx = idx

    corner_logger.patch.draw()

    window.flip()


window.close()
core.quit()
