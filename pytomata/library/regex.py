""" """

import functools
from typing import List

import automata.fa.dfa as dfa
import automata.fa.nfa as nfa
import automata.regex.regex as re
import pytomata.library.generic as generic


def generic_regex_procedure(
    correct_regex: str,
    student_regex: str,
    *,
    accept_set: set[str],
    reject_set: set[str],
    question_value: int,
    non_equivalence_deduction: float = 0.35,
) -> tuple[float, str]:
    """ """
    if re.isequal(correct_regex, student_regex):
        return question_value, ""
    question_value *= non_equivalence_deduction
    return generic.check_against_acceptance_and_rejection_sets(
        nfa.NFA.from_regex(student_regex),
        accept_set=accept_set,
        reject_set=reject_set,
        question_value=question_value,
    )


def check_regex_acceptance(regex: str, student_inputs: list[str], *, question_value: float) -> tuple[float, str]:
    """ """
    regex_nfa = nfa.from_regex(regex)
    accepted = len(list(filter(regex_nfa.accepts_input, student_inputs)))
    return question_value * (accepted / len(student_inputs)), ""


def check_regex_intersection_acceptance(regexes: list[str], student_inputs: list[str], *, question_value: float) -> tuple[float, str]:
    """Check if the intersection of regexes accepts the student inputs strings.

    Args:
        regexes (List[str]): regular expressions to intersect
        student_inputs (List[str]): list of string submissions
        question_value (float): total points the question is worth

    Returns:
        tuple[float, str]: point attracted + feedback
    """
    intersection_nfa = nfa.NFA.from_regex("&".join(regexes))
    accepted = list(filter(intersection_nfa.accepts_input, student_inputs))
    no_accepted = len(accepted)

    rate = (no_accepted / len(student_inputs))
    if rate == 1:
        feedback = f"All accepted!"
    else:
        rejected = [w for w in student_inputs if w not in accepted]
        feedback = f"Rejected {(1-rate)*100:.0f}%: {','.join(rejected)}"
    return question_value * rate, feedback


def check_regex_difference_acceptance(regexes: list[str], student_inputs: list[str], *, question_value: float) -> tuple[float, str]:
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
    return question_value * (accepted / len(student_inputs)), ""
