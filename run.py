""" """

import itertools
import multiprocessing

import autograding
import configure
import utilities


def invoke_autograder_and_output_feedback():
    """ """

    def partition_solution_paths():
        """ """
        solution_paths = []
        for path in args.solution_paths:
            if path.is_file() and path.suffix == ".py":
                solution_paths.append(path)
            elif path.is_dir():
                solution_paths.extend(path.glob("*.py"))
        for index in range(args.process_count):
            yield solution_paths[index :: args.process_count]

    args = utilities.construct_and_parse_args()
    if args.output_directory_path is not None:
        args.output_directory_path.mkdir(parents=True, exist_ok=True)
    process_context = (args.questions_path, args.output_directory_path)
    results = invoke_autograder(
        partition_solution_paths(), process_context, args.process_count
    )
    if args.output_directory_path is None:
        output = generate_output(results)
        print("\n", "\n".join(output), sep="")


def invoke_autograder(solution_partitions, process_context, process_count):
    """ """
    with multiprocessing.Pool(process_count) as process_pool:
        return itertools.chain.from_iterable(
            process_pool.starmap(
                invoke_autograder_over_partition,
                ((paths, process_context) for paths in solution_partitions),
            )
        )


def invoke_autograder_over_partition(solution_partition, process_context):
    """ """

    def invoke_autograder_over_solution(solution_path):
        """ """
        student = solution_path.stem
        solutions = utilities.load_using_path(solution_path, student)
        return student, autograding.grade_questions(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    def output_results_and_feedback_to_files(results):
        """ """
        for (student, _), output in zip(results, generate_output(results)):
            with open(output_directory_path / f"{student}.out", "w+") as file:
                file.write(output)

    questions_path, output_directory_path = process_context
    questions = utilities.load_using_path(questions_path, "questions")
    results = list(map(invoke_autograder_over_solution, solution_partition))
    if output_directory_path is not None:
        output_results_and_feedback_to_files(results)
    return results


def generate_output(results):
    """ """

    def generate_student_output(result):
        """ """
        questions = map(generate_question_output, result[1])
        return "\n".join([f"*** {result[0]} ***\n", *questions])

    def generate_question_output(result):
        """ """
        question_label, question_value, student_score, feedback = result
        return f"{question_label} | {student_score} / {question_value}\n{feedback}\n"

    return list(map(generate_student_output, results))


if __name__ == "__main__":
    invoke_autograder_and_output_feedback()
