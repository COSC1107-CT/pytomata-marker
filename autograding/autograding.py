""" """


def grade_questions(questions_and_solutions):
    """ """
    return [
        (
            question_label,
            question_value,
            *question_function(solution_function(), question_value),
        )
        for question_label, question_value, question_function, solution_function in questions_and_solutions
    ]
