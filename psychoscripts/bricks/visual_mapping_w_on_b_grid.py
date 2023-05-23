from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
from psychopy import core, logging, visual
from psychopy.visual.windowwarp import Warper

from psychoscripts import defaults
from psychoscripts.utils.logging import CornerLogger, PsychopyLogger
from psychoscripts.utils.visual_screen import get_default_psychopy_win


@dataclass
class ExpParams:
    n_reps: int = 1
    grid_n: int = 6
    stimulus_duration_s: float = 0.5


# Create a suitable psychopy window with some params:
window = get_default_psychopy_win()
data_logger = PsychopyLogger()
corner_logger = CornerLogger(window, data_logger)

# Draw the stimuli and update the window
square_size = (1 / ExpParams.grid_n, 1 / ExpParams.grid_n * defaults.SCREEN_RATIO)
patch = visual.Rect(window, size=square_size, color=(-1, -1, -1), units="norm")

starting_pos = 0
trial_clock = core.Clock()

# Create a grid of positions:
x_pos_arr = np.arange(-1 + square_size[0] / 2, 1, square_size[0])[1:-1]
y_pos_arr = np.arange(-1 + square_size[1] / 2, 1 + square_size[1] / 2, square_size[1])

# Get with the x, y positions of all patches:
positions_x, positions_y = [arr.flatten() for arr in np.meshgrid(x_pos_arr, y_pos_arr)]
n_positions = len(positions_x)

sequence_indexes = np.concatenate([np.arange(n_positions)] * ExpParams.n_reps)
np.random.shuffle(sequence_indexes)
n_stimuli = len(sequence_indexes)

idx = 0
prev_idx = 0
while trial_clock.getTime() < n_stimuli * ExpParams.stimulus_duration_s:
    idx = np.floor(trial_clock.getTime() / ExpParams.stimulus_duration_s).astype(int)

    sorted_idx = sequence_indexes[idx]
    pos = (positions_x[sorted_idx], positions_y[sorted_idx])
    patch.pos = pos
    data_logger.log_string(f"Set stimulus in position {sorted_idx}: ({pos})")

    patch.draw()

    if idx != prev_idx:
        corner_logger.toggle_state()
        prev_idx = idx

    corner_logger.patch.draw()

    window.flip()


window.close()
core.quit()
