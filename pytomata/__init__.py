import os
from pathlib import Path
from importlib.metadata import version
from .pytomata import (
    calculate_and_output_student_results as calculate_and_output_student_results,
)


def get_pkg_root() -> Path:
    """
    Returns the root of the package folder
    :return: Root Path
    """
    import inspect

    # one way
    # loc: str = os.path.abspath(__file__)
    # p: Path = Path(loc)
    # root: Path = p.parents[1]   # one level up

    # another way...
    root = Path(os.path.dirname(inspect.getfile(inspect.currentframe())))
    return root


ROOT_PATH = get_pkg_root()
VERSION = version("pytomata-marker")
