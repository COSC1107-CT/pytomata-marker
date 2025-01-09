""" """

import pathlib
import argparse
import autograding


# TODO: Should path validation happen here, or inside the invocation function?
def execute_autograding_procedure():
    """ """
    args = construct_and_parse_args()
    output_results_and_feedback(
        autograding.execute_autograding_procedure(
            args.questions_path,
            args.solutions_path,
        ),
        args.output_path,
    )


def output_results_and_feedback(autograder_output, output_path=None):
    """ """
    print(autograder_output)
    if output_path is None:
        # TODO: Print to standard output.
        pass
    elif output_path.is_file():
        # TODO: All feedback to the provided file.
        pass
    elif output_path.is_dir():
        # TODO: One feedback file per student inside the given directory.
        pass


def construct_and_parse_args():
    """ """
    # TODO: Finish.
    args = {
        "description": "",
        "epilog": "",
        "allow_abbrev": False,
    }
    parser = argparse.ArgumentParser(**args)
    args = {
        ("questions_path",): {
            "help": "path to instructor-defined question functions",
            "type": pathlib.Path,
            "metavar": "QUESTIONS",
        },
        ("solutions_path",): {
            "help": "path to student solutions",
            "type": pathlib.Path,
            "metavar": "SOLUTIONS",
        },
        ("-o", "--output"): {
            "help": "path for autograder results and feedback",
            "type": pathlib.Path,
            "metavar": "OUTPUT",
        },
    }
    for values, config in args.items():
        parser.add_argument(*values, **config)
    return parser.parse_args()


if __name__ == "__main__":
    execute_autograding_procedure()
