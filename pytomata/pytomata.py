""" """

import functools
import importlib.util
import multiprocessing
import pathlib
import sys
from typing import List, Sequence

from .elements import (
    MarkedQuestionResponse,
    ProcessContext,
    StudentResults,
)


# TODO: Use this as the shared entry point for package and CLI invocations.
def calculate_and_output_student_results(
    questions_path: pathlib.Path,
    output_path: pathlib.Path,
    submissions_paths: Sequence[pathlib.Path],
    *,
    process_count: int = 1,
):
    """Main automarking system with the arguments from CLI.
    This function is the main entry point for the automarking system.

    It can use multiprocessing to distribute the workload across multiple processes.

    Args:
        questions_path (pathlib.Path): a path to a script containing instructor-defined question functions
        output_path (pathlib.Path): a path to a directory for saving results and feedback
        submissions_paths (Sequence[pathlib.Path]): a list of paths to scripts and directories containing student solutions
        process_count (int): number of processes to distribute solutions across
    """

    def partition_submissions():
        """Partition the student solution files into groups for each process.
        This is done to distribute the workload across multiple processes.
        Each process will receive a list of student solution files to process.

        Submissions are in list list-Sequence submissions_paths
        Each submission is either a submission file or a directory with many submission files.

        The function returns a list of lists, where the i-th list contains the paths to the student solution files for the i-th process
        """
        student_solution_partitions = [[] for _ in range(process_count)]
        partition_index = 0
        for path in submissions_paths:
            if path.is_file() and path.suffix == ".py":
                student_solution_partitions[partition_index].append(path)
                partition_index = (partition_index + 1) % process_count
            elif path.is_dir():
                for script_path in path.glob("*.py"):
                    student_solution_partitions[partition_index].append(script_path)
                    partition_index = (partition_index + 1) % process_count
        return student_solution_partitions

    if output_path is not None:
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        print()  # Spacing for CLI results output.

    # create a process context object to pass to each process
    #   this is a static object, so it can be shared across processes
    #   contains: path to questions and path to output directory
    # then run the marking process in parallel across multiple processes
    marking_context = ProcessContext(questions_path, output_path)
    lock = multiprocessing.Lock()
    with multiprocessing.Pool(process_count, initialise_process, (lock,)) as pool:
        pool.map(
            functools.partial(
                calculate_and_output_results_for_student_solution_partition,
                marking_context,
            ),
            partition_submissions(), # list of lists of submission paths
        )


def initialise_process(lock):
    """ """
    global shared_exclusion_lock
    shared_exclusion_lock = lock


def calculate_and_output_results_for_student_solution_partition(
    process_context,
    submissions_partition,
):
    """ """

    def calculate_results_for_solution_partition() -> Sequence[StudentResults]:
        """ """
        for submission_path in submissions_partition:
            # submission_path is of form tests/ct19/submissions/s0000002.py
            # we can extract student id (s0000002)
            submission = load_using_path(submission_path)
            student_id = submission_path.stem
            # MARK the student submission
            yield StudentResults(
                student_id, calculate_student_results_and_feedback(submission)
            )

    def calculate_student_results_and_feedback(
        submission,
    ) -> List[MarkedQuestionResponse]:
        """ """
        return [
            MarkedQuestionResponse(label, value, *question(solution(), value))
            for label, value, question, solution in questions.main(submission)
        ]

    def output_individual_student_results():
        """ """
        student_output = generate_student_output(student_results)
        if process_context.output_directory_path is None:
            shared_exclusion_lock.acquire()
            try:
                print(student_output, "\n")
            finally:
                shared_exclusion_lock.release()
        else:
            output_path = (
                process_context.output_directory_path
                / f"{student_results.student_id}.out"
            )
            with open(output_path, "w+") as output_file:
                output_file.write(student_output + "\n")

    # Load the questions script and calculate results for each student solution.
    questions = load_using_path(process_context.questions_script_path)
    for student_results in calculate_results_for_solution_partition():
        output_individual_student_results()


def generate_student_output(student_results):
    """ """

    def generate_question_output(result):
        """ """
        feedback = result.student_feedback
        if isinstance(feedback, list):
            feedback = "\n".join(feedback)
        display_text = f"{result.question_label:10} [{result.student_result:.2f}/{result.question_value:.2f}]"
        if feedback:
            display_text += f"\n{feedback}"
        return display_text

    question_output = map(generate_question_output, student_results.results)
    return "\n".join([f"{student_results.student_id}", *question_output])


def load_using_path(path, identifier=""):
    """ """
    specification = importlib.util.spec_from_file_location(identifier, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[identifier] = module
    specification.loader.exec_module(module)
    return module
