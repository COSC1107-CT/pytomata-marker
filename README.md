[# Pytomata Marker

This is an automarker developed to support assignments in theory of computation courses @ RMIT University.

It is a re-development of the [JFLAP Automarker](https://github.com/COSC1107-CT/jflap-ct-automarker) system, but done in Python and heavily relying on [Automata](https://caleb531.github.io/automata/) library, which provides regular expression and automata APIs.

Official GitHub repo: https://github.com/COSC1107-CT/pytomata-marker

- [Install](#install)
- [Usage](#usage)
  - [Execution Options](#execution-options)
- [Assessment Design \& Configuration](#assessment-design--configuration)
  - [Questions Script](#questions-script)
  - [Question functions](#question-functions)
    - [Using Library Functions](#using-library-functions)
    - [Defining Additional Test Cases](#defining-additional-test-cases)
  - [Submissions](#submissions)
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

Submission: s0000000
1.a.i      [2.00/2.00]
All accepted!
1.a.ii     [2.00/2.00]
1.a.iii    [2.00/2.00]
1.a.iv     [1.00/1.00]
1.a.v      [1.00/1.00]
1.a.vi     [1.00/1.00]
1.a.vii    [3.00/3.00]
1.b.i      [2.00/2.00]
1.b.ii     [2.00/2.00]
1.b.iii    [2.00/2.00]
1.b.iv     [2.00/2.00]
```

When a directory is supplied, all Python scripts inside that directory (non-recursively) are treated as student submissions:

```shell
$ python -m pytomata tests/ct19/questions.py tests/ct19/submissions/s0000000.py
Submission: s0000000
1.a.i      [2.00/2.00]
All accepted!
1.a.ii     [2.00/2.00]
1.a.iii    [2.00/2.00]
1.a.iv     [1.00/1.00]
1.a.v      [1.00/1.00]
1.a.vi     [1.00/1.00]
1.a.vii    [3.00/3.00]
1.b.i      [2.00/2.00]
1.b.ii     [2.00/2.00]
1.b.iii    [2.00/2.00]
1.b.iv     [2.00/2.00]

Submission: s0000001
1.a.i      [0.00/2.00]
Rejected 100%: aaaabcccbbbb,aaaabxccbbbb
1.a.ii     [0.00/2.00]
1.a.iii    [0.00/2.00]
1.a.iv     [0.00/1.00]
1.a.v      [0.00/1.00]
1.a.vi     [0.00/1.00]
Incorrect!
1.a.vii    [0.74/3.00]
Incorrectly rejected: 111111333332222222, 111111132, 133333333332, 132222222, 1111322222, 132, 13333322222222
1.b.i      [0.43/2.00]
Incorrectly rejected: aaaaaaaabb, aaaaabb, aaaaaaaaaaaaaabbbbbb, aaaaaaaabbbbbbbbbbbb, aaaaaaaaaaaaaaaaabbbbbbbb, aaaaaaaabbbb, aaaaaaaaaaabbbbbb, aaaaaaaaaaabb, aaaaabbbbbbbbbbbb
1.b.ii     [0.00/2.00]
The input symbols between the two given DFAs do not match
1.b.iii    [0.52/2.00]
Incorrectly rejected: bbbabaab, bbbbbbbbbbb, aabab, abababab, bbbbbaaaaaa, abababababb, abbaabab, bbabaaabbbb, bbbbb, babbaabb, bbbbbbbb, bbababababb, aaababababa, babababa, babab
1.b.iv     [2.00/2.00]
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

Probably the best way to understand the automarking system is to check the example of Exercise 1 in [tests/ct19](tests/ct19).

An assessment will have two main components:

1. The _questions script_ by the instructor.
2. The _submission of solutions_ by students.

Both question and submission are basically Python functions which are intended to make heavy use of the [Automata](https://caleb531.github.io/automata/) library.

### Questions Script

A questions script basically specify the assessment. It should contain a `main` function that takes as an argument a student submission as a Python module and specifies each question by providing:

1. Id of the question as a string.
2. Number of points the question is worth.
3. Function name that marks the question.
4. Function in the submission module that encodes the student submission for the question.

The `main` function looks as follows:

```python
def main(submission: module) -> list:
    return [
        (
            "1.a.i",  # id
            2.0,  # total points
            exercise_1a_i,  # function checker
            get_student_func(
                submission, "exercise_1a_i_solution"
            ),  # function in submission
        ),
        (
            "1.a.ii",
            2.0,
            exercise_1a_ii,
            get_student_func(submission, "exercise_1a_ii_solution"),
        ),
        ...
    ]
```

> [!WARNING]
> This function must be called `main` and define one parameter, used internally to pass an individual student module. This facilitates pairing each student’s submissions against the same respective marking functions.

This function returns a _sequence_ of 4-tuples, each specifying specifying:

1. The label of the question.
2. Total number of points worth.
3. Question function.
4. Submission solution functions. Use provided tool `get_student_func` that will deal submissions that may miss some question.

The question and solution functions should correspond to those defined by the [questions](#questions) and [submissions](#submissions) scripts, respectively.

### Question functions

Questions are defined using _functions_.

Each question is a single function that mark the corresponding question and must accept:

1. a student's submission answer to the question; and
2. the total allocated points for the question.

Thq question function must returns a tuple with the points attracted as a float _and_ any (textual) feedback as a string, in that order.

This is an example:

```python
EX_1a_R1 = "1(1*|2*)3*(2*|3)1*2(1|3)*2*"

def exercise_1a_iv(word: str, question_value: float):
    """Check that both word and word + word^reverse are in L(R1)"""
    if not isinstance(word, str) and word:
        return 0.0, "Invalid response!"

    # convert R1 into a NFA
    regex_nfa = nfa.NFA.from_regex(EX_1a_R1)

    # get string word + word^reverse
    input_plus_reverse = word + word[::-1]

    # check word is accepted by R1 using Autoamta library
    correct = regex_nfa.accepts_input(word)
    # check word + word^reverse is accepted by R1 using Automata library
    correct = correct and regex_nfa.accepts_input(input_plus_reverse)

    # full points if both are accepted, otherwise 0
    if correct:
        return question_value, ""
    return 0.0, "Incorrect word provided!"
```

#### Using Library Functions

The above example question only relies on the Automata library.

Library functions provided by `pytomata.library` are provided also to apply _template marking scheme_ to handle certain _archetypal questions_ (e.g., marking of a DFA submission for a language). These functions all return the student result (points achieved) and feedback, just like question functions.

For example, consider an exercise that asks to provide a set of words that is in the language of the intersection of two regular expressions (Ex 1.a.i in CT19 test example). We make use of library template `pytomata.library.regex.check_regex_intersection_acceptance`:

```python
def check_regex_intersection_acceptance(
    regexes: list[str],
    student_inputs: list[str], *,
    question_value: float
) -> tuple[float, str]:
```

This function will take a list of regular expressions to intersect and a set of strings submitted and check how many of those strings are in the intersection language. The points awarded is proportional to the proportion of strings that pass the check.

> [!WARNING]
> The `question_value` is a **required** keyword argument, as it is needed to calculate the final points awarded.
>

Refer to the [library function catalogue](#library-function-catalogue) for an overview of available functions.

#### Defining Additional Test Cases

Certain library functions also accept additional unit test cases. These unit test cases are often used when the submitted question cannot be shown to be perfect via analytical ways (e.g., DFA equivalence check) in order to award partial points/marks.

For example, library function `pytomata.library.regex.check_regex_correctness` checks whether a regular expression is correct for the exercise:

```python
def check_regex_correctness(
    correct_regex: str,
    student_regex: str,
    *,
    accept_set: set[str],
    reject_set: set[str],
    question_value: int,
    non_equivalence_deduction: float = 0.35,
) -> tuple[float, str]:
```

Inputs  `accept_set` and `reject_set` are sets of strings that are meant to be accepted/rejected by a good answer.

The function will first check full equivalence between the submitted answer `student_regex` and the true correct solution `correct_regex`. If equivalent, full marks are given. Otherwie, the function will deduct `non_equivalence_deduction` of the question value and pro-rata the points based on the number of unit tests pased. This means that if all unit tests do pass, the points awarded will be `question_value * non_equivalence_deduction`, the most partial marks a submission can attract when found not fully correct via equivalence checking.

> [!IMPORTANT]
> The test case value can also be negative, so that passing the test case deducts marks. The feedback string is returned when the test case is failed if the value is positive, and when passed if negative.

### Submissions

Student submission solutions are also represented using functions:

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

Each function returns the student’s solution to the corresponding [question](#questions). All students should be distributed identical scripts containing pre-defined, empty functions as above.

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
    student_result, student_feedback = pytomata.library.another_library_function(
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

**Contact:** Prof. Sebastian Sardina (ssardina@gmail.com)]()