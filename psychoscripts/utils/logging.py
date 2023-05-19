import sys
from datetime import datetime
from pathlib import Path
from time import sleep

from psychopy import logging, visual

from psychoscripts import defaults


def create_psychopy_logger():
    """Create a psychopy logger.

    Returns:
    --------
        logging.LogFile: A psychopy logger.
    """
    file_tstamp = str(datetime.now().strftime(defaults.DEFAULT_TIMESTAMPING))

    # Get the name of the calling script:
    frame = sys._getframe(1)  # caller's frame
    namespace = frame.f_globals  # caller's globals
    exp_name = Path(namespace["__file__"]).stem
    print(exp_name)

    full_filename = f"{exp_name}_{defaults.MOUSE_ID}_{file_tstamp}.log"

    return logging.LogFile(
        str(Path(defaults.LOG_FOLDER) / full_filename), level=logging.EXP, filemode="w"
    )


class CornerLogger:
    """Log the displayed stimuli by flickering a square in the corner."""
    square_size = defaults.CORNER_SQUARE_SIZE
    colors = defaults.CORNER_COLORS
    pos = defaults.CORNER_SQUARE_POS

    def __init__(self, window, logger) -> None:
        self.window = window
        self.logger = logger

        self.patch = visual.Rect(window, size=self.square_size, pos=self.pos,
                                 color=self.colors[False], units="norm")

        self._state = False

    @property
    def state(self) -> bool:
        """Return the state of the patch."""
        return self._state

    @state.setter
    def state(self, value) -> None:
        """Set the state of the patch."""
        self._state = value
        self.patch.color = self.colors[self._state]

    @staticmethod
    def string_to_binary(string: str) -> list[int]:
        """Convert a string in a list of ones and zeros encoding the string."""
        bitsequence = "".join(format(ord(i), "b") for i in string)

        return [int(i) for i in bitsequence]

    def refresh(self) -> None:
        """Refresh the square."""
        self.patch.draw()
        self.window.flip()

    def toggle_state(self)  -> None:
        """Toggle state of the patch without refreshing the screen."""
        self.state = not self.state

    def _internal_toggle_state(self) -> None:
        """Toggle and refresh the square."""
        self.toggle_state()
        self.refresh()

    def _header_flicker(self) -> None:
        self.state = False
        self.refresh()
        for i in range(defaults.HEADER_PULSES_N * 2):
            self._internal_toggle_state()

    def log_string(self, stimname: str) -> None:
        """Log the stimulus name by flickering the square."""
        for i in range(defaults.N_REPS_LOGGING):
            self._header_flicker()
            bitsequence = self.string_to_binary(stimname)
            for bit in bitsequence:
                self.state = bit
                self.refresh()

            self._header_flicker()
            sleep(defaults.AFTER_LOGGING_PAUSE_MS / 1000)
