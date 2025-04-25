import automata.fa.dfa as dfa
import automata.fa.nfa as nfa
import pytomata.library


def main(solutions):
    return [
        (
            "1.a.i",    # id
            2.0,        # total points
            exercise_1a_i,  # function checker
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


def exercise_1a_vi(student_regex, question_value):
    return pytomata.library.generic_regex_procedure(
        f"({ex_1a_R1})|({ex_1a_R2})",
        student_regex,
        accept_set={
            "12",
            "11111112",
            "1222222222",
            "1333333333332",
            "132",
            "1111113333332222112131313131313222222",
            "1111133333322222211231313131313",
            "133333332222222222111121313131322",
            "1111333332222211111111121313131",
            "11113333111213133331311322222",
            "111113333333322222121111333222",
            "12222333332",
            "111111122221213131313122222",
            "11312",
            "3",
            "111111113",
            "11113232323223321311313",
            "1111322222",
            "1323232311313",
            "113222222221131313",
            "3131313131313",
            "131131311313113",
            "1111113232323232232323232322223131313",
            "323232323232323232323313131311313131",
            "333333333333333",
            "33333333333322222222222222",
            "323232323232323232",
            "323",
            "31",
            "331",
        },
        reject_set={
            "()",
            "1",
            "2",
            "2111133332",
            "2132",
            "33333332333332",
            "323232323212",
            "333333112",
            "111333321112321",
            "1122331122332233",
        },
        question_value=question_value,
    )


def exercise_1a_vii(student_regex, question_value):
    return pytomata.library.generic_regex_procedure(
        f"({ex_1a_R1})&({ex_1a_R2})",
        student_regex,
        accept_set={
            "132",
            "111111132",
            "133333333332",
            "132222222",
            "111111333332222222",
            "1111322222",
            "13333322222222",
        },
        reject_set={
            "()",
            "1",
            "2",
            "3",
            "32",
            "12",
            "13",
            "3333332222222",
            "11111222222222",
            "11111333333",
            "33311112222",
            "11111",
            "2222",
            "333333",
            "111122233333",
            "222233331111",
            "33331111222222",
        },
        question_value=question_value,
    )


def exercise_1b_i(student_regex, question_value):
    return pytomata.library.generic_regex_procedure(
        ex_1b_L1_regex,
        student_regex,
        accept_set={
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
        reject_set={
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
        question_value=question_value,
    )


def exercise_1b_ii(student_regex: str, question_value: float):
    student_dfa = dfa.DFA.from_nfa(nfa.NFA.from_regex(student_regex))
    correct_dfa = dfa.DFA.from_nfa(nfa.NFA.from_regex(ex_1b_L1_regex)).complement()
    return pytomata.library.generic_dfa_procedure(
        correct_dfa,
        student_dfa,
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
