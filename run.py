""" """

import pathlib
import argparse
import autograding


def execute_autograding_procedure():
    """ """
    args = construct_and_parse_args()
    output_results_and_feedback(
        invoke_autograder_over_solutions(
            args.questions_path,
            args.solutions_path,
        ),
        args.output_path,
    )


def invoke_autograder_over_solutions(questions_path, solutions_path):
    """ """
    print(questions_path)
    print(solutions_path)
    return autograding.execute_autograding_procedure([])


def output_results_and_feedback(autograder_output, output_path=None):
    """ """
    print(autograder_output)
    if output_path is None:
        # TODO: Print to standard output.
        pass
    elif output_path.is_file():
        # TODO: All feedback to the provided file?
        pass
    elif output_path.is_dir():
        # TODO: One feedback file per student inside the given directory.
        pass


# NOTE: Incorporate any further configuration options here.
def construct_and_parse_args():
    """ """
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
            "help": "directory for the autograder results and feedback",
            "type": pathlib.Path,
            "metavar": "OUTPUT",
        },
        # TODO: Multithreading support.
        ("-t", "--threads"): {
            "help": "parallel thread count to distribute solutions across",
            "type": int,
            "metavar": "THREADS"
        }
    }
    for values, config in args.items():
        parser.add_argument(*values, **config)
    return parser.parse_args()


if __name__ == "__main__":
    execute_autograding_procedure()
