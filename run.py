""" """

import multiprocessing
import functools
import autograding
import configure
import utilities


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
    results = invoke_autograder(
        args.questions_file_path, partition_solutions(), args.process_count
    )
    output_results_and_feedback(results, args.output_path)


def invoke_autograder(questions_file_path, solution_partitions, process_count):
    """ """
    invocation_function = functools.partial(
        grade_solution_partition, questions_file_path
    )
    with multiprocessing.Pool(process_count) as pool:
        return pool.map(invocation_function, solution_partitions)


# TODO: Share the questions across the entire process pool?
def grade_solution_partition(questions_file_path, solution_partition):
    """ """

    def grade_solution(solution_script):
        """ """
        solutions = utilities.load_using_path(
            solution_script, f"solutions.{solution_script.stem}"
        )
        return autograding.execute_autograding_procedure(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    questions = utilities.load_using_path(questions_file_path, "questions")
    return list(map(grade_solution, solution_partition))


# TODO: Actual output should be constructed here.
def output_results_and_feedback(autograder_results, output_path):
    """ """
    print(autograder_results)
    print(output_path)


if __name__ == "__main__":
    handle_autograding_invocation_and_output()
