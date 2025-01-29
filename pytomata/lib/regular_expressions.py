""" """

import .configuration


# TODO: Finish docstrings with usage instructions.


@configuration.apply_penalty_values()
def check_words_are_subset_of_language(
    words,
    language_regular_expression,
    *,
    question_value,
    incorrect_penalty,
    additional_test_cases=None,
):
    """ """
    pass



@configuration.apply_penalty_values()
def check_words_are_subset_of_language_intersection(
    words,
    language_regular_expressions,
    *,
    question_value,
    incorrect_penalty,
    additional_test_cases=None,
):
    """ """
    pass


@configuration.apply_penalty_values()
def check_words_are_subset_of_language_difference(
    words,
    language_regular_expressions,
    *,
    question_value,
    incorrect_penalty,
    additional_test_cases=None,
):
    """ """
    pass
