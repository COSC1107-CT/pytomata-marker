# Pytomata Marker

This is an automarker developed to support assignments in theory of computation courses @ RMIT University.

It is a re-development of the [JFLAP Automarker](https://github.com/COSC1107-CT/jflap-ct-automarker) system, but done in Python and heavily relying on [Automata](https://caleb531.github.io/automata/) library, which provides regular expression and automata APIs.

Official GitHub repo: https://github.com/COSC1107-CT/pytomata-marker

- [Pytomata Marker](#pytomata-marker)
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
  - [Contributors](#contributors)

> [!TIP]
> This readme is for usage of the system. If you want to develop on it, refer to [DEVELOP.md](DEVELOP.md).

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

Student submission answers are also done using functions. Check [`tests/ct19/s0000000.py`](tests/ct19/s0000000.py) for an example of a perfect submission for the CT19 example.

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
> Student submission files **should not alter** the function signature of the functions. Doing so will result in the function not being found by the automarker and will attract zero points automatically.

Each function returns the student’s solution to the corresponding [question](#questions). All students should be distributed identical scripts containing pre-defined, empty functions as above.

## Library Function Catalogue

In the table we use $\hat{\cdot}$ to denote the student submission:

| Function                                                | Behaviour                                                                                              |
|:--------------------------------------------------------|:-------------------------------------------------------------------------------------------------------|
| `check_regex_correctness` | check a regular expression correctness ($L(\hat{R}) = L(R)$)
| `check_regex_acceptance` | check a set of strings fits a regular expression ($\hat{w} \in L(R)$)
| `check_regex_intersection_acceptance` | check a set of strings fits the itnersection of a list of regular expressions ($L(\hat{w}) \in L(R_1) \cap L(R_2)$)
| `check_regex_difference_acceptance` | check a set of strings is in the difference of two regular expressions ($L(\hat{w}) \in L(R_1) - L(R_2)$)
| `check_dfa_correctness` | check a DFA correctness ($L(\hat{M}) = L(M)$)

## Contributors

The pytomata automarker was developed by Harry Porter and Sebastian Sardina in 2025, based on the [JFLAP Automarker](https://github.com/COSC1107-CT/jflap-ct-automarker) system.

**Contact:** Prof. Sebastian Sardina (ssardina@gmail.com)]()