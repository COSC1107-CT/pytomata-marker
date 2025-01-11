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
    output_results_and_feedback(
        partition_solutions_and_invoke_autograder(
            args.questions_file_path,
            args.solutions_file_and_directory_paths,
            args.process_count,
        ),
        args.output_path,
    )


def partition_solutions_and_invoke_autograder(
    questions_file_path,
    solutions_file_and_directory_paths,
    process_count,
):
    """ """

    def retrieve_solution_scripts():
        """ """
        solution_scripts = []
        for path in solutions_file_and_directory_paths:
            if path.is_file() and path[:-3] == ".py":
                solution_scripts.append(path)
            elif path.is_dir():
                solution_scripts.extend(path.glob("*.py"))
        return tuple(solution_scripts)

    def partition_solutions(solution_scripts):
        """ """
        partition_size = len(solution_scripts) // process_count
        return (
            solution_scripts[offset_index::partition_size]
            for offset_index in range(partition_size)
        )

    questions = load_using_path(questions_file_path, "questions")
    # TODO: Only for processes > 1 to avoid overhead?
    with multiprocessing.Pool(process_count) as process_pool:
        _ = process_pool.map(
            functools.partial(invoke_autograder_over_partition, questions),
            partition_solutions(retrieve_solution_scripts()),
        )


def invoke_autograder_over_partition(questions, solution_partition):
    """ """

    def grade_individual_solution(solution_script):
        """ """
        # TODO: This!
        solutions = load_using_path(solution_script, "")
        return autograding.execute_autograding_procedure(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    return list(map(grade_individual_solution, solution_partition))


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


def load_using_path(path, identifier=""):
    """ """
    specification = importlib.util.spec_from_file_location(identifier, path)
    loaded = importlib.util.module_from_spec(specification)
    sys.modules[identifier] = loaded
    specification.loader.exec_module(loaded)
    return loaded


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
        ("questions_file_path",): {
            "help": "specify path to instructor-defined question functions",
            "type": pathlib.Path,
            "metavar": "QUESTIONS",
        },
        ("solutions_file_and_directory_paths",): {
            "help": "specify path to student solutions",
            "nargs": "+",
            "type": pathlib.Path,
            "metavar": "SOLUTIONS",
        },
        ("-o", "--output"): {
            "help": "specify directory for the autograder results",
            "dest": "output_path",
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


if __name__ == "__main__":
    execute_autograding_procedure()
