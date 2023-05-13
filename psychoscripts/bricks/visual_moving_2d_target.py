from pathlib import Path

import nidaqmx
from psychopy import core, visual
from psychopy.visual import Circle, GratingStim
from psychopy.visual.windowwarp import Warper

from psychoscripts import defaults

logging.console.setLevel(logging.WARNING)
from dataclasses import dataclass
from datetime import datetime

import numpy as np


@dataclass
class ExpParams:
    warper_correction: str = "spherical"
    ball_distance: float = 25.0
    n_reps: int = 2
    units: str = "deg"
    dot_size: tuple = (10, 5)
    dot_drift_coef: float = 0.1


params = ExpParams()

# Create a suitable psychopy window with some params:
window = visual.Window(
    fullscr=True,
    monitor=defaults.MONITOR,
    useFBO=True,
    units=params.units,
    color=(0, 0, 0),
    screen=1,
)
warper = Warper(window, warp=params.warper_correction)
warper.dist_cm = params.ball_distance
warper.changeProjection(params.warper_correction)

# Draw the stimuli and update the window
circle = visual.Circle(window, size=params.dot_size, color=(-1, -1, -1))


from scipy.signal import iirfilter

# b, a = iirfilter(4, Wn=2.5, fs=100, btype="low", ftype="butter")
pos = 0
vel = 0
starting_pos = 0
trial_clock = core.Clock()

past_t = trial_clock.getTime()

while True:
    circle.pos = (pos, 0)
    circle.draw()
    window.flip()
    vel += np.random.randn() * 5 - (pos - starting_pos) ** 2 * 0.1

    dt = trial_clock.getTime() - past_t
    pos = pos + dt * vel
    past_t = trial_clock.getTime()


window.close()
time.sleep(100)
core.quit()
