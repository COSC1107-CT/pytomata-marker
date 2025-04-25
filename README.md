# Pytomata Marker

This is an automarker developed to support assignments in theory of computation courses @ RMIT University.

It is a re-development of the [JFLAP Automarker](https://github.com/COSC1107-CT/jflap-ct-automarker) system, but done in Python and heavily relying on [Automata](https://caleb531.github.io/automata/) library, which provides regular expression and automata APIs.

Official GitHub repo: https://github.com/COSC1107-CT/pytomata-marker

- [Pytomata Marker](#pytomata-marker)
  - [Install](#install)
  - [Usage](#usage)
    - [Execution Options](#execution-options)
  - [Assessment Design \& Configuration](#assessment-design--configuration)
    - [Main configuration](#main-configuration)
    - [Question functions](#question-functions)
      - [Using Library Functions](#using-library-functions)
      - [Defining Additional Test Cases](#defining-additional-test-cases)
    - [Solutions](#solutions)
  - [Library Function Catalogue](#library-function-catalogue)
  - [Development](#development)
    - [Adding Project Dependencies](#adding-project-dependencies)
    - [Writing Library Functions](#writing-library-functions)
      - [Configuring Default Penalties](#configuring-default-penalties)
      - [Penalising \& Updating Scores](#penalising--updating-scores)
      - [Handling Additional Test Cases](#handling-additional-test-cases)
      - [Documenting Library Functions](#documenting-library-functions)
    - [Style Considerations](#style-considerations)
      - [Linting \& Formatting](#linting--formatting)
      - [Library Function Auxiliaries](#library-function-auxiliaries)
  - [Contributors](#contributors)

## Install

The automarker system is distributed as a package (`pytomata-marker`) and can then be installed via pip from the repo as follows:

```shell
$ pip install git+https://github.com/COSC1107-CT/pytomata-marker/
```

Alternatively, one can clone first and install the planner:

```shell
$ git clone https://github.com/COSC1107-CT/pytomata-marker/
$ cd cfond-asp
$ pip install .
```

> [!TIP]
> If you plan to develop on Pytomata Marker it can be useful to install the cloned repo as [editable project](https://setuptools.pypa.io/en/latest/userguide/development_mode.html) via `pip install -e .`

Once installed, the planner is available via its CLI interface:

```shell
 $ pytomata-marker -h
usage: pytomata-marker [-h] [-o OUTPUT] [-p PROCESSES] [-q] QUESTIONS SOLUTIONS [SOLUTIONS ...]

Pytomata automarking system for Automata Theory and Formal Languages courses - Version 0.1.0

positional arguments:
  QUESTIONS             path to script containing instructor-defined question functions
  SOLUTIONS             paths to scripts and directories containing student solutions

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        directory for saving results and feedback
  -p PROCESSES, --processes PROCESSES
                        specify processes to distribute solutions across
  -q, --quiet           suppress all output

standard output is used for results and feedback by default
```

You can achieve the same usign `python -m pytomata -h`

## Usage

This section details executing the marking procedure.
For explanations of the different files involved, refer to the [assessment design and configuration](#assessment-design--configuration) section.
Here, we use example files located in the `tests` directory:

```plaintext
$ tree tests --gitignore
tests
├── questions.py
└── submissions
    ├── s0000000.py
    ├── s0000001.py
    └── s0000002.py
```

The system requires the following as inputs:

1. A Python script containing the instructor-defined [question](#questions) and [configuration](#configuration) functions;
2. An arbitrary list of Python scripts and directories containing students’ [solutions](#solutions).

> For assistance, use `python automarker.py -h`.

Therefore, to process an individual submission:

```shell
$ pytomata-marker tests/ct19/questions.py tests/ct19/submissions/s0000000.py
Using CPython 3.13.1
Creating virtual environment at: .venv
Installed 6 packages in 4ms

*** s0000000 ***

1.a.i | 100 / 100
Correct!
```

When a directory is supplied, all Python scripts inside that directory (non-recursively) are treated as student submissions:

```shell
$ python -m pytomata tests/ct19/questions.py tests/ct19/submissions/s0000000.py
*** s0000002 ***

1.a.i | 100 / 100
Correct!


*** s0000001 ***

1.a.i | 0 / 100
Rejected: cba


*** s0000000 ***

1.a.i | 100 / 100
Correct!
```

By default, all results are printed to standard output.

### Execution Options

To save each student’s result to an individual file instead of printing to standard output, use the `--output` or `-o` flag:

```shell
$ pytomata-marker tests/ct19/questions.py tests/ct19/submissions --output output_directory
```

Marking in parallel is also supported though the `--processes` or `-p` flag, which distributes the student solutions evenly across three processes:

```shell
$ pytomata-marker tests/ct19/questions.py tests/ct19/submissions --processes 3
```

## Assessment Design & Configuration

This section details the definition of questions by an instructor, the submission of solutions by students, and the configuration necessary to match submissions against the correct marking function.

Both question and submission functions are intended to make heavy use of the [Automata](https://caleb531.github.io/automata/) library.

### Main configuration

A question script should contain a `main` function, like this:

```python
def main(solutions):
    return [
        (
            "1.a.i",    # id of the question
            2.0,        # points worth
            exercise_1_question_a_1,    # question function
            solutions.exercise_1_question_a_1_solution, # solution function
        ),
        (
            "1.a.ii",
            4.0,
            exercise_1_question_a_2,
            solutions.exercise_1_question_a_2_solution,
        ),
    ]
```

> [!WARNING]
> This function must be called `main` and define one parameter, used internally to pass an individual student module. This facilitates pairing each student’s submissions against the same respective marking functions.

This function returns a _sequence_ of 4-tuples, each specifying specifying:

1. The label of the question.
2. Total number of points worth.
3. Question function.
4. Solution functions.

The question and solution functions should correspond to those defined by the [questions](#questions) and [solutions](#solutions) scripts, respectively.

### Question functions

Questions are defined using _functions_.

Each question is a single function that must accept _i)_ a student’s answer to the question; and _ii)_ the total allocated points for the question, and must returns the points attracted and any (textual) feedback, in that order.

```python
import automata

def exercise_1_question_a_1(student_solution, question_value):
    """Check student answer for the question; calculate points attracted and feedback

        student_solution: the student's submission answer for this question
        question_value: how many points this question is worth
    """

    # Invoke automarker library function here to check student solution.

    return student_result, student_feedback
```

#### Using Library Functions

Library functions provided by `pytomata.lib` are provided to apply template marking scheme to handle certain archetypal questions (e.g., marking of a DFA submission for a language). These functions all return the student result (points achieved) and feedback, just like question functions.

The template usage is as follows:

```python
import pytomata.lib

student_result, student_feedback = pytomata.lib.library_function(
    student_solution,
    actual_solution,
    question_value=question_value,
    incorrect_penalty=0.8,  # should be between 0 and 1 - OPTIONAL: defaults to 1
)
```

> [!WARNING]
> The `question_value` is a **required** keyword argument.
>

The `incorrect_penalty` is optional, and denotes the percentage deduction (between 0 and 1, inclusive) from the `question_value` when the student’s submission is incorrect.  The default `incorrect_penalty` is 1, indicating a 100% deduction; the example above specifies an 80% deduction.

Refer to the [library function catalogue](#library-function-catalogue) for an overview of available functions.

#### Defining Additional Test Cases

Certain library functions also accept additional test cases. Each test case represents an alternate (usually partially correct or incorrect) solution, containing:

1. A arbitrary value denoting the test case itself;
2. A value denoting a percentage of the total `question_value`;
3. Optional feedback for the test case.

```python
def exercise_1_question_a_1(student_solution, question_value):
    actual_solution = "abcd"
    additional_test_cases = [
        ("abc", 0.2, "Nearly there!"),
        ("abcde", 0.2, None),
    ]
    student_result, student_feedback = pytomata.lib.library_function(
        student_solution,
        actual_solution,
        question_value=question_value,
        additional_test_cases=additional_test_cases,
    )
    return student_result, student_feedback
```

After the student’s submission is marked against the actual solution, it is checked against each test case.
If passed, the percentage allocated to that test case is added to the student’s result.
For example, in a question worth 5 marks, a successful test case worth `0.2` will allocate 1 mark.
The test case value can also be negative, so that passing the test case deducts marks.

> [!NOTE]
> The feedback is returned when the test case is failed if the value is positive,
> and when passed if negative.

### Solutions

Student solutions are also represented using functions:

```python
import automata

def exercise_1_question_a_1_solution():
    """ """
    pass

def exercise_1_question_a_2_solution():
    """ """
    pass
```

> [!WARNING]
> Students **should not alter** the function signature.

Each function returns the student’s solution to the corresponding [question](#questions).
All students should be distributed identical scripts containing pre-defined, empty functions as above.


## Library Function Catalogue

<!-- TODO: Table containing all available functions and their behaviour. -->

| Function                                                | Behaviour                                                                                              |
|:--------------------------------------------------------|:-------------------------------------------------------------------------------------------------------|
| `check_words_are_subset_of_regex_language`              | Checks that a set of words constitute a subset a regular expression language                           |
| `check_words_are_subset_of_regex_language_intersection` | Checks that a set of words is a subset of the intersection of two or more regular expression languages |
| `check_words_are_subset_of_regex_language_difference`   | Checks that a set of words is a subset of the difference of two or more regular expression languages   |

## Development

This section is intended for contributors.
Please ensure you have read and understood this section before contributing.

### Adding Project Dependencies

To add an additional dependency, use [`uv add`](https://docs.astral.sh/uv/concepts/projects/dependencies/).
Once added, ensure the dependency is also listed by `requirements.txt`:

```shell
uv pip compile pyproject.toml -o requirements.txt
```

This ensures the project can be [configured manually](#manual-project-configuration).

### Writing Library Functions

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

#### Configuring Default Penalties

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

This applies a default 80% incorrectness penalty for the given library function.
Instructor-defined question functions can override these defaults if necessary:

```python
def exercise_1_question_a_1():
    # …
    student_result, student_feedback = pytomata.lib.another_library_function(
        question_value=5, incorrect_penalty=0.6
    )
```

Marks can be adjusted using [additional test cases](#additional-test-cases), if they are defined.

#### Penalising & Updating Scores

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

#### Handling Additional Test Cases

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

#### Documenting Library Functions

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

### Style Considerations

#### Linting & Formatting

All source code should be linted and formatted using [Ruff](https://docs.astral.sh/ruff/):

```shell
$ uv run ruff check
```

```shell
$ uv run ruff format
```

This tool is installed as a project dependency; if you aren’t using uv, omit `uv run`.
The `pyproject.toml` file contains additional [configuration](https://docs.astral.sh/ruff/configuration/).

#### Library Function Auxiliaries

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

## Contributors

The pytomata automarker was developed by Harry Porter and Sebastian Sardina in 2025, based on the [JFLAP Automarker](https://github.com/COSC1107-CT/jflap-ct-automarker) system.

**Contact:** Prof. Sebastian Sardina (ssardina@gmail.com)