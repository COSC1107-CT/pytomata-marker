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

    def check_words_are_subset_of_test_case_language(test_case, words):
        """ """
        test_case_regex, test_case_value, test_case_feedback = test_case
        test_case_nfa = nfa.NFA.from_regex(
            test_case_regex, input_symbols=regex_input_symbols
        )
        for word in words:
            if not test_case_nfa.accepts_input(word):
                return 0, base.get_test_case_failure_feedback(
                    test_case_feedback, test_case_value
                )
        return test_case_value, base.get_test_case_success_feedback(
            test_case_feedback, test_case_value
        )

    solution_nfa = nfa.NFA.from_regex(regex, input_symbols=regex_input_symbols)
    student_score, student_feedback = _check_words_are_subset_of_automaton_language(
        words, solution_nfa, question_value, incorrect_penalty
    )
    student_score, test_case_feedback = base.run_additional_test_cases(
        additional_test_cases,
        check_words_are_subset_of_test_case_language,
        student_score,
        question_value,
        words,
    )
    student_feedback.extend(test_case_feedback)
    return base.calculate_final_score(
        student_score, question_value
    ), student_feedback or "Correct!"


@configuration.apply_penalty_values()
def check_words_are_subset_of_regex_language_intersection(
    words,
    regex,
    *other_regexes,
    question_value,
    incorrect_penalty,
    regex_input_symbols=None,
):
    """ """
    intersection_nfa = nfa.NFA.from_regex(regex, input_symbols=regex_input_symbols)
    for other_regex in other_regexes:
        other_nfa = nfa.NFA.from_regex(other_regex, input_symbols=regex_input_symbols)
        intersection_nfa = intersection_nfa.intersection(other_nfa)
    student_score, student_feedback = _check_words_are_subset_of_automaton_language(
        words, intersection_nfa, question_value, incorrect_penalty
    )
    return base.calculate_final_score(
        student_score, question_value
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
    student_score = question_value
    if not passed:
        student_score = base.penalise_score(question_value, incorrect_penalty)
    return student_score, student_feedback
