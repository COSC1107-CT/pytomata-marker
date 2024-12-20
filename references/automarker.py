""" Python Automarker System for Automata Assignments

This system allows the automarking of Prolog-based assignments.

It relies on Python's swiplserver package (https://pypi.org/project/swiplserver/)
to run SWI-Prolog (http://swi-prolog.org) within Python.

YAML files are used for automarking design and reports.

@author Sebastian Sardina, Andrew Chester
@contact sssardina@gmail.com
@year 2023-2024
@license Apache-2.0 license
"""

# grades student "logic.pl" submissions for the flight network assignment.
import sys
import argparse
import yaml  # pip install pyyaml (https://pynative.com/python-yaml/)
import traceback
import importlib.util
import os
import logging
import colorlog
from colorlog import ColoredFormatter

yaml.Dumper.ignore_aliases = (
    lambda *args: True
)  # avoid aliases in yaml output - weird behaviour!
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html

######## SETUP LOGGER
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG
LOGFORMAT = (
    "  %(log_color)s%(levelname)-4s%(reset)s | %(log_color)s%(message)s%(reset)s"
)
logging.root.setLevel(LOG_LEVEL)
formatter = colorlog.ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger("pythonConfig")
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)


MARKER_SCRIPT_PATH = Path(os.path.realpath(__file__)).parent
PATH_SUB = Path("submissions/")
PATH_REPORTS = Path("reports/")

# def get_new_prolog():
#     MQI = PrologMQI()
#     MQI.start()

#     PL = MQI.create_thread()
#     PL.start()

#     return PL


def filter_test_weights(question_weights: list, q_vars: dict, args_list: list) -> dict:
    """Function to filter the full list of question weights down to those necessary for this particular test case query.

    To facilitate partial matching of answers, each variable in the predicate is given a weight for how much it should be penalised for disagreeing with the expected answer.

    Different test case queries however will have different free variables - we must only take weights for free variables as ground arguments in queries are not returned by Prolog.

    Free query variables will start with a capital letter.

    Queries that are compound should be wrapped in a view under another single predicate.

    Args:
        question_weights (list): weights for each argument in query
        query (str): test case query

    Raises:
        ValueError: cannot parse arguments in query

    Returns:
        dict: mapping variable name in query to weight
    """
    q_vars_reversed = {v: k for k, v in q_vars.items()}

    if len(args_list) != len(question_weights):
        logger.warning(
            "mismatch between variables in Prolog query and question weights: no of arguments different from number of weights!"
        )

    # compute weights for each variable mentioned in the query
    weights_dict = {}
    for unground_vars, w in zip(args_list, question_weights):
        n = len(unground_vars)  # number of variables in this argument
        for v in unground_vars:
            if v == "_":  # ignore anonymous variables
                continue
            if v not in q_vars.keys():
                v = q_vars_reversed[v]

            if v in weights_dict.keys():
                weights_dict[v] = min(
                    1, weights_dict[v] + w / n
                )  # if a variable appears in multiple arguments, take the sum of their penalties (capped at 1).
            else:
                weights_dict[v] = w / n
    return weights_dict


def parse_text(text: str) -> list:
    """Generate a list of lists of variables from a prolog query string.

    Each list contains the variables in a single argument of the query.


    NOT USED NOW - Replaced by extract_vars_term/2 in Prolog
    """
    MAPPING = {"]": "[", ")": "("}
    variables = []
    variable = ""
    stack = []

    for char in text:
        variable += char

        if char in "([":
            stack.append(char)
        elif char in ")]":
            if stack[-1] == MAPPING[char]:
                stack.pop()
            else:
                raise ValueError(
                    "Unmatched parentheses in prolog query string while assigning variable weights"
                )
        elif char == ",":
            if (
                not stack
            ):  # only if the stack of brackets is empty do we count the comma as real
                variables.append(
                    variable[:-1]
                )  # ommit last character added as it will be the comma
                variable = ""

    variables.append(variable)

    return variables


