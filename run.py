""" """

import multiprocessing
import functools
import dataclasses
import pathlib
import autograding
import configure
import utilities


@dataclasses.dataclass
class ProcessContext:
    questions_file_path: pathlib.Path
    output_path: pathlib.Path


# TODO: Accept individual solution scripts again.
def handle_autograding_invocation_and_output():
    """ """

    def partition_solutions():
        """ """
        solution_file_paths = list(args.solutions_directory_path.glob("*.py"))
        return [
            solution_file_paths[offset_index :: args.process_count]
            for offset_index in range(args.process_count)
        ]

    args = utilities.construct_and_parse_args()
    invoke_autograder(
        partition_solutions(),
        args.process_count,
        ProcessContext(args.questions_file_path, args.output_path),
    )


def invoke_autograder(solution_partitions, process_count, process_context):
    """ """
    with multiprocessing.Pool(process_count) as pool:
        return pool.map(
            # NOTE: Context contains data dispersed across all processes.
            functools.partial(grade_solution_partition, process_context),
            solution_partitions,
        )


# TODO: Output results inside subprocesses?
# TODO: Share the questions across the entire process pool?
def grade_solution_partition(process_context, solution_partition):
    """ """

    def grade_solution(solution_script):
        """ """
        solutions = utilities.load_using_path(
            solution_script, f"solutions.{solution_script.stem}"
        )
        return solution_script.stem, autograding.execute_autograding_procedure(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    # NOTE: Unpack any additional contextual data here.
    questions = utilities.load_using_path(
        process_context.questions_file_path, "questions"
    )
    output_results_and_feedback(map(grade_solution, solution_partition), process_context.output_path)


# TODO: Actual output should be constructed here.
def output_results_and_feedback(autograder_results, output_path):
    """ """
    print(output_path, *autograder_results)


if __name__ == "__main__":
    handle_autograding_invocation_and_output()
