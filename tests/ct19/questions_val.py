"""Submission checker for CT19 exercises"""

__authors__ = "Harry Porter and Sebastian Sardina"
__version__ = "0.1.0"
__license__ = "MIT License"
import argparse
import importlib
import pathlib
import sys
import traceback
from types import NoneType

from proto import module

QUESTIONS = [
    "exercise_1a_i_solution",
    "exercise_1a_ii_solution",
    "exercise_1a_iii_solution",
    "exercise_1a_iv_solution",
    "exercise_1a_v_solution",
    "exercise_1a_vi_solution",
    "exercise_1a_vii_solution",
    "exercise_1b_i_solution",
    "exercise_1b_ii_solution",
    "exercise_1b_iii_solution",
    "exercise_1b_iv_solution",
    "exercise_3a_v_solution",
]


def get_module_from_path(path: pathlib.Path, identifier=None) -> module:
    """Given a path to a python file, return the module object
    Args:
        path (pathlib.Path): the path to the python file
        identifier (str): the name of the module to be used in sys.modules
    Returns:
        module: the module object
    """
    if identifier is None:
        # use the file name as the module name
        identifier = path.stem

    specification = importlib.util.spec_from_file_location(identifier, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[identifier] = module
    try:
        # load the module
        specification.loader.exec_module(module)
    except Exception as e:
        # if there is an error, remove the module from sys.modules
        del sys.modules[identifier]
        raise e

    return module


def get_module_func(module: module, func: str):
    """Get a function from a module by name."""
    if hasattr(module, func) and callable(getattr(module, func)):
        return getattr(module, func)
    else:
        return None


if __name__ == "__main__":
    """CLI Command line interface"""
    parser = argparse.ArgumentParser(description="Submission validator/checker")
    parser.add_argument(
        "submission", help="Submission to check/validate", type=pathlib.Path
    )
    args = parser.parse_args()
    print(args)

    try:
        submission = get_module_from_path(args.submission)
    except Exception as e:
        print(f"!!! Problem loading submission *{args.submission}*:", e)
        print("-" * 80)
        traceback.print_exc()
        print("-" * 80)
        print()
        print(
            "!!! Please check and fix the submission file. It will attract zero marks as is."
        )
        sys.exit(1)

    for question in QUESTIONS:
        try:
            func = get_module_func(
                    submission, question
                )
            print(f"Answer for *{question}*:", func())
        except Exception as e:
            print(f"!!! Problem with *{question}*:", e)
            # traceback.print_exc()
