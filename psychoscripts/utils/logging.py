import sys
from datetime import datetime
from pathlib import Path

from psychopy import logging

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


if __name__ == "__main__":
    create_psychopy_logger()
