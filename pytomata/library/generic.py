""" """

import automata.fa.fa as fa


def check_against_acceptance_and_rejection_sets(
    student_auto: fa.FA,
    *,
    accept_set: set[str],
    reject_set: set[str],
    question_value: int,
) -> tuple[float, str]:
    """
    Checks that the supplied `student_auto` accepts and rejects input as intended.
    The `accept_set` contains strings that should be accepted, and the `reject_set` those that should not be.
    If less than 50% of strings are correctly accepted and rejected, zero is returned.
    Above 50% the product of the proportion and `question_value` is returned.

    """
    assert len(accept_set) + len(reject_set) > 0
    accepted = set(filter(student_auto.accepts_input, accept_set))
    rejected = reject_set.difference(filter(student_auto.accepts_input, reject_set))
    proportion = (len(accepted) + len(rejected)) / (len(accept_set) + len(reject_set))
    if proportion < 0.5:
        return 0.0, "Incorrect!"
    feedback = []
    incorrectly_rejected = accept_set.difference(accepted)
    if incorrectly_rejected:
        feedback += [f"Incorrectly rejected: {', '.join(incorrectly_rejected)}"]
    incorrectly_accepted = reject_set.difference(rejected)
    if incorrectly_accepted:
        feedback += [f"Incorrectly accepted: {','.join(incorrectly_accepted)}"]
    return question_value * proportion, "\n".join(feedback)
