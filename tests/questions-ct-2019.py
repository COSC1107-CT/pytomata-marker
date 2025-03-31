import automata.fa.nfa as nfa
import pytomata.library

# TODO: Regex stuff should return feedback.


def construct_questions_and_solutions(solutions):
    return [
        (
            "1.a.i",
            2.0,
            exercise_1_question_a_part_i,
            solutions.exercise_1_question_a_part_i_solution,
        ),
        (
            "1.a.ii",
            2.0,
            exercise_1_question_a_part_ii,
            solutions.exercise_1_question_a_part_ii_solution,
        ),
        (
            "1.a.iii",
            2.0,
            exercise_1_question_a_part_iii,
            solutions.exercise_1_question_a_part_iii_solution,
        ),
        (
            "1.a.iv",
            1.0,
            exercise_1_question_a_part_iv,
            solutions.exercise_1_question_a_part_iv_solution,
        ),
        (
            "1.a.v",
            1.0,
            exercise_1_question_a_part_v,
            solutions.exercise_1_question_a_part_v_solution,
        ),
        (
            "1.a.vi",
            1.0,
            exercise_1_question_a_part_vi,
            solutions.exercise_1_question_a_part_vi_solution,
        ),
        (
            "1.a.vii",
            3.0,
            exercise_1_question_a_part_vii,
            solutions.exercise_1_question_a_part_vii_solution,
        ),
    ]


exercise_1_regex_1 = "(a+b*)cc*a*(c+b*)*"
exercise_1_regex_2 = "(a+b)*c*c(a*+b)*"


def exercise_1_question_a_part_i(student_solutions, question_value):
    conditions = (
        len(student_solutions) == 2,
        all(map(bool, student_solutions)),
    )
    if not all(conditions):
        return 0, "Invalid response!"
    regexes = [exercise_1_regex_1, exercise_1_regex_2]
    student_result = pytomata.library.check_regex_intersection_acceptance(
        regexes, student_solutions, question_value=question_value
    )
    return student_result, "Feedback!"


def exercise_1_question_a_part_ii(student_solutions, question_value):
    conditions = (
        len(student_solutions) == 2,
        all(map(bool, student_solutions)),
    )
    if not all(conditions):
        return 0.0, "Invalid response!"
    regexes = [exercise_1_regex_1, exercise_1_regex_2]
    student_result = pytomata.library.check_regex_difference_acceptance(
        regexes, student_solutions, question_value=question_value
    )
    return student_result, "Feedback!"


def exercise_1_question_a_part_iii(student_solutions, question_value):
    conditions = (
        len(student_solutions) == 2,
        all(map(bool, student_solutions)),
    )
    if not all(conditions):
        return 0.0, "Invalid response!"
    regexes = [exercise_1_regex_2, exercise_1_regex_1]
    student_result = pytomata.library.check_regex_difference_acceptance(
        regexes, student_solutions, question_value=question_value
    )
    return student_result, "Feedback!"


def exercise_1_question_a_part_iv(student_solution, question_value):
    if not isinstance(student_solution, str) and student_solution:
        return 0.0, "Invalid response!"
    student_solution_2 = student_solution + student_solution[::-1]
    regex_nfa = nfa.NFA.from_regex(exercise_1_regex_1)
    if regex_nfa.accepts_input(student_solution) and regex_nfa.accepts_input(
        student_solution_2
    ):
        return question_value, "Correct!"
    return 0.0, "Incorrect!"


def exercise_1_question_a_part_v(student_solution, question_value):
    if not isinstance(student_solution, str) and student_solution:
        return 0.0, "Invalid response!"
    student_solution_2 = student_solution + student_solution[::-1]
    regex_nfa = nfa.NFA.from_regex(exercise_1_regex_1)
    if regex_nfa.accepts_input(student_solution) and not regex_nfa.accepts_input(
        student_solution_2
    ):
        return question_value, "Correct!"
    return 0.0, "Incorrect!"


def exercise_1_question_a_part_vi(student_solution, question_value):
    return pytomata.library.generic_regex_procedure(
        f"({exercise_1_regex_1})|({exercise_1_regex_2})",
        student_solution,
        accept_set={"abc"},  # TODO: Build lists for testing.
        reject_set=set(),
        question_value=question_value,
    )


def exercise_1_question_a_part_vii(student_solution, question_value):
    return pytomata.library.generic_regex_procedure(
        f"({exercise_1_regex_1})|({exercise_1_regex_2})",
        student_solution,
        accept_set={"cba"},  # TODO: Build lists for testing.
        reject_set=set(),
        question_value=question_value,
    )


if __name__ == "__main__":
    pass
