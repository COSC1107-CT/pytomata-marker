def construct_questions_and_solutions(solutions):
    return [
        (
            "1.a.i",
            2,
            exercise_1_question_a_part_i,
            solutions.exercise_1_question_a_part_i_solution
        ),
        (
            "1.a.ii",
            2,
            exercise_1_question_a_part_ii,
            solutions.exercise_1_question_a_part_ii_solution
        ),
        (
            "1.a.iii",
            2,
            exercise_1_question_a_part_iii,
            solutions.exercise_1_question_a_part_iii_solution
        ),
        (
            "1.a.iv",
            2,
            exercise_1_question_a_part_iv,
            solutions.exercise_1_question_a_part_iv_solution
        ),
        (
            "1.a.v",
            2,
            exercise_1_question_a_part_v,
            solutions.exercise_1_question_a_part_v_solution
        ),
        (
            "1.a.vi",
            2,
            exercise_1_question_a_part_vi,
            solutions.exercise_1_question_a_part_vi_solution
        ),
        (
            "1.a.vii",
            2,
            exercise_1_question_a_part_vii,
            solutions.exercise_1_question_a_part_vii_solution
        ),
    ]


exercise_1_regex_1 = "(a+b*)cc*a*(c+b*)*"
exercise_2_regex_2 = "(a+b)*c*c(a*+b)*"


def exercise_1_question_a_part_i(student_solution):
    return False


def exercise_1_question_a_part_ii(student_solution):
    return False


def exercise_1_question_a_part_iii(student_solution):
    return False


def exercise_1_question_a_part_iv(student_solution):
    return False


def exercise_1_question_a_part_v(student_solution):
    return False


def exercise_1_question_a_part_vi(student_solution):
    return False


def exercise_1_question_a_part_vii(student_solution):
    return False


if __name__ == "__main__":
    pass