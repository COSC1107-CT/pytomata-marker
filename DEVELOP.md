# Development

This section is intended for contributors. Please ensure you have read and understood this section before contributing.

## Writing Library Functions

Library functions adhere to a shared interface, so their usage and behaviour are consistent. They should:

- Accept a `question_value`;
- Optionally accept an `incorrect_penalty` to denote the percentage deduction for incorrect solutions;
- Optionally accept `additional_test_cases`, if applicable; if defined, test cases should always be optional.

These should always be [keyword-only arguments](https://peps.python.org/pep-3102/).

Provided these conventions are observed, additional parameters may be defined on a per-function basis.

```python
def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):
    # …
    return student_result, student_feedback
```

The body of every library function should:

1. Check the student’s answer against the specified solution, and [deduct points](#penalising--updating-scores) if not;
2. If [additional test cases](#handling-additional-test-cases) are accepted, check the student’s answer against each test case.
3. Return the student’s result and feedback, in that order.

Once defined, import the function in the `lib/__init__.py` script, and add a corresponding entry to the [library function catalogue](#library-function-catalogue).

### Configuring Default Penalties

Default incorrectness penalties are applied using the `apply_penalty_values` decorator:

```python
import .configuration

@configuration.apply_penalty_values()
def another_library_function(*args, incorrect_penalty, additional_test_cases=None):
    pass
```

> [!WARNING]
> Ensure the `apply_penalty_values` function is always **invoked** using parentheses.
> This returns the actual decorator function.

This returns a [partial object](https://docs.python.org/3/library/functools.html#partial-objects) with the `incorrect_penalty` supplied.
A 100% penalty is applied by default. To configure:

```python
@configuration.apply_penalty_values(default_incorrect_penalty=0.8)
def another_library_function(*args, incorrect_penalty, additional_test_cases=None):
    pass
```

This applies a default 80% incorrectness penalty for the given library function. Instructor-defined question functions can override these defaults if necessary:

```python
def exercise_1_question_a_1():
    # …
    student_result, student_feedback = pytomata.library.another_library_function(
        question_value=5, incorrect_penalty=0.6
    )
```

Marks can be adjusted using [additional test cases](#additional-test-cases), if they are defined.

### Penalising & Updating Scores

The `lib/base.py` script contains auxiliary functions to ensure consistent marking behaviour across all library functions.
Utilising these auxiliaries in library functions is **mandatory** for their respective operations.

To deduct the [configured incorrectness penalty](#configuring-default-penalties) for an incorrect answer,
use the `penalise_score` function.

```python
import base

def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):
    student_result = question_value
    solution_is_correct = True
    # …
    if not solution_is_correct:
        student_result = base.penalise_score(question_value, incorrect_penalty)
```

If you are not using the [test case auxiliaries](#handling-additional-test-cases), use:

1. The `update_score` function to alter the student’s score based on the test case, and;
2. The `get_feedback` function to return test case feedback under the correct circumstances.

```python
import base

def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):

    def test_case_handler(test_case):
        test_case_passed = True
        _, test_case_value, test_case_feedback = test_case
        # …
        if test_case_passed:
            student_result = base.update_score(student_result, question_value, test_case_value)
        feedback = base.get_feedback(test_case_value, test_case_feedback, test_case_passed)
        if feedback:
            student_feedback.append(feedback)


    student_result = question_value
    student_feedback = []
    # …
    if additional_test_cases is not None:
        for test_case in additional_test_cases:
            test_case_handler(test_case)
```

Finally, once the solution and test cases have been checked, use `calculate_final_score` to finalise the student’s result:

```python
import base

def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):
    student_result = question_value
    # …
    return base.calculate_final_score(student_result, question_value), student_feedback
```

This rounds the result to the nearest integer between zero and the `question_value`.

### Handling Additional Test Cases

Auxiliaries are also provided for handling additional test cases.
Unlike the [marking auxiliaries](#penalising--updating-scores), utilising these functions is optional.
Refer [here](#defining-additional-test-cases) for an explanation of additional test case behaviour.

The `run_additional_test_cases` function executes another function over each individual test case,
handling the corresponding updates to the student’s result and the collection of feedback for each test.
To utilise this function:

1. Define a function that checks the student’s solution against an arbitrary test case;
the test case should be the first parameter. This function should return `True` if the test case is passed, or `False` otherwise.
2. Invoke `run_additional_test_cases`, passing the test cases, handler function, the student’s current score, and total question value.
This returns the student’s updated result and any feedback for individual test cases.
3. Incorporate the test case feedback.

```python
def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):

    def test_case_handler_function(test_case):
        test_case_passed = True
        # …
        return test_case_passed

    student_result = question_value
    student_feedback = []
    # …
    if additional_test_cases is not None:
        student_result, test_case_feedback = base.run_additional_test_cases(
            additional_test_cases,
            test_case_handler_function,
            student_result,
            question_value,
        )
        student_feedback.extend(test_case_feedback)
```

> [!NOTE]
> The `test_case_handler_function` is an inner function out of convenience, for access to values in the enclosing scope.

If the test case handler function defines additional parameters,
these should be passed as further positional and keyword arguments to `run_additional_test_cases` as follows:

```python
def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):
    # …
    if additional_test_cases is not None:
        student_result, test_case_feedback = base.run_additional_test_cases(
            additional_test_cases,
            test_case_handler_function,
            student_result,
            question_value,
            arg_1,
            arg_2,
            key_value=key_arg,
        )


def test_case_handler_function(test_case, value_1, value_2, *, key_value):
    # …
```

This function is only applicable when all test cases are evaluated identically.

### Documenting Library Functions

All library functions should have docstrings including:

1. A description of the intended use case and behaviour;
2. A breakdown of parameters, including the structure of solutions and test cases (if applicable);
3. A maximally-detailed usage example, structured as though invoked through the CLI REPL.

```python
def another_library_function(para_1, para_2, *, question_value, incorrect_penalty, additional_test_cases=None):
    """
    Checks that the language accepted by `para_1` is a subset of the language accepted by `para_2`.
    If additional test cases are specified, checks that `para_1` is a subset of each test case language.

    Args:
        `para_1`: arbitrary regular expression;
        `para_2`: regular expression, expected to denote a superset of the `para_1` language;
        `additional_test_cases`: optional list of regular expressions; test cases succeed if `para_1` denotes a subset language.

    Raises:
        `ErrorType`: if the function raises an unhandled exception, detail this here.

    ```python
    >>> arg_1 = "ab*c*"
    >>> arg_2 = "a*b*c*d*"
    >>> test_cases = [
        ("a*b*d*c*", 0.1, None),
        ("a+b+c+d+", 0.2, None),
    ]
    >>> another_library_function(arg_1, arg_2, question_value=10, additional_test_cases=test_cases)
    ```
    """
    pass
```

The docstring style follows the [Google convention](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings), with some modifications.
The `question_value`, `incorrect_penalty`, and return values do not need to be specified,
since they are [uniform across all library functions](#writing-library-functions).

## Style Considerations

### Linting & Formatting

All source code should be linted and formatted using [Ruff](https://docs.astral.sh/ruff/):

```shell
$ uv run ruff check
```

```shell
$ uv run ruff format
```

This tool is installed as a project dependency; if you aren’t using uv, omit `uv run`.
The `pyproject.toml` file contains additional [configuration](https://docs.astral.sh/ruff/configuration/).

### Library Function Auxiliaries

If library functions depend on internal auxiliary functions,
these auxiliaries should be prefixed by `_` and left out of `lib/__init__.py`.

```python
def library_function(*args, question_value, incorrect_penalty):
    student_result, student_feedback = _auxiliary_library_function()
    # …
    return student_result, student_feedback

def _auxiliary_library_function():
    pass
```
