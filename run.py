""" """

import multiprocessing
import autograding
import configure
import utilities


# NOTE: Updated once questions are loaded.
questions = None


def handle_autograding_invocation_and_output():
    """ """

    def update_questions():
        """ """
        global questions
        questions = utilities.load_using_path(args.questions_file_path, "")

    def partition_solutions():
        """ """
        solution_file_paths = list(args.solutions_directory_path.glob("*.py"))
        return [
            solution_file_paths[offset_index :: args.process_count]
            for offset_index in range(args.process_count)
        ]

    args = utilities.construct_and_parse_args()
    update_questions()
    results = invoke_autograder(partition_solutions(), args.process_count)
    output_results_and_feedback(results, args.output_path)


def invoke_autograder(solution_partitions, process_count):
    """ """
    with multiprocessing.Pool(process_count) as pool:
        return pool.map(grade_solution_partition, solution_partitions)


def grade_solution_partition(solution_partition):
    """ """

    def grade_solution(solution_script):
        """ """
        # TODO: Fix this!
        solutions = utilities.load_using_path(solution_script, "")
        return autograding.execute_autograding_procedure(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    return list(map(grade_solution, solution_partition))


# TODO: Actual output should be constructed here.
def output_results_and_feedback(autograder_results, output_path):
    """ """
    print(autograder_results)
    print(output_path)


if __name__ == "__main__":
    handle_autograding_invocation_and_output()
