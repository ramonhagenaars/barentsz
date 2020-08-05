import inspect
from pathlib import Path


def here(frames_back: int = 0) -> Path:
    """
    Get the current directory from which this function is called.
    Args:
        frames_back: the number of extra frames to look back.

    Returns: the directory as a Path instance.

    """
    stack = inspect.stack()
    previous_frame = stack[1 + frames_back]
    return Path(previous_frame.filename).parent
