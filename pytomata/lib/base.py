"""
Module containing library function auxiliaries.
"""


def penalise_score(question_value, incorrect_penalty):
    """
    Penalise the `question_value` by the `incorrect_penalty` percentage.
    The penalised value is left unrounded; see the `calculate_final_score` function.
    Also validates the penalty value.

    ```python
    >>> penalise_score(10, 0.8)
    2.0
    ```
    """
    assert 0 <= incorrect_penalty <= 1, "penalties should fall between 0 and 1"
    return question_value * (1 - incorrect_penalty)


def update_score(current_student_score, question_value, update_value):
    """
    Updates the `current_student_score` with the `update_value` percentage of the `question_value`.
    Intended for use in processing additional test cases.

    ```python
    >>> current_student_score = 2
    >>> question_value = 10
    >>> update_score(current_student_score, question_value, 0.1)
    3.0
    ```
    """
    assert -1 <= update_value <= 1, (
        "update values should fall between -1 and 1"
    )
    return current_student_score + (question_value * update_value)


def calculate_final_score(student_score, question_value):
    """
    Constrains the `student_score` to between 0 and the `question_value`,
    and returns the result rounded to the nearest integer.
    """
    return round(max(0, min(question_value, student_score)))


def run_additional_test_cases(
    test_cases,
    test_case_function,
    student_score,
    question_value,
    *test_case_args,
    **test_case_kwargs,
):
    """
    Executes `test_case_function` over each test case in `test_cases`,
    updating the `student_score` for each test_case proportional to the `question_value`.
    The first `test_case_function` positional arg is reserved for test cases.
    Any additional positional and keyword args are passed to the `test_case_function` for each test case.

    Args:
        `test_cases`: list of tuples containing the additional test case, its value, and any corresponding feedback;
        `test_case_function`: function used to evaluate each individual test case that returns a boolean indicating success;
        `student_score`: the student’s current score, before evaluating test cases;
        `question_value`: the overall question value;
        `test_case_args`: arbitrary positional args passed into the `test_case_function`;
        `test_case_kwargs`: arbitrary positional args passed into the `test_case_function`.

    Returns:
        Tuple containing the student’s updated score and a list of received test case feedback.

    ```python
    >>> def very_thorough_test_case_function(test_case, be_harsh=False):
            return not be_harsh

    >>> test_cases = [
        ("a*b*c?", 0.1, None),
        ("a*b*c+", 0.2, "Partially correct!"),
    ]
    >>> current_student_score = 8
    >>> question_value = 10
    >>> run_additional_test_cases(
        test_cases,
        very_thorough_test_case_function,
        current_student_score,
        question_value,
        be_harsh=True,
    )
    ```
    """
    test_cases_feedback = []
    for test_case in test_cases:
        _, test_case_value, test_case_feedback = test_case
        test_case_passed = test_case_function(
            test_case, *test_case_args, **test_case_kwargs
        )
        if test_case_passed:
            student_score = update_score(
                student_score, question_value, test_case_value
            )
        test_case_feedback = get_feedback(
            test_case_value, test_case_feedback, test_case_passed
        )
        if test_case_feedback:
            test_cases_feedback.append(test_case_feedback)
    return student_score, test_cases_feedback


def get_feedback(test_value, test_case_feedback, success=True):
    """
    Returns `test_case_feedback` under the correct conditions:
    when `test_value > 0` and `success is False`,
    or `test_value < 0` and `success is True`.

    ```python
    >>> test_case_value = 0.2
    >>> test_case_feedback = "Not quite!"
    >>> get_feedback(test_case_value, test_case_feedback)
    >>> get_feedback(test_case_value, test_case_feedback, success=False)
    "Not quite!"
    ```
    """
    if (success and test_value < 0) or ((not success) and test_value > 0):
        return test_case_feedback