def perform_partial_matching(answers, expected_answers, weights):
    """Performs partial matching of answers against expected answers.

    For each expected answer, take the provided answer that has the highest match score, and remove it from the of answers (leftover answers, to be checked against unsoundness).

    The score is the weighted number of correct answers obtained.
    If there are N expected correct answers and all of them are returned perfecly then score is N.
    Each fully correct answer counts as 1, and each partially correct answer counts as a fraction of 1, depending the weights per arguments.
    So, the maximum score is N = len(expected_answers)

    Args:
        answers (list(dict)): binding answers to query from the student
        expected_answers (list(dict)): list of correct binding answers to query
        weights (dict): weights for each variable in query

    Returns:
        tuple: total score(float), unmatched_answers (list), remaining answers(list), feedback(list)
    """
    total_score = 0
    remaining_answers = answers
    unmatched_answers = []
    partial_answers = []
    feedback = []
    for ea in expected_answers:
        best_match = None
        best_score = 0
        for a in remaining_answers:
            score = calculate_matching_score(a, ea, weights)
            if score > best_score:
                best_score = score
                best_match = a

        if best_score > 0:
            remaining_answers.remove(best_match)
            total_score += best_score
            if best_score < 1:
                # we have a match, but it is partial. Give some feedback
                partial_answers.append((ea, best_match, best_score))
        else:
            unmatched_answers.append(ea)

    return total_score, unmatched_answers, partial_answers, remaining_answers


def calculate_matching_score(answer, expected_answer, weights):
    match = 1
    for v, w in weights.items():
        # allow for some descrepancy due to fp arithmetic
        if type(expected_answer[v]) == float:
            try:
                if abs(answer[v] - expected_answer[v]) > pow(10, -1 * FLOAT_PRECISION):
                    match -= w
            except TypeError as e:
                logger.debug(
                    "Student answer contained non-numeric variable where numeric was expected"
                )
                match -= w
        else:
            if answer[v] != expected_answer[v]:
                match -= w

    return round(max(0, match), 2)


