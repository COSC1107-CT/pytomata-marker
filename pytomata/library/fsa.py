""" """

import pytomata.library.generic as generic


def generic_fsa_procedure(
    correct_fsa,
    student_fsa,
    *,
    accept_set,
    reject_set,
    question_value,
    non_equivalence_deduction=0.35,
):
    """ """
    if student_fsa.issubset(correct_fsa) and student_fsa.issuperset(correct_fsa):
        return question_value, ""
    question_value *= non_equivalence_deduction
    return generic.check_against_acceptance_and_rejection_sets(
        student_fsa,
        accept_set=accept_set,
        reject_set=reject_set,
        question_value=question_value,
    )
