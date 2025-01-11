""" """

import sys
import pathlib
import argparse
import functools
import multiprocessing
import importlib.util
import autograding
import configure


def execute_autograding_procedure():
    """ """
    args = construct_and_parse_args()
    print(args)
    output_results_and_feedback(
        partition_solutions_and_invoke_autograder(
            args.questions_path,
            args.solutions_path,
            args.process_count,
        ),
        args.output_path,
    )


def partition_solutions_and_invoke_autograder(
    questions_path,
    solutions_path,
    process_count,
):
    """ """

    # TODO: Load solutions.
    def retrieve_solution_scripts():
        """ """
        return []

    def partition_solutions(solution_scripts):
        """ """
        partition_size = len(solution_scripts) // process_count
        return [
            solution_scripts[offset_index::partition_size]
            for offset_index in range(partition_size)
        ]

    questions = load_using_path(questions_path, "questions")
    # TODO: Only for processes > 1 to avoid overhead?
    with multiprocessing.Pool(process_count) as process_pool:
        results_and_feedback = process_pool.map(
            functools.partial(invoke_autograder_over_solutions, questions),
            partition_solutions(retrieve_solution_scripts()),
        )
        print(results_and_feedback)


def invoke_autograder_over_solutions(questions, solutions):
    """ """
    return []


def load_using_path(path, identifier=""):
    """ """
    specification = importlib.util.spec_from_file_location(identifier, path)
    loaded = importlib.util.module_from_spec(specification)
    sys.modules[identifier] = loaded
    spec.loader.exec_module(loaded)
    return loaded


# NOTE: Produce actual output structure here.
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
            "dest": "output_path",
            "type": pathlib.Path,
            "metavar": "OUTPUT",
        },
        ("-p", "--processes"): {
            "help": "processes to distribute solutions across",
            "dest": "process_count",
            "type": int,
            "default": 1,
            "metavar": "PROCESSES",
        },
    }
    for values, config in args.items():
        parser.add_argument(*values, **config)
    return parser.parse_args()


if __name__ == "__main__":
    execute_autograding_procedure()
