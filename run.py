""" """

import dataclasses
import itertools
import multiprocessing
import pathlib

import configure
import pytomata
import utilities

# TODO: Use generator to yield and output student solutions!


@dataclasses.dataclass
class ProcessContext:
    """ """

    questions_path: pathlib.Path
    output_directory_path: pathlib.Path


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
        return [
            solution_paths[index :: args.process_count]
            for index in range(args.process_count)
        ]

    args = utilities.construct_and_parse_args()
    if args.output_directory_path is not None:
        args.output_directory_path.mkdir(parents=True, exist_ok=True)
    results = invoke_autograder(
        partition_solution_paths(),
        ProcessContext(args.questions_path, args.output_directory_path),
        args.process_count,
    )
    if args.output_directory_path is None:
        output = configure.generate_output(results)
        print("\n\n".join(output))


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

    def invoke_autograder_over_solution(student_solution_path):
        """ """
        student = student_solution_path.stem
        solutions = utilities.load_using_path(student_solution_path, student)
        return student, pytomata.calculate_student_results(
            configure.construct_questions_and_solutions(questions, solutions)
        )

    def output_results_and_feedback_to_files(results):
        """ """
        labelled_output = zip(results, configure.generate_output(results))
        for (student, _), output in labelled_output:
            path = process_context.output_directory_path / f"{student}.out"
            with open(path, "w+") as file:
                file.write(output)

    questions = utilities.load_using_path(
        process_context.questions_path, "questions"
    )
    all_results = list(map(invoke_autograder_over_solution, solution_partition))
    if process_context.output_directory_path is not None:
        output_results_and_feedback_to_files(all_results)
    return all_results


if __name__ == "__main__":
    invoke_autograder_and_output_feedback()
