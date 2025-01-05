"""
Script for configuring questions and executing the autograder.
"""

import argparse
import pathlib


# TODO: Handle feedback generation and output.
def initiate_autograding_procedure():
    """ """
    args = configure_and_parse_args()


def execute_autograder_and_construct_feedback():
    """ """
    pass


def configure_questions():
    """ """
    return []


# TODO: Finalise help and description strings.
def configure_and_parse_args():
    """ """
    parser = argparse.ArgumentParser(**{
        "description": "",
        "epilog": "",
    })
    args = {
        ("questions",): {
            "help": "path to the instructor question script or package",
            "metavar": "QUESTIONS",
            "type": pathlib.Path,
        },
        ("solutions",): {
            "help": "path to the student solution script or directory",
            "metavar": "SOLUTIONS",
            "type": pathlib.Path,
        },
        ("-o", "--output"): {
            "help": "specify an output file or directory for feedback",
            "metavar": "PATH",
            "type": pathlib.Path,
        }
    }
    for options, config in args.items():
        parser.add_argument(*options, **config)
    return parser.parse_args()


if __name__ == "__main__":
    initiate_autograding_procedure()
