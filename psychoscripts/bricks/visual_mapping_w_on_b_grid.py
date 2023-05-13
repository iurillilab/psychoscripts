from pathlib import Path

from psychopy import core, logging, visual
from psychopy.visual.windowwarp import Warper

logging.console.setLevel(logging.WARNING)
from dataclasses import dataclass
from datetime import datetime

import numpy as np

EXP_NAME = "isi_sweeps"


@dataclass
class ExpParams:
    warper_correction: str = "spherical"
    ball_distance: float = 25.0
    n_reps: int = 5
    grid_n: int = 4
    screen_ratio: float = 16 / 9


params = ExpParams()

# Configure logger:
file_tstamp = str(datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
full_filename = f"{EXP_NAME}_{file_tstamp}.log"
data_logger = logging.LogFile(
    str(LOG_FOLDER / full_filename), level=logging.EXP, filemode="w"
)

# Create a suitable psychopy window with some params:
window = visual.Window(
    fullscr=True,
    monitor=MONITOR,
    useFBO=True,
    units="deg",
    color=(0, 0, 0),
    screen=1,
)
warper = Warper(window, warp=params.warper_correction)
warper.dist_cm = params.ball_distance
warper.changeProjection(params.warper_correction)

# Draw the stimuli and update the window
square_size = (1 / params.grid_n, 1 / params.grid_n * params.screen_ratio)
patch = visual.Rect(window, size=square_size, color=(-1, -1, -1), units="norm")


from scipy.signal import iirfilter

# b, a = iirfilter(4, Wn=2.5, fs=100, btype="low", ftype="butter")
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

while trial_clock.getTime() < 500:
    idx = np.floor(trial_clock.getTime() / dur).astype(int)
    sorted_idx = sorting_vals[idx]
    patch.pos = (positions_x[sorted_idx], positions_y[sorted_idx])
    patch.draw()
    window.flip()


window.close()
core.quit()
