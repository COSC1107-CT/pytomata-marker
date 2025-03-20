""" """

import dataclasses
import multiprocessing
import pathlib
import typing

import pytomata
import utilities


@dataclasses.dataclass
class ProcessContext:
    questions_script_path: pathlib.Path
    output_directory_path: pathlib.Path


def handle_script_invocation():
    """ """
    args = utilities.construct_and_parse_args()
    return calculate_and_output_student_results(
        args.questions_script_path,
        args.output_directory_path,
        args.student_solution_paths,
        process_count=args.process_count,
    )


# TODO: Use this as the shared entry point for package and CLI invocations.
def calculate_and_output_student_results(
    questions_script_path: pathlib.Path,
    output_directory_path: pathlib.Path,
    student_solution_paths: typing.Sequence[pathlib.Path],
    *,
    process_count: int,
):
    """ """

    def derive_and_partition_student_solution_files():
        """ """
        student_solution_partitions = [[] for _ in range(process_count)]
        part_index = 0
        for path in student_solution_paths:
            if path.is_file() and path.suffix == ".py":
                student_solution_partitions[partition_index].append(path)
                part_index = (part_index + 1) % process_count
            elif path.is_dir():
                for script_path in path.glob("*.py"):
                    student_solution_partitions[part_index].append(script_path)
                    part_index = (part_index + 1) % process_count
        return student_solution_partitions

    if output_directory_path is not None:
        output_directory_path.mkdir(parents=True, exist_ok=True)
    student_solution_partitions = derive_and_partition_student_solution_files()
    process_context = (questions_script_path, output_directory_path)
    lock = multiprocessing.Lock()
    with multiprocessing.Pool(process_count, initialise_process, (lock,)) as pool:
        pool.starmap(
            calculate_and_output_results_for_student_solution_partition,
            zip(
                student_solution_partitions,
                [process_context] * process_count,
            ),
        )


def initialise_process(lock):
    """ """
    global shared_exclusion_lock
    shared_exclusion_lock = lock


def calculate_and_output_results_for_student_solution_partition(
    student_solution_partition,
    process_context,
):
    """ """

    def calculate_results_for_solution_partition():
        """ """
        for student_solution_path in student_solution_partition:
            solutions = utilities.load_using_path(student_solution_path)
            student_id = student_solution_path.stem
            student_results = pytomata.calculate_student_results_and_feedback(
                questions.construct_questions_and_solutions(solutions)
            )
            yield student_id, student_results

    def output_individual_student_results():
        """ """
        student_output = generate_student_output(student_id, student_results)
        if output_directory_path is None:
            shared_exclusion_lock.acquire()
            try:
                print("\n", student_output, "\n", sep="")
            finally:
                shared_exclusion_lock.release()
        else:
            output_path = output_directory_path / f"{student_id}.out"
            with open(output_path, "w+") as output_file:
                output_file.write(student_output + "\n")

    questions_script_path, output_directory_path = process_context
    questions = utilities.load_using_path(questions_script_path)
    for (
        student_id,
        student_results,
    ) in calculate_results_for_solution_partition():
        output_individual_student_results()


def generate_student_output(student_id, student_results):
    """ """

    def generate_question_output(question_result):
        """ """
        label, value, student_score, student_feedback = question_result
        if isinstance(student_feedback, list):
            student_feedback = "\n".join(student_feedback)
        return f"{label} | {student_score} / {value}\n{student_feedback}"

    question_output = map(generate_question_output, student_results)
    return "\n\n".join([f"*** {student_id} ***", *question_output])


if __name__ == "__main__":
    handle_script_invocation()
