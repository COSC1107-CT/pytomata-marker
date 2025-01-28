# Pytomata Marker

<!-- TODO: Overview. -->

- [Pytomata Marker](#pytomata-marker)
    - [Technologies](#technologies)
    - [Usage](#usage)
        - [Questions](#questions)
            - [Library Functions](#library-functions)
        - [Solutions](#solutions)
        - [Configuration](#configuration)
        - [Execution](#execution)
            - [Options](#options)

## Technologies

| Technology                                       | Usage |
|:------------------------------------------------:|:------|
| [Automata](https://caleb531.github.io/automata/) |       |

## Usage

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
            "1.a.i",
            2,
            exercise_1_question_a_1,
            solutions.exercise_1_question_a_1_solution,
        ),
    ]
```

This function returns a sequence of tuples specifying the label, total value, question and solution functions for each question.
The functions should correspond to those defined by the [questions](#questions) and [solutions](#solutions) scripts, respectively.

### Execution

Once [configuration](#configuration) is finished, invoke the `execute.py` script.
Here, `questions.py` contains the instructor-defined [question](#questions) and [configuration](#configuration) functions,
and `student_solutions` is a directory containing the students' [solution](#solutions) scripts:

```
uv run execute.py questions.py student_solutions
```

Student solution scripts can also be specified individually, interspersed with directories:

```
uv run execute.py questions.py student_solutions extra_student_1.py extra_student_2.py
```

By default, all results are printed to standard output.

#### Options

To save each student's result to an individal file, use the `--output` or `-o` flag:

```
uv run execute.py questions.py student_solutions --output output_directory
```

Marking in parallel is also supported though the `--processes` or `-p` flag;
this distributes the student solutions evenly across three processes:

```
uv run execute.py questions.py student_solutions --processes 3
```