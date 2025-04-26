import automata.fa.dfa as dfa
import automata.fa.nfa as nfa
from proto import module
import pytomata.library
from pytomata.utils import get_student_func


def main(submission: module) -> list:
    return [
        (
            "1.a.i",  # id
            2.0,  # total points
            exercise_1a_i,  # function checker
            get_student_func(
                submission, "exercise_1a_i_solution"
            ),  # function in submission
        ),
        (
            "1.a.ii",
            2.0,
            exercise_1a_ii,
            get_student_func(submission, "exercise_1a_ii_solution"),
        ),
        (
            "1.a.iii",
            2.0,
            exercise_1a_iii,
            get_student_func(submission, "exercise_1a_iii_solution"),
        ),
        (
            "1.a.iv",
            1.0,
            exercise_1a_iv,
            get_student_func(submission, "exercise_1a_iv_solution"),
        ),
        (
            "1.a.v",
            1.0,
            exercise_1a_v,
            get_student_func(submission, "exercise_1a_v_solution"),
        ),
        (
            "1.a.vi",
            1.0,
            exercise_1a_vi,
            get_student_func(submission, "exercise_1a_vi_solution"),
        ),
        (
            "1.a.vii",
            3.0,
            exercise_1a_vii,
            get_student_func(submission, "exercise_1a_vii_solution"),
        ),
        (
            "1.b.i",
            2.0,
            exercise_1b_i,
            get_student_func(submission, "exercise_1b_i_solution"),
        ),
        (
            "1.b.ii",
            2.0,
            exercise_1b_ii,
            get_student_func(submission, "exercise_1b_ii_solution"),
        ),
        (
            "1.b.iii",
            2.0,
            exercise_1b_iii,
            get_student_func(submission, "exercise_1b_iii_solution"),
        ),
        (
            "1.b.iv",
            2.0,
            exercise_1b_iv,
            get_student_func(submission, "exercise_1b_iv_solution"),
        ),
        (
            "3.a.v",
            4.0,
            exercise_3a_v,
            get_student_func(submission, "exercise_3a_v_solution"),
        ),
    ]


# check format accepted by library (not the same as JFLAP!):
# https://caleb531.github.io/automata/api/regular-expressions/
EX_1a_R1 = "1(1*|2*)3*(2*|3)1*2(1|3)*2*"
EX_1a_R2 = "1*3(2|3)*2*(1|3)*(1|3)*"


# TODO: why std_inputs is a tuple rather than a list of strings?
def exercise_1a_i(words, question_value):
    conditions = (
        len(words) == 2,
        all(map(bool, words)),
    )
    if not all(conditions):
        return 0, "Invalid response!"
    # these are the two regexes for the intersection
    regexes = [EX_1a_R1, EX_1a_R2]
    # use the template library to mark regex-intersection questions
    std_pts, std_feed = pytomata.library.check_regex_intersection_acceptance(
        regexes, words, question_value=question_value
    )
    return std_pts, std_feed


def exercise_1a_ii(words, question_value):
    conditions = (
        len(words) == 2,
        all(map(bool, words)),
    )
    if not all(conditions):
        return 0.0, "Invalid response!"
    regexes = [EX_1a_R1, EX_1a_R2]
    student_result, _ = pytomata.library.check_regex_difference_acceptance(
        regexes, words, question_value=question_value
    )
    return student_result, ""


def exercise_1a_iii(words, question_value):
    conditions = (
        len(words) == 2,
        all(map(bool, words)),
    )
    if not all(conditions):
        return 0.0, "Invalid response!"
    regexes = [EX_1a_R2, EX_1a_R1]
    student_result, _ = pytomata.library.check_regex_difference_acceptance(
        regexes, words, question_value=question_value
    )
    return student_result, ""


def exercise_1a_iv(word: str, question_value: float):
    """Check that both word and word + word^reverse are in L(R1)"""
    if not isinstance(word, str) and word:
        return 0.0, "Invalid response!"

    # convert R1 into a NFA
    regex_nfa = nfa.NFA.from_regex(EX_1a_R1)

    # get string word + word^reverse
    input_plus_reverse = word + word[::-1]

    # check word is accepted by R1 using Pytomata library
    correct = regex_nfa.accepts_input(word)
    # check word + word^reverse is accepted by R1 using Pytomata library
    correct = correct and regex_nfa.accepts_input(input_plus_reverse)

    # full points if both are accepted, otherwise 0
    if correct:
        return question_value, ""
    return 0.0, "Incorrect word provided!"


def exercise_1a_v(word: str, question_value):
    if not isinstance(word, str) and word:
        return 0.0, "Invalid response!"
    regex_nfa = nfa.NFA.from_regex(EX_1a_R1)
    input_plus = word + word[::-1]
    correct = regex_nfa.accepts_input(word)
    correct = correct and not regex_nfa.accepts_input(input_plus)
    if correct:
        return question_value, ""
    return 0.0, ""


