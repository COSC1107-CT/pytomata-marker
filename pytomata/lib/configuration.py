""" """

import functools


# TODO: Ask about defaults? Other values?
def apply_penalty_values(default_incorrect_penalty=1):
    """ """

    def apply_penalty_values_decorator(library_function):
        """ """
        return functools.partial(library_function, incorrect_penalty=default_incorrect_penalty)

    return apply_penalty_values_decorator
