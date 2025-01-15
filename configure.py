""" """

import autograding


def construct_questions_and_solutions(questions, solutions):
    """ """
    return [
        autograding.QuestionConfiguration(*configuration)
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


# TODO: Outline results and feedback structure in docstring.
def construct_results_output(student_results):
    """ """

    def construct_feedback_for_question():
        """ """
        pass

    print(*student_results)
