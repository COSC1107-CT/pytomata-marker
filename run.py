""" """

import multiprocessing
import pathlib
import dataclasses
import autograding
import configure
import utilities


@dataclasses.dataclass
class ProcessContext:
    """ """

    questions_script_path: pathlib.Path
    output_directory_path: pathlib.Path


# TODO: Accept individual solution scripts again.
def invoke_autograder_and_output_results_and_feedback():
    """ """

    def resolve_solution_paths():
        """ """
        solution_paths = []
        for path in args.solution_paths:
            if path.is_file() and path.suffix == ".py":
                solution_paths.append(path)
            elif path.is_dir():
                solution_paths.extend(path.glob("*.py"))
        return solution_paths

    def partition_solution_files(solution_paths):
        """ """
        return [
            solution_paths[offset :: args.process_count]
            for offset in range(args.process_count)
        ]

    args = utilities.construct_and_parse_args()
    results_and_feedback = invoke_autograder(
        partition_solution_files(resolve_solution_paths()),
        ProcessContext(args.questions_script_path, args.output_directory_path),
        args.process_count,
    )
    output_results_and_feedback(
        results_and_feedback, args.output_directory_path
    )


def invoke_autograder(solution_subsets, process_context, process_count):
    """ """
    with multiprocessing.Pool(process_count) as pool:
        return pool.starmap(
            grade_solution_subset,
            ((process_context, subset) for subset in solution_subsets),
        )


# TODO: Output to files inside subprocesses?
def grade_solution_subset(process_context, solution_subset):
    """ """

    def grade_solution(solution_script):
        """ """
        student = solution_script.stem
        solutions = utilities.load_using_path(solution_script, student)
        return student, autograding.execute_autograding_procedure(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    print(process_context)
    questions = utilities.load_using_path(
        process_context.questions_script_path, "questions"
    )
    return list(map(grade_solution, solution_subset))


def output_results_and_feedback(results_and_feedback, output_directory_path):
    """ """

    # TODO: Actual output should be constructed here.
    def construct_results_and_feedback_output(student, results):
        """ """
        print(student, results)

    print(output_directory_path, *results_and_feedback, sep="\n")


if __name__ == "__main__":
    invoke_autograder_and_output_results_and_feedback()
