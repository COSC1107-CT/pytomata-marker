""" """

import functools

import automata.fa.dfa as dfa
import automata.fa.nfa as nfa


def check_regex_acceptance(regex, student_inputs, *, question_value):
    """ """
    regex_nfa = nfa.from_regex(regex)
    accepted = len(list(filter(regex_nfa.accepts_input, student_inputs)))
    return question_value * (accepted / len(student_inputs))


def check_regex_intersection_acceptance(regexes, student_inputs, *, question_value):
    """ """
    intersection_nfa = nfa.NFA.from_regex("&".join(regexes))
    accepted = len(list(filter(intersection_nfa.accepts_input, student_inputs)))
    return question_value * (accepted / len(student_inputs))


def check_regex_difference_acceptance(regexes, student_inputs, *, question_value):
    """ """

    def convert_regex_into_dfa(regex):
        return dfa.DFA.from_nfa(nfa.NFA.from_regex(regex))

    regex, regexes = regexes[0], regexes[1:]
    difference_dfa = functools.reduce(
        lambda dfa_1, dfa_2: dfa_1.difference(dfa_2),
        map(convert_regex_into_dfa, regexes),
        convert_regex_into_dfa(regex),
    )
    accepted = len(list(filter(difference_dfa.accepts_input, student_inputs)))
    return question_value * (accepted / len(student_inputs))
