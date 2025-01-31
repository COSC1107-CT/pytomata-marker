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
  - [Development](#development)
    - [Writing Library Functions](#writing-library-functions)
      - [Configuring Default Penalties](#configuring-default-penalties)
    - [Style Considerations](#style-considerations)

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
If you don't already have a virtual environment to use, create one like this:

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
2. An arbitrary list of Python scripts and directories containing students' [solutions](#solutions).

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

To save each student's result to an individal file instead of printing to standard output, use the `--output` or `-o` flag:

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
    # Invoke library function.
    return student_result, student_feedback
```

Each question is a single function that accepts a student's solution and the total allocated marks,
then returns the student's result and any feedback, in that order.

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

This denotes the percentage deduction to the `question_value` when the student's submission is incorrect.
The default `incorrect_penalty` is one, indicating a 100% deduction.

#### Defining Additional Test Cases

Certain library functions also accept additional test cases.
Each test case represents an alternate (usually partially correct or incorrect) solution,
has an associated value and optional feedback.
The value denotes a percentage of the total `question_value`.

```
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

> [!WARNING]
> Additional test case values must fall between -1 and 1, inclusive.

After the student's submission is marked against the actual solution, it is checked against each test case.
If passed, the percentage allocated to that test case is added to the student's result.
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
    return "abc"

def exercise_1_question_a_2_solution():
    """ """
    return {}
```

Each function returns the student's solution to the corresponding [question](#questions).

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

This function returns a sequence of tuples specifying the label, total value, question and solution functions for each question.
The functions should correspond to those defined by the [questions](#questions) and [solutions](#solutions) scripts, respectively.

## Development

This section is intended for contributors.

### Writing Library Functions

<!-- TODO: Additional test cases intended behaviour? -->

Library functions adhere to a shared interface, so their usage and behaviour are consistent.

<!--
Library functions should all define a `question_value` and `incorrect_penalty` to denote the percentage deduction for incorrect solutions.
Defining `additional_test_cases` is not necessary; if it is defined, it should be optional.
These should always be [keyword-only arguments](https://peps.python.org/pep-3102/).
-->

```python
def another_library_function(*args, question_value, incorrect_penalty, additional_test_cases=None):
    # ...
    return student_result, student_feedback
```

Every library function returns the student's result and any feedback, in that order.
Once defined, import the function in the `lib/__init__.py` script.

#### Configuring Default Penalties

Default incorrectness penalties are applied using the `apply_penalty_values` decorator:

```python
import .configuration

@configuration.apply_penalty_values()
def another_library_function(*args, incorrect_penalty, additional_test_cases=None):
    pass
```

> Ensure the `apply_penalty_values` function is always **invoked** using parentheses. This returns the actual decorator function.

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

### Style Considerations

<!-- TODO: Ruff stuff. -->

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
