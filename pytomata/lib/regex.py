"""
Module containing library functions for questions involving regular expressions.
"""

import functools

import automata.fa.nfa as nfa

import pytomata.lib.base as base
import pytomata.lib.configuration as configuration


@configuration.apply_penalty_values()
def check_words_are_subset_of_regex_language(
    words,
    regex,
    *,
    question_value,
    incorrect_penalty,
    additional_test_cases=None,
):
    """
    Checks that `words` is a subset of the language denoted by `regex`.
    If `additional_test_cases` are specified,
    checks that `words` is a subset of each test case regular expression.

    Args:
        `words`: set of strings denoting words in a language;
        `regex`: string denoting a regular expression that encodes a language;
        `additional_test_cases`: additional string regular expressions;

    Raises:
        `InvalidSymbolError`: reserved characters used as input symbols.

    ```python
    >>> words = {"a", "ab", "bcc", "abccc"}
    >>> solution_regex = "a*b*c*"
    >>> test_cases = [
        ("a*b*c?", 0.1, None),
        ("a*b*c+", 0.2, None),
    ]
    >>> check_words_are_subset_of_language(
        words,
        solution_regex,
        question_value=10,
        additional_test_cases=test_cases,
    )
    ```
    """

    def check_words_are_subset_of_test_case_language(test_case):
        test_nfa = nfa.NFA.from_regex(test_case[0])
        return all(map(lambda word: test_nfa.accepts_input(word), words))

    solution_nfa = nfa.NFA.from_regex(regex)
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
    student_result = base.calculate_final_score(student_result, question_value)
    return student_result, student_feedback


@configuration.apply_penalty_values()
def check_words_are_subset_of_regex_language_intersection(
    words,
    regex_1,
    regex_2,
    *extra_regexes,
    question_value,
    incorrect_penalty,
):
    """
    Checks that `words` is a subset of the intersection of the languages
    denoted by an arbitrary set of regular expressions.

    Args:
        `words`: set of strings denoting words in a language;
        `regex_1`: …;
        `regex_2`: …;
        `extra_regexes`: …

    Raises:
        `InvalidSymbolError`: reserved characters used as input symbols.

    ```python
    ```
    """
    intersection_nfa = functools.reduce(
        lambda nfa_1, nfa_2: nfa_1.intersection(nfa_2),
        map(
            lambda regex: nfa.NFA.from_regex,
            (regex_1, regex_2, *extra_regexes),
        ),
    )
    student_result, student_feedback = (
        _check_words_are_subset_of_automaton_language(
            words, intersection_nfa, question_value, incorrect_penalty
        )
    )
    student_result = base.calculate_final_score(student_result, question_value)
    return student_result, student_feedback


@configuration.apply_penalty_values()
def check_words_are_subset_of_language_difference(
    words,
    regex_1,
    regex_2,
    *extra_regexes,
    question_value,
    incorrect_penalty,
):
    """
    Checks that `words` is a subset of the difference of the languages
    denoted by an arbitrary set of regular expressions.
    Difference operation is left-associative.

    Args:
        `words`: set of strings denoting words in a language;
        `regex_1`: …;
        `regex_2`: …;
        `extra_regexes`: …

    Raises:
        `InvalidSymbolError`: reserved characters used as input symbols.

    ```python
    ```
    """
    difference_nfa = functools.reduce(
        lambda nfa_1, nfa_2: nfa_1.difference(nfa_2),
        map(
            lambda regex: nfa.NFA.from_regex,
            (regex_1, regex_2, *extra_regexes),
        ),
    )
    student_result, student_feedback = (
        _check_words_are_subset_of_automaton_language(
            words, difference_nfa, question_value, incorrect_penalty
        )
    )
    student_result = base.calculate_final_score(student_result, question_value)
    return student_result, student_feedback


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
