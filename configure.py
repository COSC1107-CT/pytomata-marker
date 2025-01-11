""" """

# NOTE: All configurable values are located here.


def construct_questions_and_solutions(questions, solutions):
    """
    ```py
    [
        (questions.function_1, solutions.function_1, 2),
        (questions.function_2, solutions.function_2, 3),
        (questions.function_3, solutions.function_3, 3),
    ]
    ```
    """
    return [
        (
            questions.exercise_1_question_a_1,
            solutions.exercise_1_question_a_1_solution,
            5,
        ),
        (
            questions.exercise_1_question_a_2,
            solutions.exercise_1_question_a_2_solution,
            5,
        ),
        (
            questions.exercise_1_question_a_3,
            solutions.exercise_1_question_a_3_solution,
            5,
        ),
    ]
