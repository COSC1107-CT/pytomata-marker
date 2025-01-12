""" """

import multiprocessing
import pathlib
import autograding
import configure
import utilities


# TODO: Accept individual solution scripts again.
def invoke_autograder_and_output_results():
    """ """

    def retrieve_and_partition_solutions():
        """ """
        solution_file_paths = list(args.solutions_directory_path.glob("*.py"))
        return [
            solution_file_paths[index :: args.process_count]
            for index in range(args.process_count)
        ]

    args = utilities.construct_and_parse_args()
    output_results(invoke_autograder(retrieve_and_partition_solutions(), args))


def invoke_autograder(solution_subsets, args):
    """ """
    process_context = (args.questions_script_path, args.output_path)
    with multiprocessing.Pool(args.process_count) as pool:
        return pool.starmap(
            grade_solution_subset,
            ((process_context, subset) for subset in solution_subsets),
        )


def grade_solution_subset(process_context, solution_subset):
    """ """

    def grade_solution(solution_script):
        """ """
        student = solution_script.stem
        solutions = utilities.load_using_path(solution_script, student)
        return student, autograding.execute_autograding_procedure(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    questions_script_path, output_directory_path = process_context
    questions = utilities.load_using_path(questions_script_path, "questions")
    return list(map(grade_solution, solution_subset))


# TODO: Actual output should be constructed here. Output serially?
def output_results(student, results):
    """ """
    print(output_directory_path, *results_and_feedback)


if __name__ == "__main__":
    invoke_autograder_and_output_results()
