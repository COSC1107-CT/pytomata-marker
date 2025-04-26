import automata.fa.dfa as dfa
import automata.fa.nfa as nfa


def exercise_1a_i_solution():
    return "aaaabcccbbbb", "aaaabxccbbbb"


def exercise_1a_ii_solution():
    return "abca", "acaa"


def exercise_1a_iii_solution():
    return "ccc", "ccz"


def exercise_1a_iv_solution():
    return "aabccbbccbbcbccccb"


def exercise_1a_v_solution():
    return "aaaaaaaaaacc"


def exercise_1a_vi_solution():
    return "(z?z((xy|y))((xy|y)|(xy|y))|z?z)|(xx*y*y?zz*z?x*x?zz*(y?zz*|y))"


def exercise_1a_vii_solution():
    return "(xyz)*"


def exercise_1b_i_solution():
    return "x(xx)*(xx)?yyy(yyyy)*(yyyy)?"


def exercise_1b_ii_solution():
    return "(xx)*(xy(yyyy)*((yyyx|(y(yx|x)|x))(x|y)*|(yyy|y?))|(y(x|y)*|x?))"


# def exercise_1b_iii_solution():
#     return "(a|b)(a|b)((a)(a|b)(a|b))*"


def exercise_1b_iv_solution():
    return "bbb*(a|c)*(a|c)c"

##################
# Exercise 3
##################


def exercise_3a_v_solution():
    DFA = dfa.DFA(
        states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "e"},
        input_symbols={"a", "b", "c"},
        transitions={
            "q0": {"a": "q5", "b": "q1", "c": "q1"},
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