def calculate_points(id, answers, expected_answers, weights, total_points):
    """Calculate the points earned in a SINGLE test case based on the answers given by the student and the expected answers based on:

        - How complete the answers are (this considers partial correctness via weights on arguments)
        - Are there wrong solutions given, unsound ones
        - Are there duplicates in answers (i.e. the same answer given more than once)

    The WEIGHTS are used to judge the level of correctness of an answer, by weighting each
    argument. For example a weight [1, .5, .2] says that:
        - First argument wrong has full deduction, no points if wrong
        - Second argument wrong has 50% deduction if wrong
        - THird argument wrong has 20% deduction if wrong

    Args:
        id (str): id of the test case (as per YAML)
        answers (list/bool): answer or answers of student code
        expected_answers (list/bool): answer or answers expected (correct)
        weights (list): weights for correctness
        total_points (int): total points available for this test case

    Returns:
        points_earned (float): points or % earned/lost for the test case (out of total_points)
        feedback (list(str)): feedback for the test case
    """

    logger.debug(
        f"\t\tCalculating points for test {id}. Expected answers: {expected_answers} ({type(expected_answers)}). Student answers: {answers} ({type(answers)})"
    )

    if total_points >= 0:  # this is a positive-based test case
        points_available = total_points
        points_penalty = 0
    else:  # this is a penalty-based test case
        points_available = 0
        points_penalty = total_points

    points_earned = 0
    feedback = []

    # NOTE: We assume that expected correct answer will never be a duplicate boolean value: i.e. [True, True].
    # CASE 1: we are expecting a single boolean
    if type(expected_answers) == bool:
        # 1a: If answer is indeed a Boolean True/False we can compare directly
        if type(answers) == bool:
            if answers == expected_answers:  # full marks
                return points_available, [
                    feedback_test(id, f"Correct answer! :-)", points_available)
                ]
            else:  # wrong answer, full penalty If any)
                return points_penalty, [
                    feedback_test(
                        id, f"Incorrect answer (wrong bool answer)", points_penalty
                    )
                ]
        # 1b: If answers is a list, student may have returned redundant boolean results of the form
        # [True, True, True, True] (can never have any False) OR disagree in boolean
        elif type(answers) == list and answers == [expected_answers] * len(answers):
            return (1 - W_REDUNDANT) * points_available, [
                feedback_test(
                    id,
                    f"Correct answer with duplication ",
                    (1 - W_REDUNDANT) * points_available,
                )
            ]
        else:  # either we expected False and we got answers; or expected True and got
            return points_penalty, [
                feedback_test(
                    id, f"Incorrect answer (wrong bool list answer)", points_penalty
                )
            ]
    # CASE 2: we are expecting a list of successes (possibly with bindings)
    else:
        if type(answers) == bool:
            return points_penalty, [
                feedback_test(
                    id,
                    f"Incorrect answer (expected list but gave bool answer)",
                    points_penalty,
                )
            ]

    assert type(answers) == list
    assert type(expected_answers) == list

    # we want to remove duplicates to check for redundancy (can't use a set because not hashable):
    deduped_expected_answers = []
    for a in expected_answers:
        if a not in deduped_expected_answers:
            deduped_expected_answers.append(a)

    deduped_answers = []
    for a in answers:
        if a not in deduped_answers:
            deduped_answers.append(a)

    # we consider you to have redundancy if the number of duplicates exceeds that in the expected answers
    # need to do this comparison here because deduped answers list modified in below code.
    redundancy = False
    student_duplicates = len(answers) - len(deduped_answers)
    expected_duplicates = len(expected_answers) - len(deduped_expected_answers)
    if student_duplicates > expected_duplicates:
        redundancy = True

    # check completeness of answers
    # 90% of points available if all expected solutions are there
    # no_correct may be less than len(expected_answers) due to partial correctness
    no_correct, unmatched_answers, partial_answers, remaining_answers = (
        perform_partial_matching(deduped_answers, deduped_expected_answers, weights)
    )
    recall = no_correct / len(deduped_expected_answers)
    points_penalty = recall * points_available * W_COMPLETENESS  # points to add
    points_earned += points_penalty
    feedback.append(
        feedback_test(
            id,
            f"Completeness: {no_correct}/{len(deduped_expected_answers)}",
            points_penalty,
        )
    )

    # feedback += match_feedback    # do not add it to feedback, just report in in log
    for a in unmatched_answers:
        logger.info(f"\t\t\tMissing matched answer: {a}")
    for a in partial_answers:
        logger.info(
            f"\t\t\tPartial match for expected answer {a[0]} ({a[2]} score): {a[1]}"
        )

    # give 10% if no redundant answers given
    if recall == 0:
        feedback.append(
            feedback_test(
                id, f"No correct answers given, not eligible for redundancy marks", 0
            )
        )
    elif not redundancy:
        points_penalty = points_available * W_REDUNDANT  # points to add
        points_earned += points_penalty
        feedback.append(
            feedback_test(id, f"No redundant answers found! :-)", points_penalty)
        )
    else:
        feedback.append(feedback_test(id, f"Redundant answers found...", 0))

    # check soundness of solutions
    # if wrong solution found, then 1/3 of points obtained
    if len(remaining_answers) > 0:
        for a in remaining_answers:
            logger.info(f"\t\t\tIncorrect answers found: {a}")
        points_penalty = -(points_earned * W_INCORRECT)
        points_earned += points_penalty
        feedback.append(
            feedback_test(
                id,
                f"Incorrect answers found... (e.g., {remaining_answers[0]}) :-( )",
                points_penalty,
            )
        )

    # clip mark to positive
    points_earned = max(0, points_earned)

    return points_earned, feedback


