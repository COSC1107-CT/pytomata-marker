""" """

import automata.fa.nfa as nfa

import pytomata.lib.base as base
import pytomata.lib.configuration as configuration


# TODO: Better student error handling.
# TODO: Docstrings and usage.
@configuration.apply_penalty_values()
def check_words_are_subset_of_regex_language(
    words,
    regex,
    *,
    question_value,
    incorrect_penalty,
    additional_test_cases=None,
    regex_input_symbols=None,
):
    """
    ```python
    >>> words = {"a", "ab", "bcc"}
    >>> regex = "a*b*c*"
    >>> check_words_are_subset_of_language(words, regex, question_value=10)
    ...
    ```
    """

    def check_words_are_subset_of_test_case_language(test_case):
        """ """
        test_regex, test_value, test_feedback = test_case
        test_nfa = nfa.NFA.from_regex(
            test_regex, input_symbols=regex_input_symbols
        )
        for word in words:
            if not test_nfa.accepts_input(word):
                return False
        return True

    solution_nfa = nfa.NFA.from_regex(regex, input_symbols=regex_input_symbols)
    student_result, student_feedback = (
        _check_words_are_subset_of_automaton_language(
            words, solution_nfa, question_value, incorrect_penalty
        )
    )
    if additional_test_cases is not None:
        student_result, test_case_feedback = base.run_additional_test_cases(
            additional_test_cases,
            check_words_are_subset_of_test_case_language,
            student_result,
            question_value,
        )
    student_feedback.extend(test_case_feedback)
    student_feedback = student_feedback or "Correct!"
    return base.calculate_final_score(
        student_result, question_value
    ), student_feedback


@configuration.apply_penalty_values()
def check_words_are_subset_of_regex_language_intersection(
    words,
    regex_1,
    regex_2,
    *extra_regexes,
    question_value,
    incorrect_penalty,
    regex_input_symbols=None,
):
    """ """
    nfa_1 = nfa.NFA.from_regex(regex_1, input_symbols=regex_input_symbols)
    nfa_2 = nfa.NFA.from_regex(regex_2, input_symbols=regex_input_symbols)
    intersection_nfa = nfa_1.intersection(nfa_2)
    for extra_regex in extra_regexes:
        extra_nfa = nfa.NFA.from_regex(
            extra_regex, input_symbols=regex_input_symbols
        )
        intersection_nfa = intersection_nfa.intersection(extra_nfa)
    student_result, student_feedback = (
        _check_words_are_subset_of_automaton_language(
            words, intersection_nfa, question_value, incorrect_penalty
        )
    )
    return base.calculate_final_score(
        student_result, question_value
    ), student_feedback or "Correct!"


@configuration.apply_penalty_values()
def check_words_are_subset_of_language_difference(
    words,
    regex_1,
    regex_2,
    *,
    question_value,
    incorrect_penalty,
    additional_test_cases=None,
    regex_input_symbols=None,
):
    """ """
    pass


def _check_words_are_subset_of_automaton_language(
    words,
    automaton,
    question_value,
    incorrect_penalty,
):
    """ """
    student_feedback = []
    passed = True
    for word in words:
        if not automaton.accepts_input(word):
            passed = False
            student_feedback.append(f"Rejected: {word}")
    student_result = question_value
    if not passed:
        student_result = base.penalise_score(question_value, incorrect_penalty)
    return student_result, student_feedback
