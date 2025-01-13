""" """

import typing
import dataclasses


@dataclasses.dataclass
class QuestionConfiguration:
    """ """

    question_function: typing.Callable
    solution_function: typing.Callable
    question_label: str
    question_value: int


@dataclasses.dataclass
class QuestionResult:
    """ """

    question_label: str
    student_result: int
    student_feedback: str


@dataclasses.dataclass
class QuestionTestCase:
    """ """

    # TODO: Update this type annotation?
    test_case: typing.Any
    pass_update: float


# TODO: Finish docstring and usage directions.
def execute_autograding_procedure(questions_and_solutions):
    """ """
    return tuple(
        QuestionResult(
            question.question_label,
            *question.question_function(
                question.solution_function(), question.question_value
            ),
        )
        for question in questions_and_solutions
    )
