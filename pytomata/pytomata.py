""" """

import dataclasses
import importlib.util
import multiprocessing
import pathlib
import sys
import typing


@dataclasses.dataclass(frozen=True)
class ProcessContext:
    """ """

    questions_script_path: pathlib.Path
    output_directory_path: pathlib.Path


@dataclasses.dataclass(frozen=True)
class MarkedQuestionResponse:
    """ """

    question_label: str
    question_value: float
    student_result: float
    student_feedback: str


@dataclasses.dataclass(frozen=True)
class StudentResults:
    """ """

    student_id: str
    results: typing.Sequence[MarkedQuestionResponse]


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
        partition_index = 0
        for path in student_solution_paths:
            if path.is_file() and path.suffix == ".py":
                student_solution_partitions[partition_index].append(path)
                partition_index = (partition_index + 1) % process_count
            elif path.is_dir():
                for script_path in path.glob("*.py"):
                    student_solution_partitions[partition_index].append(script_path)
                    partition_index = (partition_index + 1) % process_count
        return student_solution_partitions

    if output_directory_path is not None:
        output_directory_path.mkdir(parents=True, exist_ok=True)
    student_solution_partitions = derive_and_partition_student_solution_files()
    process_context = ProcessContext(questions_script_path, output_directory_path)
    lock = multiprocessing.Lock()
    with multiprocessing.Pool(process_count, initialise_process, (lock,)) as pool:
        pool.starmap(
            calculate_and_output_results_for_student_solution_partition,
            zip(student_solution_partitions, [process_context] * process_count),
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
            solutions = load_using_path(student_solution_path)
            student_id = student_solution_path.stem
            yield StudentResults(
                student_id, calculate_student_results_and_feedback(solutions)
            )

    def calculate_student_results_and_feedback(solutions):
        """ """
        return [
            MarkedQuestionResponse(label, value, *question(solution(), value))
            for label, value, question, solution in questions.construct_questions_and_solutions(
                solutions
            )
        ]

    def output_individual_student_results():
        """ """
        student_output = generate_student_output(student_results)
        if output_directory_path is None:
            shared_exclusion_lock.acquire()
            try:
                print("\n", student_output, "\n", sep="")
            finally:
                shared_exclusion_lock.release()
        else:
            output_path = output_directory_path / f"{student_results.student_id}.out"
            with open(output_path, "w+") as output_file:
                output_file.write(student_output + "\n")

    questions_script_path, output_directory_path = process_context
    questions = load_using_path(questions_script_path)
    for student_results in calculate_results_for_solution_partition():
        output_individual_student_results()


def generate_student_output(student_results):
    """ """

    def generate_question_output(result):
        """ """
        feedback = result.student_feedback
        if isinstance(feedback, list):
            feedback = "\n".join(feedback)
        return f"{result.label} | {result.student_score} / {result.question_value}\n{feedback}"

    question_output = map(generate_question_output, student_results.results)
    return "\n\n".join([f"*** {student_results.student_id} ***", *question_output])


def load_using_path(path, identifier=""):
    """ """
    specification = importlib.util.spec_from_file_location(identifier, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[identifier] = module
    specification.loader.exec_module(module)
    return module
