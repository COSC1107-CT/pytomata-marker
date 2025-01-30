# Pytomata Marker

<!-- TODO: Overview. -->

- [Pytomata Marker](#pytomata-marker)
  - [Install \& setup](#install--setup)
      - [Manual Project Configuration](#manual-project-configuration)
  - [Usage](#usage)
  - [Design and configuration of assessment](#design-and-configuration-of-assessment)
    - [Questions](#questions)
      - [Library Functions](#library-functions)
      - [Additional Test Cases](#additional-test-cases)
    - [Solutions](#solutions)
    - [Configuration](#configuration)
    - [Options](#options)
  - [Development](#development)
    - [Adding Library Functions](#adding-library-functions)
      - [Configuring Default Penalties](#configuring-default-penalties)
    - [Style Considerations](#style-considerations)

## Install & setup

| Technology                                       | Usage |
|:------------------------------------------------:|:------|
| [Automata](https://caleb531.github.io/automata/) | automata library      |
| [uv](https://docs.astral.sh/uv/)                 | project dependencies      |

This project has been configured using uv to handle dependencies, etc. Executing `uv run` downloads the dependencies in `pyproject.toml` and the correct Python version if necessary before running the script 🤗

#### Manual Project Configuration

Manual project configuration, without `uv`, can still be done using [venv](https://docs.python.org/3/library/venv.html).

If you would prefer to avoid using [uv](tps://docs.astral.sh/uv/), create first a new virtual environment (here at `~/.pyauto`) if you don't have one that want to use:

```shell
$ python3 -m venv ~/.pyauto
```

Make sure it is active:

```shell
$ source ~..pyauto/bin/activate
```

> [!WARNING]
> Use the correct shell-specific `activate` script:
>
> `activate.fish` for [fish](https://fishshell.com), `activate.ps1` for PowerShell, etc.

Install the required dependencies:

```shell
$ pip install -r requirements.txt
```

Once finished, use `python` instead of `uv run` in the [execution instructions](#execution).

## Usage

Once [configuration](#configuration) is finished, invoke the `execute.py` script with the file containing the instructor-defined [question](#questions) and [configuration](#configuration) functions, and directory containing the students' [solution](#solutions) scripts:

```shell
$ uv run execute.py questions.py student_solutions_dir
```

Student solution scripts can also be specified individually, interspersed with directories:

```shell
$ uv run execute.py questions.py student_solutions extra_student_1.py extra_student_2.py
```

By default, all results are printed to standard output.

If you did not install [uv](tps://docs.astral.sh/uv/), use `python` instead of `uv run`.

## Design and configuration of assessment

### Questions

Questions are defined using functions:

```python
def exercise_1_question_a_1(student_solution, question_value):
    actual_solution = {}
    # ...
    return student_result, student_feedback
```

All question functions should return the student's result and any feedback, as above.

<!-- TODO: Additional test cases. -->

#### Library Functions

<!-- TODO: Overview. Table, eventually? -->

#### Additional Test Cases

### Solutions

Student solutions are also represented using functions:

```python
def exercise_1_question_a_1_solution():
    """ """
    return {}

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

### Options

To save each student's result to an individal file, use the `--output` or `-o` flag:

```shell
$ uv run execute.py questions.py student_solutions --output output_directory
```

Marking in parallel is also supported though the `--processes` or `-p` flag;
this distributes the student solutions evenly across three processes:

```shell
$ uv run execute.py questions.py student_solutions --processes 3
```

## Development

This section is intended for contributors.

### Adding Library Functions

<!-- TODO: Additional test cases intended behaviour? -->

Library functions should all define a `question_value` and `incorrect_penalty` to denote the percentage deduction for incorrect solutions.
Defining `additional_test_cases` is not necessary; if it is defined, it should be optional.
These should always be [keyword-only arguments](https://peps.python.org/pep-3102/).

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
    _ = _auxiliary_library_function()
    return student_result, student_feedback

def _auxiliary_library_function():
    pass
```
