"""This submission does not even load as it has syntaxt error"""
import automata.fa.dfa as dfa
import automata.fa.nfa as nfa

# This should be a PERFECT submission: 0000000


##################
# Exercise 1
##################


def exercise_1a_i_solution():
    return "132", "11332213"


def exercise_1a_ii_solution():
    return "12", "132132"


def exercise_1a_iii_solution():
    return "3", "132321"


dsef exercise_1a_iv_solution():
    return "12"


# def exercise_1a_v_solution():
#     return "12122"


def exercise_1a_vi_solution():
    return "(1(1*|2*)3*(2*|3)1*2(1|3)*2*)|(1*3(2|3)*2*(1|3)*(1|3)*)"


def exercise_1a_vii_solution():
    return "11*33*22*(()|1(1|3)*|33*(()|22*|1(1|3)*))"


def exercise_1b_i_solution():
    return "aaaaa(aaa)*bb(bb)*"


def exercise_1b_ii_solution():
    return "((aa|((()|a)(aaa)*))b*)|(a*(()|b(bb)*))|((a|b)*b(a|b)*a(a|b)*)"


def exercise_1b_iii_solution():
    return "(a|b)(a|b)((a|b)(a|b)(a|b))*"


def exercise_1b_iv_solution():
    return "bbb*(a|c)*(a|c)c"


##################
# Exercise 3
##################


def exercise_3a_v_solution():
    DFA = dfa.DFA(
        states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "e"},
        input_symbols={"a", "b", "c"},
        transitXions={
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

    return DFA
