"""
Script for configuring questions and executing the autograder.
"""

# TODO: Accept arbitrary question scripts.
import questions
import argparse
import pathlib


def execute_autograder_and_construct_feedback():
    """ """
    pass


def configure_questions():
    """ """
    return []


def configure_and_parse_args():
    """ """
    args = {
        # TODO: Module and package support.
        ("QUESTIONS",): {
            "help": "Module or package containing instructor-defined functions",
            "type": pathlib.Path,
        },
        # TODO: Module and package support.
        ("SOLUTIONS",): {
            "help": "Module or package containing student solutions",
            "type": pathlib.Path,
        },
        # NOTE: File and directory support.
        ("-o", "--output"): {
            "help": "File or directory used to output results",
            "type": pathlib.Path,
        }
    }
    parser = argparse.ArgumentParser()
    for options, config in args.items():
        parser.add_argument(*options, **config)
    return parser.parse_args()


if __name__ == "__main__":
    print(configure_and_parse_args())
