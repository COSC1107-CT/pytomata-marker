import automata.fa.nfa as nfa
import pytomata.library


def main(solutions):
    return [
        (
            "1.a.i",
            2.0,
            exercise_1a_i,
            solutions.exercise_1a_i_solution,
        ),
        (
            "1.a.ii",
            2.0,
            exercise_1a_ii,
            solutions.exercise_1a_ii_solution,
        ),
        (
            "1.a.iii",
            2.0,
            exercise_1a_iii,
            solutions.exercise_1a_iii_solution,
        ),
        (
            "1.a.iv",
            1.0,
            exercise_1a_iv,
            solutions.exercise_1a_iv_solution,
        ),
        (
            "1.a.v",
            1.0,
            exercise_1a_v,
            solutions.exercise_1a_v_solution,
        ),
        (
            "1.a.vi",
            1.0,
            exercise_1a_vi,
            solutions.exercise_1a_vi_solution,
        ),
        (
            "1.a.vii",
            3.0,
            exercise_1a_vii,
            solutions.exercise_1a_vii_solution,
        ),
        (
            "1.b.i",
            2.0,
            exercise_1b_i,
            solutions.exercise_2b_i_solution,
        ),
        (
            "1.b.ii",
            2.0,
            exercise_1b_ii,
            solutions.exercise_2b_ii_solution,
        ),
    ]


# check format accepted by library (not the same as JFLAP!):
# https://caleb531.github.io/automata/api/regular-expressions/
ex_1a_R1 = "1(1*|2*)3*(2*|3)1*2(1|3)*2*"
ex_1a_R2 = "1*3(2|3)*2*(1|3)*(1|3)*"
ex_1b_L1_regex = "aaaaa(aaa)*(bb)*bb"


# TODO: why std_inputs is a tuple rather than a list of strings?
def exercise_1a_i(std_inputs, question_value):
    conditions = (
        len(std_inputs) == 2,
        all(map(bool, std_inputs)),
    )
    if not all(conditions):
        return 0, "Invalid response!"
    # these are the two regexes for the intersection
    regexes = [ex_1a_R1, ex_1a_R2]
    # use the template library to mark regex-intersection questions
    std_pts, std_feed = pytomata.library.check_regex_intersection_acceptance(
        regexes, std_inputs, question_value=question_value
    )
    return std_pts, std_feed


def exercise_1a_ii(student_inputs, question_value):
    conditions = (
        len(student_inputs) == 2,
        all(map(bool, student_inputs)),
    )
    if not all(conditions):
        return 0.0, "Invalid response!"
    regexes = [ex_1a_R1, ex_1a_R2]
    student_result, _ = pytomata.library.check_regex_difference_acceptance(
        regexes, student_inputs, question_value=question_value
    )
    return student_result, ""


def exercise_1a_iii(student_inputs, question_value):
    conditions = (
        len(student_inputs) == 2,
        all(map(bool, student_inputs)),
    )
    if not all(conditions):
        return 0.0, "Invalid response!"
    regexes = [ex_1a_R2, ex_1a_R1]
    student_result, _ = pytomata.library.check_regex_difference_acceptance(
        regexes, student_inputs, question_value=question_value
    )
    return student_result, ""


def exercise_1a_iv(student_input, question_value):
    if not isinstance(student_input, str) and student_input:
        return 0.0, "Invalid response!"
    regex_nfa = nfa.NFA.from_regex(ex_1a_R1)
    input_plus_reverse = student_input + student_input[::-1]
    correct = regex_nfa.accepts_input(student_input)
    correct = correct and regex_nfa.accepts_input(input_plus_reverse)
    if correct:
        return question_value, ""
    return 0.0, ""


def exercise_1a_v(student_input, question_value):
    if not isinstance(student_input, str) and student_input:
        return 0.0, "Invalid response!"
    regex_nfa = nfa.NFA.from_regex(ex_1a_R1)
    input_plus = student_input + student_input[::-1]
    correct = regex_nfa.accepts_input(student_input)
    correct = correct and not regex_nfa.accepts_input(input_plus)
    if correct:
        return question_value, ""
    return 0.0, ""


# TODO: needs to be updated with the correct strings from CT19
def exercise_1a_vi(student_regex, question_value):
    return pytomata.library.generic_regex_procedure(
        f"({ex_1a_R1})|({ex_1a_R2})",
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


# TODO: needs to be updated with the correct strings from CT19
def exercise_1a_vii(student_regex, question_value):
    return pytomata.library.generic_regex_procedure(
        f"({ex_1a_R1})&({ex_1a_R2})",
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


# TODO: needs to be updated with the correct strings from CT19
def exercise_1b_i(student_regex, question_value):
    return pytomata.library.generic_regex_procedure(
        ex_1b_L1_regex,
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


# This have been fixed and they are now aligned with CT19!
def exercise_1b_ii(student_regex, question_value):
    return pytomata.library.generic_regex_procedure(
        ex_1b_L1_regex,
        student_regex,
        accept_set={
            "()",
            "bbbbbbb",
            "abbbbbbb",
            "aabbbbbbb",
            "aaaabbbbbbbb",
            "aaaaaabbbbbbbbb",
            "aaaaab",
            "aaaaabbb",
            "aaaaabbbbb",
            "aaaaaaaab",
            "aaaaaaaabbb",
            "aaaaaaaabbbbb",
            "aaaaabba",
            "baaaaabb",
        },
        reject_set={
            "aaaaabb",
            "aaaaaaaabb",
            "aaaaaaaabbbb",
            "aaaaaaaaaaabb",
            "aaaaaaaaaaabbbbbb",
            "aaaaaaaaaaaaaabbbbbb",
            "aaaaaaaaaaaaaaaaabbbbbbbb",
            "aaaaabbbbbbbbbbbb",
            "aaaaaaaabbbbbbbbbbbb",
        },
        question_value=question_value,
    )


if __name__ == "__main__":
    pass
