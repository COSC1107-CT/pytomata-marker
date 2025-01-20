""" """


def construct_questions_and_solutions(questions, solutions):
    """ """
    return [
        (
            "1.a.i",
            2,
            questions.exercise_1_question_a_1,
            solutions.exercise_1_question_a_1_solution,
        ),
        (
            "1.a.ii",
            2,
            questions.exercise_1_question_a_2,
            solutions.exercise_1_question_a_2_solution,
        ),
        (
            "1.a.iii",
            2,
            questions.exercise_1_question_a_3,
            solutions.exercise_1_question_a_3_solution,
        ),
    ]


def generate_output(results):
    """ """

    def generate_student_output(result):
        """ """
        questions = map(generate_question_output, result[1])
        return "\n".join([f"*** {result[0]} ***\n", *questions])

    def generate_question_output(result):
        """ """
        question_label, question_value, student_score, feedback = result
        return f"{question_label} | {student_score} / {question_value}\n{feedback}\n"

    return list(map(generate_student_output, results))
