from psychopy.visual.windowwarp import Warper
from psychopy import visual

from psychoscripts import defaults


def get_default_psychopy_win(fullscreen=True, monitor=defaults.MONITOR,
                             use_fbo=True, units="deg", color=(0, 0, 0),
                             screen=defaults.MONITOR_ID, warp=True):
    """Create a suitable psychopy window with default params."""
    window = visual.Window(
        fullscr=fullscreen,
        monitor=monitor,
        useFBO=use_fbo,
        units=units,
        color=color,
        screen=screen,
    )

    if warp:
        warp_win(window)

    return window


def warp_win(window):
    """Warp the visual stimulus window."""
    warper = Warper(window, warp=defaults.WARP_CORRECTION)
    warper.dist_cm = defaults.MONITOR_DISTANCE
    warper.changeProjection(defaults.WARP_CORRECTION)

    return warper