def load_prereq(pl: PrologThread, setup_file, student_file, prereq_mode="none"):
    """Load pre-req tools for automarker, like

        - consult tools.pl (e.g., own consulting service with exception)
        - consult setup file setup_file (e.g., setup_e3.pl) (domain independent)
        - query automarker_setup(student_file, prereq_mode) (domain dependent)
            this should load the student file and any pre-requisite files needed (domain dependent)

    prereq_mode states mode to load pre-requisite files:
        none: simply call automarker_setup/1
        true: call automarker_setup/2 with true
        false: call automarker_setup/2 with false
    """
    setup_path = PATH_TEST_DIR / setup_file
    tools_path = MARKER_SCRIPT_PATH / "tools.pl"
    pl.query(f'consult("{tools_path.as_posix()}")')  # load tools always
    pl.query(f'consult("{setup_path.as_posix()}")')
    if prereq_mode == "none":
        pl.query(f'automarker_setup("{student_file.as_posix()}")')
    else:
        pl.query(f'automarker_setup("{student_file.as_posix()}", {prereq_mode})')


def generate_correct_answers():
    # load test suite
    test_suite = yaml.load(PATH_TESTS.read_text(), Loader=yaml.FullLoader)

    for q in test_suite:  # this loops modifies test_suite object; adds answers!
        logger.debug(f"Loading test {q}")
        q_points = 0
        q_bonus = 0
        tests = test_suite[q]["tests"]
        setup_file = test_suite[q].get("setup", "setup.pl")
        sol_file = test_suite[q].get("student_file", DEFAULT_SUBMISSION_FILE)
        path_sol_file = PATH_SOL / sol_file

        logger.info(f"Generating solutions for question: {q}")
        logger.info(f"\t Setup file: {setup_file}")
        logger.info(f"\t Solution file: {path_sol_file}")
        with PrologMQI() as mqi:
            with mqi.create_thread() as pl:
                # Consult required files for each question
                # note this should never throw an exception, as it is the solution file consults well!
                load_prereq(pl, setup_file, path_sol_file)

                for t in tests:
                    logger.info(f"\t Generating solution for test {t['id']}")

                    t_query = t["query"]
                    if t["points"] > 0:  # not negative penalty point test case
                        if not t.get("bonus", False):
                            q_points += t["points"]
                        else:
                            q_bonus += t["points"]
                    # DO THE ACTUAL QUERY!
                    # We do not use timeout as it is the "perfect" solutions, it should work well!
                    try:
                        answer = pl.query(t_query)
                    except PrologError as e:
                        logger.error(
                            f"Error in query when building answers: {t_query} \n\t\t {e}"
                        )
                        exit(1)

                    t["answer"] = answer
                # add total points to test question
                test_suite[q]["points"] = q_points
                # add total bonus points to test question
                test_suite[q]["bonus"] = q_bonus

    # write tests with answers to file (for human validation)
    Path(PATH_ANSWERS).write_text(yaml.dump(test_suite, sort_keys=False))
    logger.debug(f"... done generating OK answers for tests: {PATH_TESTS}\n")

    return test_suite


def feedback_test(id, message, points=0, total_points=None):
    """Build the final feedback summary string for a test:
    For example:

        'Test 6: [14.00/14.00] - Final points collected'
        'Test 8: [7.00/7.00] - Final points collected (BONUS)'
        'Test 12: [0%/-10%] - Final points collected'
    """
    denominator = ""
    percentage_penalty = False
    if total_points is not None:
        # build denominator if needed in some cases
        if total_points < 0 and total_points > -1:
            percentage_penalty = True
            denominator = f"/{total_points:.0%}"
        else:
            denominator = f"/{total_points:.2f}"

    if percentage_penalty:
        # it's a penalty question, so we should display as percentage
        return f"Test {id}: [{points:.0%}{denominator}] - {message}"
    else:
        # standard question, so give points as decimal.
        return f"Test {id}: [{points:.2f}{denominator}] - {message}"


