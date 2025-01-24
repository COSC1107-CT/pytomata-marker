""" """

import dataclasses
import typing


@dataclasses.dataclass
class QuestionConfiguration:
    """ """

    question_label: str
    question_value: int
    question_function: typing.Callable
    solution_function: typing.Callable


@dataclasses.dataclass
class MarkingResult:
    """ """

    question_label: str
    question_value: int
    student_score: int
    student_feedback: str


def calculate_student_results(questions_and_solutions):
    """ """
    return [
        MarkingResult(
            configuration.question_label,
            configuration.question_value,
            *configuration.question_function(
                configuration.solution_function(), configuration.question_value
            ),
        )
        for configuration in questions_and_solutions
    ]
