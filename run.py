""" """

import multiprocessing

import autograding
import configure
import utilities


def invoke_autograder_and_output_results():
    """ """

    def partition_solution_paths():
        """ """
        solution_paths = []
        for path in args.solution_paths:
            if path.is_file() and path.suffix == ".py":
                solution_paths.append(path)
            elif path.is_dir():
                solution_paths.extend(path.glob("*.py"))
        return [
            solution_paths[index :: args.process_count]
            for index in range(args.process_count)
        ]

    args = utilities.construct_and_parse_args()
    process_context = (args.questions_path, args.output_directory_path)
    results = invoke_autograder(
        partition_solution_paths(), process_context, args.process_count
    )
    output_results_and_feedback(results)


def invoke_autograder(solution_partitions, process_context, process_count):
    """ """
    with multiprocessing.Pool(process_count) as process_pool:
        return [
            student_result
            for partition_results in process_pool.starmap(
                invoke_autograder_over_partition,
                ((paths, process_context) for paths in solution_partitions),
            )
            for student_result in partition_results
        ]


def invoke_autograder_over_partition(solution_partition, process_context):
    """ """

    def invoke_autograder_over_solution(solution_path):
        """ """
        student = solution_path.stem
        solutions = utilities.load_using_path(solution_path, student)
        return student, autograding.grade_questions(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    questions_path, _ = process_context
    questions = utilities.load_using_path(questions_path, "questions")
    return [
        invoke_autograder_over_solution(solution_path)
        for solution_path in solution_partition
    ]


def output_results_and_feedback(results):
    """ """
    for result in results:
        print(result)


if __name__ == "__main__":
    invoke_autograder_and_output_results()