def mark_student(path_student, test_suite):
    sid = path_student.name
    report = {"id": sid, "question": {}}

    # now run each question in suite (e.g., route)
    for q in test_suite:
        logger.info(f"Start marking question: {q}")

        # get details of test case for question q
        q_value = test_suite[q]["marks"]
        q_tests = test_suite[q]["tests"]
        q_desc = test_suite[q]["desc"]
        setup_file = test_suite[q].get("setup", "setup.pl")
        student_file = test_suite[q].get("student_file", DEFAULT_SUBMISSION_FILE)
        q_weights = test_suite[q].get("correctness_weights", [])
        q_marks = q_value / sum(
            [
                test["points"]
                for test in q_tests
                if test["points"] > 0 and not test.get("bonus", False)
            ]
        )
        path_stud_file = path_student / student_file
        q_prereq = test_suite[q].get("prerequisites", "none")
        prerequisite_modes = []

        # prerequisite_modes is a list of modes to run the question in: none, true, false
        if q_prereq == "none":
            prerequisite_modes.append("none")
        if q_prereq in ("ours", "both"):
            prerequisite_modes.append("false")
        if q_prereq in ("theirs", "both"):
            prerequisite_modes.append("true")

        q_points = {}
        q_frac_penalty = {}
        q_feedback = {}
        # we run the test set for each mode (both, us, theirs, none) and keep the best result
        for mode in prerequisite_modes:
            logger.info(
                f"Marking question {q} with pre-requisite replacement mode: {mode}"
            )

            # track collected points, frac penalties, and feedback
            q_points[mode] = 0
            q_frac_penalty[mode] = 0
            q_feedback[mode] = []

            with PrologMQI() as mqi:
                with mqi.create_thread() as pl:
                    # Consult required files for marking student code
                    # Up to IDM23, we used to handle consult errors via throw exception
                    # to Python. But this will not work as nothing after the error
                    # will be consulted (e.g., pre-reqs). So we change to leave
                    # error_happened/1 fact and we check if there is some error
                    # we now just use consult/1 and check for error_happened/1
                    try:
                        load_prereq(pl, setup_file, path_stud_file, mode)
                        error = pl.query("error_happened(E)")  # load tools always
                        if error:
                            feedback = f"Solution file consulted with error (this should never happen): {error[0]['E']}"
                            logger.error(feedback)
                            q_feedback[mode].append(feedback)
                    except PrologError as e:
                        # From AI24 this should never happen, as we are using error_happened/1
                        # eventually needs to be removed
                        logger.error(f"Error consulting student file system: {e}")
                        print(traceback.print_exc())
                        exit(1)

                    # next, run each test in question
                    points_available = 0  # for the whole question/test section
                    bonus_available = 0
                    for i, test in enumerate(q_tests):

                        # load test information
                        test_id = test["id"]
                        query = test["query"]
                        test_points = test["points"]
                        test_bonus = test.get("bonus", False)
                        expected_answer = test["answer"]
                        test_feedback = [
                            f"Test {test_id}: {test.get('description','')}"
                        ]
                        if test_points > 0:
                            if test_bonus:
                                bonus_available += test_points
                            else:
                                points_available += test_points

                        # TODO: document this piece of code.
                        # This was a way to correctly extract the free variables of a query and match them with the spec test and weights
                        ARGS_LIST = "ArgsList"  # this is just a placeholder variable, can be anything that does not clash with a test case.
                        q_vars = pl.query(
                            f"extract_vars_term({query}, {ARGS_LIST})",
                            query_timeout_seconds=QUERY_TIMEOUT,
                        )[0]
                        args_list = q_vars.pop(ARGS_LIST)
                        test_weights = filter_test_weights(q_weights, q_vars, args_list)

                        logger.info(
                            f"\t Testing case {test_id} for question {q} ({test_points} points)"
                        )

                        # query submission logic and calculate mark while catching prolog errors
                        try:
                            # RUN QUERY ON STUDENT CODE!
                            pl.query("retractall(forbidden)")
                            stud_answer = pl.query(
                                query, query_timeout_seconds=QUERY_TIMEOUT
                            )
                            logger.debug("Finished query against submission!")
                            forbidden = pl.query("forbidden(M)")
                            if forbidden:
                                pred_forbidden = set([x["M"] for x in forbidden])
                                raise Exception(
                                    f"A forbidden predicate has been used: {pred_forbidden}"
                                )

                            points, feedback = calculate_points(
                                test_id,
                                stud_answer,
                                expected_answer,
                                test_weights,
                                test_points,
                            )

                        except Exception as e:
                            points = min(0, test_points)
                            logger.info(f"\t\t EXCEPTION!!: {e}")
                            feedback = [
                                feedback_test(
                                    test_id,
                                    f"Test failed due to exception: {e}",
                                    points,
                                )
                            ]

                        test_feedback = test_feedback + feedback
                        # if points in (-1, 0) then it is a % penalty (on student final score!).
                        #   if so, store those % penalties for later application as + numbers
                        if points < 0 and points > -1:
                            q_frac_penalty[mode] += -points
                        else:
                            q_points[mode] += points

                        q_feedback[mode] = q_feedback[mode] + test_feedback
                        final_point_string = "Final points collected"
                        if test_bonus:
                            final_point_string += " (BONUS)"
                        q_feedback[mode].append(
                            feedback_test(
                                test_id, final_point_string, points, test_points
                            )
                        )

            # round question mark to 2dp and prevent going below 0
            q_points[mode] = max(round(q_points[mode], 2), 0)

            # now apply fractional penalty collected on final student score
            #   we take the min in case we have collected penalty > 1 (100%)
            q_points[mode] = q_points[mode] * (1 - min(q_frac_penalty[mode], 1))

        q_points_best = -1  # to make sure first time is always better!
        best_mode = "none"
        for mode in prerequisite_modes:
            if q_points[mode] > q_points_best:
                q_points_best = q_points[mode]
                q_feedback_best = q_feedback[mode]
                best_mode = {"true": "our", "false": "your", "none": "your"}[mode]

        # update student report for question q
        report["question"][q] = {}
        report["question"][q]["desc"] = q_desc
        report["question"][q]["points"] = q_points_best
        report["question"][q]["points_available"] = points_available
        report["question"][q]["bonus_available"] = bonus_available
        report["question"][q]["marks"] = round(q_points_best * q_marks, 2)
        report["question"][q]["marks_available"] = q_value
        if q_prereq == "both":
            report["question"][q][
                "best_mode"
            ] = f"You scored the most points when we ran your code with {best_mode} implementations for prior questions, so all results for this question are using {best_mode} implementations."
        report["question"][q]["feedback"] = q_feedback_best

    # calc total score for the whole assignment report
    report["marks"] = round(
        sum([report["question"][q]["marks"] for q in report["question"]]), 2
    )

    # write report to file
    logger.info(f"Writing report for submission {sid}...")
    PATH_REPORTS.mkdir(exist_ok=True)
    (PATH_REPORTS / f"{sid}.yaml").write_text(yaml.dump(report, sort_keys=False))


