from typing import List, Sequence
import dataclasses
import pathlib

@dataclasses.dataclass(frozen=True)
class ProcessContext:
    """A static object representing the context for a marking process.
    It contains the path to the questions script and the output directory path.

    Each student solution is marked in a separate process, and this context is passed to each process.
    """

    questions_script_path: pathlib.Path
    output_directory_path: pathlib.Path


@dataclasses.dataclass(frozen=True)
class MarkedQuestionResponse:
    """An object representing a question result with feedback."""

    question_label: str
    question_value: float
    student_result: float
    student_feedback: str


@dataclasses.dataclass(frozen=True)
class StudentResults:
    """Store the results for a student as a sequence of marked questions (each with its points and feedback)."""

    student_id: str
    results: Sequence[MarkedQuestionResponse]
