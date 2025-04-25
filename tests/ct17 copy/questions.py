import automata.fa.nfa as nfa
import pytomata.library


def main(solutions):
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
        (
            "1.b.i",
            2.0,
            exercise_1_question_b_part_i,
            solutions.exercise_2_question_b_part_i_solution,
        ),
        (
            "1.b.ii",
            2.0,
            exercise_1_question_b_part_ii,
            solutions.exercise_2_question_b_part_ii_solution,
        ),
    ]


exercise_1_regex_1 = "(a+b*)cc*a*(c+b*)*"
exercise_1_regex_2 = "(a+b)*c*c(a*+b)*"

exercise_1_language_1_regex = "a(aa)*bbb(bbbb)*"


def exercise_1_question_a_part_i(student_inputs, question_value):
    conditions = (
        len(student_inputs) == 2,
        all(map(bool, student_inputs)),
    )
    if not all(conditions):
        return 0, "Invalid response!"
    regexes = [exercise_1_regex_1, exercise_1_regex_2]
    student_result, _ = pytomata.library.check_regex_intersection_acceptance(
        regexes, student_inputs, question_value=question_value
    )
    return student_result, ""


def exercise_1_question_a_part_ii(student_inputs, question_value):
    conditions = (
        len(student_inputs) == 2,
        all(map(bool, student_inputs)),
    )
    if not all(conditions):
        return 0.0, "Invalid response!"
    regexes = [exercise_1_regex_1, exercise_1_regex_2]
    student_result, _ = pytomata.library.check_regex_difference_acceptance(
        regexes, student_inputs, question_value=question_value
    )
    return student_result, ""


def exercise_1_question_a_part_iii(student_inputs, question_value):
    conditions = (
        len(student_inputs) == 2,
        all(map(bool, student_inputs)),
    )
    if not all(conditions):
        return 0.0, "Invalid response!"
    regexes = [exercise_1_regex_2, exercise_1_regex_1]
    student_result, _ = pytomata.library.check_regex_difference_acceptance(
        regexes, student_inputs, question_value=question_value
    )
    return student_result, ""


def exercise_1_question_a_part_iv(student_input, question_value):
    if not isinstance(student_input, str) and student_input:
        return 0.0, "Invalid response!"
    regex_nfa = nfa.NFA.from_regex(exercise_1_regex_1)
    input_plus_reverse = student_input + student_input[::-1]
    correct = regex_nfa.accepts_input(student_input)
    correct = correct and regex_nfa.accepts_input(input_plus_reverse)
    if correct:
        return question_value, ""
    return 0.0, ""


def exercise_1_question_a_part_v(student_input, question_value):
    if not isinstance(student_input, str) and student_input:
        return 0.0, "Invalid response!"
    regex_nfa = nfa.NFA.from_regex(exercise_1_regex_1)
    input_plus = student_input + student_input[::-1]
    correct = regex_nfa.accepts_input(student_input)
    correct = correct and not regex_nfa.accepts_input(input_plus)
    if correct:
        return question_value, ""
    return 0.0, ""


def exercise_1_question_a_part_vi(student_regex, question_value):
    return pytomata.library.check_regex_correctness(
        f"({exercise_1_regex_1})|({exercise_1_regex_2})",
        student_regex,
        accept_set={
            "aaaacaaaacccbccc",
            "acacbcccbccbb",
            "cbaabbabb",
            "abccbcccbcbc",
            "aaabcbaabbbbb",
            "aaabccccbbbbaab",
            "acacbcbbcbcb",
            "ababaaaabccbbb",
            "abbcaaccbcccbb",
            "aacaacbbbcbbcb",
            "aaccacccbb",
            "ababccabbaab",
            "aaccbbccc",
            "aaaccccccbcccccb",
            "abbccbccbb",
        },
        reject_set=set(),
        question_value=question_value,
    )


def exercise_1_question_a_part_vii(student_regex, question_value):
    return pytomata.library.check_regex_correctness(
        f"({exercise_1_regex_1})&({exercise_1_regex_2})",
        student_regex,
        accept_set={
            "abccccccb",
            "aaaabccccccccc",
            "aabccccccccccccb",
            "aaaaaaaabcc",
            "aabcccccccccb",
            "aaaaabcc",
            "aaaabcccc",
            "aaaaabccb",
            "aaabccbbbbb",
            "aaabccbbb",
            "aaaaaabccc",
            "abccccccbbbb",
            "aaaaaabcccbbbbbb",
            "abccccccccbbb",
            "aaabccccbbbbbb",
        },
        reject_set=set(),
        question_value=question_value,
    )


def exercise_1_question_b_part_i(student_regex, question_value):
    return pytomata.library.check_regex_correctness(
        exercise_1_language_1_regex,
        student_regex,
        accept_set={
            "aaaaaaaaaaabbbbbbb",
            "aaabbbbbbbbbbbbbbb",
            "aaaaaaaaaaabbbbbbb",
            "aaaaaaaaaaaaaaabbb",
            "aaaaaaaaaaabbbbbbb",
            "aaaaaaaaaaabbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaaaaaabbbbbbb",
            "aaaaaaaaaaabbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaaaaaaaaaabbb",
            "aaaaaaaaaaabbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaaaaaabbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaabbbbbbbbbbb",
            "aaaaaaaaaaaaaaabbb",
            "aaabbbbbbbbbbbbbbb",
            "aaabbbbbbbbbbbbbbb",
            "aaaaaaabbbbbbbbbbb",
        },
        reject_set=set(),
        question_value=question_value,
    )


def exercise_1_question_b_part_ii(student_regex, question_value):
    return pytomata.library.check_regex_correctness(
        exercise_1_language_1_regex,
        student_regex,
        accept_set={
            "bbaabbabbbabbbbbaabbaaa",
            "baaabbbaabbaaaaabbabbbaa",
            "ababaaabababbabbbabbbb",
            "abaabbbbaababbbbba",
            "abaababbaaabbabbb",
            "abaaabbbaaabababa",
            "baabbaabbaaaabaaaab",
            "ababbabbabaabbaaaaa",
            "baabbbaaaaaababbbbabbba",
            "abaababbaaababbaaaa",
            "bbbababab",
            "babbaaabbabaaaabba",
            "aabaababaababaaaaaaa",
            "abaaaaab",
            "aabbabababbabaab",
            "bbbaabbbbabbabbbabaab",
            "ababbbbaaa",
            "aabbabbbbabaabaaaaaa",
            "abbabbabbbbabb",
            "bababbbbaaababb",
            "aaabaaaabbbaa",
            "bbabaaaabbaababbbbabba",
            "bbbbababab",
            "abaabbaabbaa",
            "abbbaababb",
        },
        reject_set=set(),
        question_value=question_value,
    )


if __name__ == "__main__":
    pass
