""" """


def penalise_score(question_value, incorrect_penalty):
    """ """
    assert 0 <= incorrect_penalty <= 1, "penalties should fall between 0 and 1"
    return question_value * (1 - incorrect_penalty)


def update_score(current_student_score, question_value, update_value):
    """ """
    assert -1 <= update_value <= 1, "update values should fall between -1 and 1"
    return current_student_score + (question_value * update_value)


def calculate_final_score(student_score, question_value):
    """ """
    return round(max(0, min(question_value, student_score)))


def run_additional_test_cases(
    test_cases,
    test_case_function,
    student_score,
    question_value,
    *test_case_args,
    **test_case_kwargs,
):
    """ """
    test_cases_feedback = []
    for test_case in test_cases:
        test_case_update, test_case_feedback = test_case_function(
            test_case, *test_case_args, **test_case_kwargs
        )
        student_score = update_score(student_score, question_value, test_case_update)
        if test_case_feedback:
            test_cases_feedback.append(test_case_feedback)
    return student_score, test_cases_feedback
