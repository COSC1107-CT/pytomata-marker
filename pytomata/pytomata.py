""" """

import functools
import importlib.util
import multiprocessing
import pathlib
import sys
from typing import List, Sequence

from proto import module

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
                perform_marking,
                marking_context,
            ),
            partition_submissions(),  # list of lists of submission paths
        )


def initialise_process(lock):
    """ """
    global shared_exclusion_lock
    shared_exclusion_lock = lock


def perform_marking(
    process_context: ProcessContext,
    submissions_paths: Sequence[pathlib.Path],
):
    """Performs marking of a set of submission files within a context

    Args:
        process_context (ProcessContext): a context object containing the path to the questions script and output directory
        submissions_partition (Sequence[pathlib.Path]): a list of paths to student solution files
    """

    def assess_submissions() -> Sequence[StudentResults]:
        """This function assess a list of submission paths, yielding the results for each submission."""
        for submission_path in submissions_paths:
            # submission_path is of form tests/ct19/submissions/s0000002.py
            # from it we extract student id (s0000002)
            student_id = submission_path.stem
            submission = get_module_from_path(submission_path)

            # MARK the student submission and yield the result
            yield StudentResults(student_id, assess_submission(submission))

    def assess_submission(submission: module) -> List[MarkedQuestionResponse]:
        """Assess the submission and return the results for each question"""

        responses = []
        for label, value, question, question_submission in questions.main(submission):
            try:
                response = MarkedQuestionResponse(
                            label,
                            value,
                            *(
                                question(question_submission(), value)
                                if question_submission
                                else (0, "Missing question!")
                            ),
                        )
            except Exception as e:
                response = MarkedQuestionResponse(
                    label, value, *(0, f"Exception loading/processing question answer: {e}")
                )

            responses.append(response)

        return responses
        # old more compact way, but cannot handle exceptions when running the question
        # return [
        #     MarkedQuestionResponse(
        #         label, value,
        #         *question(question_submission(), value) if question_submission else (0, "Missing question!")
        #     )
        #     for label, value, question, question_submission in questions.main(
        #         submission
        #     )
        # ]

    def output_submission_results(student_results: StudentResults):
        """Generate the output for a submission result

        if not output folder in contrext, then report to stdout
        otherwise, write to file in output folder
        Args:
            student_results (StudentResults): the results for a student submission
        """
        student_output = generate_student_output(student_results)
        if process_context.output_directory_path is None:
            # print in stdout atomically
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

    # Load the questions script
    #  questions is a module containing the instructor-defined question functions
    questions = get_module_from_path(process_context.questions_script_path)

    # Mark every  results for each student solution.
    for student_results in assess_submissions():
        output_submission_results(student_results)


def generate_student_output(student_results: StudentResults) -> str:
    """Generate a string output for a student result
    Args:
        student_results (StudentResults): the results for a student submission
    Returns:
        str: the output string for the student result
    """

    def generate_question_output(result):
        """ """
        feedback = result.student_feedback
        if isinstance(feedback, list):
            feedback = "\n".join(feedback)
        display_text = (
            f"{result.question_label:10} "
            f"[{result.student_result:.2f}/{result.question_value:.2f}]"
        )
        if feedback:
            display_text += f"\n{feedback}"
        return display_text

    question_output = map(generate_question_output, student_results.results)
    return "\n".join([f"Submission: {student_results.student_id}", *question_output])


def get_module_from_path(path: pathlib.Path, identifier=None) -> module:
    """Given a path to a python file, return the module object
    Args:
        path (pathlib.Path): the path to the python file
        identifier (str): the name of the module to be used in sys.modules
    Returns:
        module: the module object
    """
    if identifier is None:
        # use the file name as the module name
        identifier = path.stem

    specification = importlib.util.spec_from_file_location(identifier, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[identifier] = module
    specification.loader.exec_module(module)

    return module
