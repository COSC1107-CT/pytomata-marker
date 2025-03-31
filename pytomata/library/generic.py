""" """


def generic_accept_reject_procedure(
    student_auto,
    *,
    accept_set,
    reject_set,
    question_value,
):
    """
    Checks that the supplied `student_auto` accepts and rejects input as intended.
    The `accept_set` contains strings that should be accepted, and the `reject_set` those that should not be.
    If less than 50% of strings are correctly accepted and rejected, zero is returned.
    Above 50% the product of the proportion and `question_value` is returned.

    ```python
    ```
    """
    accepted = set(filter(student_auto.accepts_input, accept_set))
    rejected = reject_set.difference(filter(student_auto.accepts_input, reject_set))
    proportion = (len(accepted) + len(rejected)) / (len(accept_set) + len(reject_set))
    if proportion < 0.5:
        return 0.0, "Incorrect!"
    accept_report = ["Rejected:", *accept_set.difference(accepted)]
    reject_report = ["Accepted:", *reject_set.difference(rejected)]
    return question_value * proportion, "\n".join(accept_report + reject_report)
