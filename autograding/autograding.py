""" """


# TODO: Finish docstring and usage directions.
def execute_autograding_procedure(questions_and_solutions):
    """
    ```py
    questions_and_solutions = [
        (question_function_1, solution_function_1, 2),
        (question_function_2, solution_function_2, 3),
        (question_function_3, solution_function_3, 3),
    ]
    results = execute_autograding_procedure(questions_and_solutions)
    ```
    """
    return [
        question_function(solution_function(), question_value)
        for question_function, solution_function, question_value
        in questions_and_solutions
    ]
