# Pytomata Marker

<!-- TODO: Overview. -->

- [Pytomata Marker](#pytomata-marker)
  - [Installation \& Setup](#installation--setup)
      - [Manual Project Configuration](#manual-project-configuration)
  - [Usage](#usage)
      - [Execution Options](#execution-options)
  - [Assessment Design \& Configuration](#assessment-design--configuration)
    - [Questions](#questions)
      - [Using Library Functions](#using-library-functions)
      - [Defining Additional Test Cases](#defining-additional-test-cases)
    - [Solutions](#solutions)
    - [Configuration](#configuration)
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

## Installation & Setup

<!-- TODO: Add Graphviz? -->

| Technology                                       | Usage                                          |
|:------------------------------------------------:|:-----------------------------------------------|
| [Automata](https://caleb531.github.io/automata/) | Provides regular expression and automata APIs  |
| [uv](https://docs.astral.sh/uv/)                 | Manages project dependencies and configuration |
| [Ruff](https://docs.astral.sh/ruff/)             | Source code linting and formatting             |

This project has been configured using uv to handle dependencies, etc.
To use uv, ensure it is [installed](https://docs.astral.sh/uv/getting-started/installation/), clone this repository, and proceed through the [usage instructions](#usage).
Otherwise, proceed through the next section.

### Manual Project Configuration

If you would prefer to avoid using uv, project configuration can still be done using [venv](https://docs.python.org/3/library/venv.html).
If you don’t already have a virtual environment to use, create one like this:

```shell
$ python3 -m venv ~/.pyauto
```

> [!NOTE]
> You can create your virtual environment under any directory.
> Here, the location is `~/.pyauto`; an alternative could be `.venv`.

Then, ensure the virtual environment is active; replace `~/.pyauto` with the location of your virtual environment:

```shell
$ source ~/.pyauto/bin/activate
```

> [!WARNING]
> Use the correct shell-specific `activate` script:
> `activate.fish` for [fish](https://fishshell.com), `activate.ps1` for PowerShell, etc.

Once activated, install the required dependencies:

```shell
$ pip install -r requirements.txt
```

Then, use `python` instead of `uv run` in the [execution instructions](#execution).

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

The procedure is run by the `execute.py` script, which accepts:

1. A Python script containing the instructor-defined [question](#questions) and [configuration](#configuration) functions;
2. An arbitrary list of Python scripts and directories containing students’ [solutions](#solutions).

> For assistance, use `uv run execute.py -h`.

Therefore, to process an individual submission:

```shell
$ uv run execute.py tests/questions.py tests/s0000000.py
```

```plaintext
Using CPython 3.13.1
Creating virtual environment at: .venv
Installed 6 packages in 4ms

*** s0000000 ***

1.a.i | 100 / 100
Correct!
```

> [!NOTE]
> Notice that `uv run` identified an already-installed interpreter, identified and downloaded the required dependencies before running the `execute.py` script.
> Output like this will only occur once, upon first invoking a script; refer to the [uv docs](https://docs.astral.sh/uv/) for details.

When a directory is supplied, all Python scripts inside that directory (non-recursively) are treated as student submissions:

```shell
$ uv run execute.py tests/questions.py tests/submissions
```

```plaintext
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
$ uv run execute.py tests/questions.py tests/submissions --output output_directory
```

Marking in parallel is also supported though the `--processes` or `-p` flag;
this distributes the student solutions evenly across three processes:

```shell
$ uv run execute.py tests/questions.py tests/submissions --processes 3
```

## Assessment Design & Configuration

This section details the definition of questions by an instructor,
the submission of solutions by students,
and the configuration necessary to match submissions against the correct marking function.
Both question and submission functions are intended to make heavy use of the [Automata](https://caleb531.github.io/automata/) library.

### Questions

Questions are defined using functions:

```python
import automata

def exercise_1_question_a_1(student_solution, question_value):
    actual_solution = {}
    # Invoke library function here.
    return student_result, student_feedback
```

Each question is a single function that accepts a student’s solution and the total allocated marks,
then returns the student’s result and any feedback, in that order.

#### Using Library Functions

Library functions are provided to handle certain archetypal questions.
These functions all return the student result and feedback, just like question functions; the result is always rounded to the nearest integer.

```python
import pytomata.lib

student_result, student_feedback = pytomata.lib.library_function(
    student_solution, actual_solution, question_value=question_value
)
```

The `question_value` is a required keyword argument.
An `incorrect_penalty` can also be optionally supplied:

```python
student_result, student_feedback = pytomata.lib.library_function(
    student_solution,
    actual_solution,
    question_value=question_value,
    incorrect_penalty=0.8,
)
```

> [!WARNING]
> The `incorrect_penalty` value must fall between 0 and 1, inclusive.

This denotes the percentage deduction from the `question_value` when the student’s submission is incorrect.
The default `incorrect_penalty` is 1, indicating a 100% deduction; the example above specifies an 80% deduction.

Refer to the [library function catalogue](#library-function-catalogue) for an overview of available functions.

#### Defining Additional Test Cases

Certain library functions also accept additional test cases.
Each test case represents an alternate (usually partially correct or incorrect) solution, containing:

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

### Configuration

The [question](#questions) script should contain a `construct_questions_and_solutions` function, like this:

```python
def construct_questions_and_solutions(solutions):
    return [
        (
            "1.a.i",
            2,
            exercise_1_question_a_1,
            solutions.exercise_1_question_a_1_solution,
        ),
        (
            "1.a.ii",
            2,
            exercise_1_question_a_2,
            solutions.exercise_1_question_a_2_solution,
        ),
    ]
```

> [!WARNING]
> This function must be called `construct_questions_and_solutions` and define one parameter,
> used internally to pass an individual student module.
> This facilitates pairing each student’s submissions against the same respective marking functions.

This function returns a sequence of tuples specifying the label, total value, question and solution functions for each question.
The functions should correspond to those defined by the [questions](#questions) and [solutions](#solutions) scripts, respectively.

Once this function is defined, refer to the [execution instructions](#usage).

## Library Function Catalogue

<!-- TODO: Table containing all available functions and their behaviour. -->

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
    # ...
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
    # ...
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
    # ...
    if not solution_is_correct:
        student_result = base.penalise_score(question_value, incorrect_penalty)
```

<!-- TODO: Handling additional test cases. -->
See [the following section](#handling-additional-test-cases) for further usage details.

Finally, once the solution and test cases have been checked, use `calculate_final_score` to finalise the student’s result:

```python
import base

def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):
    student_result = question_value
    # ...
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
        # ...
        if test_case_passed:
            return True
        return False

    student_result = question_value
    student_feedback = []
    # ...
    if additional_test_cases:
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

If the `test_case_handler_function` defines additional parameters,
these should be passed as further positional and keyword arguments to `run_additional_test_cases` as follows:

```python
def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):
    # ...
    if additional_test_cases:
        student_result, test_case_feedback = base.run_additional_test_cases(
            additional_test_cases,
            test_case_handler_function,
            student_result,
            question_value,
            arg_1,
            arg_2,
            keyword_para=arg_3,
        )


def test_case_handler_function(test_case, para_1, para_2, *, keyword_para):
    # ...
```

#### Documenting Library Functions

All library functions should include a docstring describing the:

<!-- TODO: Finish and provide an e.g. including test cases. -->

### Style Considerations

#### Linting & Formatting

All source code should be linted and formatted using [Ruff](https://docs.astral.sh/ruff/):

```shell
uv run ruff check
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
    # ...
    return student_result, student_feedback

def _auxiliary_library_function():
    pass
```
