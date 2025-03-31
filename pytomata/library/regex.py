""" """

import functools

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
    regex, regexes = regexes[0], regexes[1:]
    difference_nfa = functools.reduce(
        lambda nfa_1, nfa_2: nfa_1.difference(nfa_2),
        map(nfa.NFA.from_regex, regexes),
        nfa.NFA.from_regex(regex),
    )
    accepted = len(list(filter(difference_nfa.accepts_input, student_inputs)))
    return question_value * (accepted / len(student_inputs))
