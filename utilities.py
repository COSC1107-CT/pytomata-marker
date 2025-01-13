""" """

import sys
import pathlib
import argparse
import importlib.util


# NOTE: Incorporate any further configuration options here.
def construct_and_parse_args():
    """ """
    args = {
        "description": "",
        "epilog": "standard output is used for results and feedback by default",
        "allow_abbrev": False,
    }
    parser = argparse.ArgumentParser(**args)
    args = {
        ("questions_script_path",): {
            "help": "path to script containing instructor-defined question functions",
            "type": pathlib.Path,
            "metavar": "QUESTIONS",
        },
        ("solution_paths",): {
            "help": "paths to files and directories containing student solutions",
            "nargs": "+",
            "type": pathlib.Path,
            "metavar": "SOLUTIONS",
        },
        ("-o", "--output"): {
            "help": "directory for saving results and feedback",
            "dest": "output_directory_path",
            "type": pathlib.Path,
            "metavar": "OUTPUT",
        },
        ("-p", "--processes"): {
            "help": "specify processes to distribute solutions across",
            "dest": "process_count",
            "type": int,
            "default": 1,
            "metavar": "PROCESSES",
        },
    }
    for values, config in args.items():
        parser.add_argument(*values, **config)
    return parser.parse_args()


def load_using_path(path, identifier=""):
    """ """
    specification = importlib.util.spec_from_file_location(identifier, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[identifier] = module
    specification.loader.exec_module(module)
    return module