def exercise_1a_vi(regex, question_value):
    return pytomata.library.check_regex_correctness(
        f"({EX_1a_R1})|({EX_1a_R2})",
        regex,
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


def exercise_1a_vii(regex, question_value):
    return pytomata.library.check_regex_correctness(
        f"({EX_1a_R1})&({EX_1a_R2})",
        regex,
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


ex_1b_L1_regex = "aaaaa(aaa)*(bb)*bb"


def exercise_1b_i(regex, question_value):
    return pytomata.library.check_regex_correctness(
        ex_1b_L1_regex,
        regex,
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


def exercise_1b_ii(regex: str, question_value: float):
    student_dfa = dfa.DFA.from_nfa(nfa.NFA.from_regex(regex))
    correct_dfa = dfa.DFA.from_nfa(nfa.NFA.from_regex(ex_1b_L1_regex)).complement()
    return pytomata.library.check_dfa_correctness(
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


def exercise_1b_iii(regex: str, question_value: float):
    student_dfa = dfa.DFA.from_nfa(nfa.NFA.from_regex(regex))

    sol_regex = "(a|b)(a|b)((a|b)(a|b)(a|b))*"
    correct_dfa = dfa.DFA.from_nfa(nfa.NFA.from_regex(sol_regex))
    return pytomata.library.check_dfa_correctness(
        correct_dfa,
        student_dfa,
        accept_set={
            "aa",
            "ba",
            "ab",
            "bb",
            "aaaaa",
            "ababa",
            "babab",
            "baaba",
            "aabab",
            "bbbbb",
            "aaaaaaaa",
            "abababab",
            "babbaabb",
            "babababa",
            "abbaabab",
            "bbbabaab",
            "baaaaabb",
            "bbbbbbbb",
            "aaaaaaaaaaa",
            "abababababb",
            "bbababababb",
            "aaababababa",
            "bbabaaabbbb",
            "bbbbbaaaaaa",
            "bbbbbbbbbbb",
        },
        reject_set={
            "()",
            "a",
            "b",
            "aaa",
            "aba",
            "bbb",
            "bab",
            "abb",
            "baa",
            "aaaa",
            "bbbb",
            "abab",
            "baba",
            "abba",
            "baab",
            "aaaaaa",
            "ababab",
            "bababa",
            "baabab",
            "bbbbbb",
            "ababab",
            "bbbbbb",
            "aaaaaaa",
            "abababa",
            "bababab",
            "bbbabab",
            "aababba",
            "bababaa",
            "bbbbbbb",
            "aaaaaaaaa",
            "bbbbbbbbb",
            "ababababa",
            "bababaabb",
            "abababbab",
        },
        question_value=question_value,
    )


def exercise_1b_iv(regex: str, question_value: float):
    student_dfa = dfa.DFA.from_nfa(nfa.NFA.from_regex(regex))

    sol_regex = "bbb*(a|c)*(a|c)c"
    correct_dfa = dfa.DFA.from_nfa(nfa.NFA.from_regex(sol_regex))
    return pytomata.library.check_dfa_correctness(
        correct_dfa,
        student_dfa,
        accept_set={
            "bbac",
            "bbbbbbbbac",
            "bbbbacacacacac",
            "bbcc",
            "bbbbbccccc",
            "bbbbbbbbbacacacacacac",
            "bbbbaaaaaac",
            "bbbbcaccacacacacacacacc",
            "bbbbbccccacaccacac",
            "bbbbbbbbbcacacacacacacccccacacccc",
        },
        reject_set={
            "()",
            "a",
            "b",
            "aaa",
            "aba",
            "bbb",
            "bab",
            "abb",
            "baa",
            "aaaa",
            "bbbb",
            "abab",
            "baba",
            "abba",
            "baab",
            "aaaaaa",
            "ababab",
            "bababa",
            "baabab",
            "bbbbbb",
            "ababab",
            "bbbbbb",
            "aaaaaaa",
            "abababa",
            "bababab",
            "bbbabab",
            "aababba",
            "bababaa",
            "bbbbbbb",
            "aaaaaaaaa",
            "bbbbbbbbb",
            "ababababa",
            "bababaabb",
            "abababbab",
        },
        question_value=question_value,
    )


DFA_3av = dfa.DFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "e"},
    input_symbols={"a", "b", "c"},
    transitions={
        "q0": {"a": "q5", "b": "q1", "c": "q3"},
        "q1": {"a": "q2", "b": "e", "c": "e"},
        "q2": {"a": "e", "b": "q0", "c": "e"},
        "q3": {"a": "q4", "b": "e", "c": "e"},
        "q4": {"a": "e", "b": "e", "c": "e"},
        "q5": {"a": "e", "b": "q6", "c": "e"},
        "q6": {"a": "q7", "b": "e", "c": "e"},
        "q7": {"a": "e", "b": "e", "c": "e"},
        "e": {"a": "e", "b": "e", "c": "e"},
    },
    initial_state="q0",
    final_states={"q4", "q7"},
)


def exercise_3a_v(dfa: dfa.DFA, question_value: float):
    student_dfa = dfa
    correct_dfa = DFA_3av
    return pytomata.library.check_dfa_correctness(
        correct_dfa,
        student_dfa,
        accept_set={
            "babbabbabbababa",
            "aba",
            "ca",
            "babbabbabbabca",
            "babbabbabbabbababa",
            "babbabbabca",
            "bababa",
            "babca",
            "babbabbabbabbabbabbabbabbabbabbabbabca",
            "babbabbabbabbabbabbabbabbabbabbabbababa",
            "babbabbabbababbabbabbabca",
            "babbabbabbababbabbabbab",
        },
        reject_set={
            "()",
            "a",
            "b",
            "c",
            "bb",
            "cc",
            "ab",
            "cb",
            "baba",
            "abaa",
            "abac",
            "babbbb",
            "aaaaaaa",
            "ccccccc",
            "babbabbabc",
            "babbabbabbabab",
            "babbabbabbabac",
            "babbabbabbabcac",
            "babbabbabbabcaa",
            "babbabbabbabcab",
            "abaaba",
            "abaabaaba",
            "cacacaca",
            "babbabcacaca",
            "abaca",
            "babbababaca",
            "babbabcaaba",
            "ababbb",
            "babaaaa",
            "aababaabbaababbb",
        },
        question_value=question_value,
    )


if __name__ == "__main__":
    pass
