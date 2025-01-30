""" """

import pytomata.lib


def construct_questions_and_solutions(solutions):
    """ """
    return [
        (
            "1.a.i",
            100,
            exercise_1_question_a_1,
            solutions.exercise_1_question_a_1_solution,
        )
    ]


def exercise_1_question_a_1(solution, question_value):
    """ """
    language_regex = "abc"
    additional_test_cases = [
        ("a*b*c*", 0.2, "You failed!"),
        ("a*b*cc", -0.3, None),
    ]
    student_result, student_feedback = (
        pytomata.lib.check_words_are_subset_of_regex_language(
            solution,
            language_regex,
            question_value=question_value,
            additional_test_cases=additional_test_cases,
        )
    )
    return student_result, student_feedback
