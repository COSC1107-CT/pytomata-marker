""" """

def generic_fsa_procedure(
    correct_dfa,
    student_dfa,
    acceptance_list,
    *,
    question_value,
    non_equivalence_deduction = 0.35,
):
    """ """
    if student_dfa.issubset(correct_dfa) and student_dfa.issuperset(correct_dfa):
        return question_value, "Equivalent!"
    question_value *= non_equivalence_deduction
    accepted = set(filter(student_dfa.accepts_input, acceptance_list))
    proportion_accepted = len(accepted) / len(acceptance_list)
    if proportion_accepted < 0.5:
        return 0.0, "Incorrect!"
    rejected = set(acceptance_list).difference(accepted)
    return question_value * proportion_accepted, "\n".join(["Rejected: ", *rejected])