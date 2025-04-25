""" """

import automata.fa.dfa as dfa
import automata.base.exceptions as exc
import pytomata.library.generic as generic


def generic_dfa_procedure(
    correct_dfa: dfa.DFA,
    student_dfa: dfa.DFA,
    *,
    accept_set: set[str],
    reject_set: set[str],
    question_value: int,
    non_equivalence_deduction: float = 0.35,
) -> tuple[float, str]:
    """ """
    try:
        if student_dfa.issubset(correct_dfa) and student_dfa.issuperset(correct_dfa):
            return question_value, ""
        question_value *= non_equivalence_deduction
        return generic.check_against_acceptance_and_rejection_sets(
            student_dfa,
            accept_set=accept_set,
            reject_set=reject_set,
            question_value=question_value,
        )
    except exc.SymbolMismatchError as error:
        return 0, error
