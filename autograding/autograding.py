""" """

import typing
import dataclasses


@dataclasses.dataclass
class QuestionConfiguration:
    """ """

    question_function: typing.Callable
    solution_function: typing.Callable
    question_value: int


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
        config.question_function(
            config.solution_function(),
            config.question_value,
        )
        for config in questions_and_solutions
    )
