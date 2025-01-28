""" """


def construct_questions_and_solutions(solutions):
    """ """
    return [
        (
            "1.a.i",
            2,
            exercise_1_question_a_1,
            solutions.exercise_1_question_a_1_solution,
        ),
        (
            "1.a.ii",
            2,
            exercise_1_question_a_2,
            solutions.exercise_1_question_a_2_solution,
        ),
        (
            "1.a.iii",
            2,
            exercise_1_question_a_3,
            solutions.exercise_1_question_a_3_solution,
        ),
    ]


def exercise_1_question_a_1(solution, question_value):
    """ """
    return (question_value, "Correct!") if solution else (0, "Incorrect!")


def exercise_1_question_a_2(solution, question_value):
    """ """
    return (question_value, "Correct!") if solution else (0, "Incorrect!")


def exercise_1_question_a_3(solution, question_value):
    """ """
    return (question_value, "Correct!") if solution else (0, "Incorrect!")
