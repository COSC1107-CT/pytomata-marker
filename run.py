"""
Autograder invocation script.
Also handles the output of results and feedback.
"""

import argparse
import pathlib


# TODO: Handle feedback generation and output.
def invoke_autograding_procedure():
    """ """
    args = configure_and_parse_args()
    execute_autograder_and_construct_feedback(args)
    handle_results_and_feedback_output(args)


def execute_autograder_and_construct_feedback(args):
    """ """
    pass


def handle_results_and_feedback_output(args):
    """ """
    pass


# TODO: Finalise help and description strings.
def configure_and_parse_args():
    """ """
    args = {
        "description": "",
        "epilog": "",
    }
    parser = argparse.ArgumentParser(**args)
    args = {
        ("questions_path",): {
            "help": "path to the instructor question script or package",
            "metavar": "QUESTIONS_PATH",
            "type": pathlib.Path,
        },
        ("solutions_path",): {
            "help": "path to the student solution script or directory",
            "metavar": "SOLUTIONS_PATH",
            "type": pathlib.Path,
        },
        ("-o", "--output"): {
            "help": "specify an output file or directory for feedback",
            "dest": "output_path",
            "metavar": "PATH",
            "type": pathlib.Path,
        },
    }
    for options, config in args.items():
        parser.add_argument(*options, **config)
    return parser.parse_args()


if __name__ == "__main__":
    invoke_autograding_procedure()
