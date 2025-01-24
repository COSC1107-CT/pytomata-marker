""" """

import pytomata


def construct_questions_and_solutions(questions, solutions):
    """ """
    return [
        pytomata.QuestionConfiguration(*configuration)
        for configuration in [
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
    ]


def generate_output(results):
    """ """

    def generate_student_output(result):
        """ """
        _, student_results = result
        questions = map(generate_result_output, student_results)
        return "\n".join([f"*** {result[0]} ***", *questions])

    def generate_result_output(result):
        """ """
        return f"""
{result.question_label} | {result.student_score} / {result.question_value}
{result.student_feedback}
"""

    return list(map(generate_student_output, results))
