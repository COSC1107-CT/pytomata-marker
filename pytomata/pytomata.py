""" """


def calculate_student_results_and_feedback(questions_and_solutions):
    """ """
    return [
        (label, value, *question(solution(), value))
        for label, value, question, solution in questions_and_solutions
    ]
