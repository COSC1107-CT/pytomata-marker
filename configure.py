""" """

import autograding


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
    # NOTE: Outline all questions and solutions here.
    questions_and_solutions = [
        (
            questions.exercise_1_question_a_1,
            solutions.exercise_1_question_a_1_solution,
            3,
        ),
        (
            questions.exercise_1_question_a_2,
            solutions.exercise_1_question_a_2_solution,
            4,
        ),
        (
            questions.exercise_1_question_a_3,
            solutions.exercise_1_question_a_3_solution,
            5,
        ),
    ]
    return [
        autograding.QuestionConfiguration(*configuration)
        for configuration in questions_and_solutions
    ]


# TODO: Outline results and feedback structure in docstring.
def construct_results_output(student, student_results):
    """ """
    print(student, *student_results)