def main(args):
    # STEP 1 - GENERATE EXPECTED ANSWERS TO TESTS:
    # generate expected answers to tests using solution files
    # and write the test suite to file with answers included.
    if PATH_ANSWERS.exists():
        logger.info("Reading perfect solutions")
        test_suite = yaml.load(PATH_ANSWERS.read_text(), Loader=yaml.FullLoader)

    # STEP 2 - RUN TESTS ON STUDENT SUBMISSIONS:
    # remove students that already have a report if not in remark mode
    if not args.remark:
        for path_student in PATH_SUB_STUDENTS.copy():
            report_file = PATH_REPORTS / path_student.with_suffix(".yaml").name
            if report_file.exists():
                logger.info(f"Skipping student (report exists): {path_student.name}")
                PATH_SUB_STUDENTS.remove(path_student)

    no_mark = len(PATH_SUB_STUDENTS)
    logger.info(f"Start marking {no_mark} student submissions")
    for i, path_student in enumerate(PATH_SUB_STUDENTS):
        report_file = PATH_REPORTS / path_student.with_suffix(".yaml").name
        logger.info(
            f"############################ MARKING STUDENT {i+1}/{no_mark}: {path_student.name} ############################"
        )
        mark_student(path_student, test_suite)
    logger.info("Done marking submissions...")


# PATH_SUB = Path("submissions/")
# PATH_REPORTS = Path("reports/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automarker System for Automata Projects"
    )
    parser.add_argument(
        "CONFIG_FILE",
        help="Specify the configuration file to be used",
    )
    parser.add_argument(
        "--gensol", action="store_true", help="Regenerate solution answer file"
    )
    parser.add_argument(
        "--remark",
        action="store_true",
        default=False,
        help="Mark students even if their report already exist (Default: %(default)s)",
    )
    parser.add_argument(
        "--students",
        nargs="+",
        metavar="<list names>",
        default=None,
        help="Restrict to specified submissions",
    )
    parser.add_argument(
        "--submissions",
        metavar="<path>",
        default=PATH_SUB,
        help="Folder where submissions are placed (Default: %(default)s)",
    )
    parser.add_argument(
        "--reports",
        metavar="<path>",
        default=PATH_REPORTS,
        help="Folder to place reports (Default: %(default)s)",
    )
    args = parser.parse_args()

    # Load configuration file with all GLOBAL variables
    # Load the module from the given path
    # https://medium.com/@Doug-Creates/dynamically-import-a-module-by-full-path-in-python-bbdf4815153e
    spec = importlib.util.spec_from_file_location("module_name", args.CONFIG_FILE)
    module_feedback = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module_feedback)
    # Add the module to sys.modules
    sys.modules["module_name"] = module_feedback

    QUERY_TIMEOUT = getattr(module_feedback, "QUERY_TIMEOUT")
    PATH_TEST_DIR = getattr(module_feedback, "PATH_TEST_DIR")
    PATH_TESTS = getattr(module_feedback, "PATH_TESTS")
    PATH_ANSWERS = getattr(module_feedback, "PATH_ANSWERS")
    PATH_SOL = getattr(module_feedback, "PATH_SOL")
    PATH_SUB = getattr(module_feedback, "PATH_SUB")
    DEFAULT_SUBMISSION_FILE = getattr(module_feedback, "DEFAULT_SUBMISSION_FILE")
    PATH_REPORTS = getattr(module_feedback, "PATH_REPORTS")
    PATH_SOL = getattr(module_feedback, "PATH_SOL")
    W_REDUNDANT = getattr(module_feedback, "W_REDUNDANT")
    W_COMPLETENESS = getattr(module_feedback, "W_COMPLETENESS")
    W_INCORRECT = getattr(module_feedback, "W_INCORRECT")
    FLOAT_PRECISION = getattr(module_feedback, "FLOAT_PRECISION")

    if args.gensol:
        logger.info(f"Generating correct answer from perfect solution...")
        logger.info(f"Using perfect solution at: {PATH_SOL}")
        logger.info(f"Tests as defined at: {PATH_TESTS}")
        logger.info(f"Saving test answers at: {PATH_ANSWERS}")

        test_suite = generate_correct_answers()
        logger.info("Done generating perfect solutions...")
        exit(0)

    if args.reports:
        PATH_REPORTS = Path(args.reports)
    if not PATH_REPORTS.exists():
        os.mkdir(PATH_REPORTS)
        logger.error(f"Folder '{PATH_REPORTS}' does not exist. Creating it...")

    if args.submissions:
        PATH_SUB = Path(args.submissions)
    PATH_SUB_STUDENTS = [path for path in PATH_SUB.iterdir() if path.is_dir()]

    if args.students:  # filter students to those provided
        PATH_SUB_STUDENTS = [
            path for path in PATH_SUB_STUDENTS if path.name in args.students
        ]

    main(args)
