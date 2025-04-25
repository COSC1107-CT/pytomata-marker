"""An automarking system for Automata Theory and Formal Languages courses.

In some sense,it is a re-made in Python of the Java-based [JFLAP Automarker](https://github.com/COSC1107-CT/jflap-ct-automarker)

"""
__authors__ = "Harry Porter and Sebastian Sardina"
__version__ = "0.1.0"
__license__ = "MIT License"
import argparse
import pathlib

import pytomata


def main(args: argparse.Namespace) -> None:
    """Main automarking system with the arguments from CLI """
    return pytomata.calculate_and_output_student_results(
        args.questions_script_path,
        args.output_directory_path,
        args.student_solution_paths,
        process_count=args.process_count,
    )


def construct_and_parse_args():
    """CLI Command line interface"""
    parser = argparse.ArgumentParser(
        description="Pytomata automarking system for Automata Theory and Formal Languages courses",
        epilog="standard output is used for results and feedback by default",
    )
    parser.add_argument(
        "questions_script_path",
        help="path to script containing instructor-defined question functions",
        type=pathlib.Path,
        metavar="QUESTIONS",
    )
    parser.add_argument(
        "student_solution_paths",
        help="paths to scripts and directories containing student solutions",
        nargs="+",
        type=pathlib.Path,
        metavar="SOLUTIONS",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="directory for saving results and feedback",
        dest="output_directory_path",
        type=pathlib.Path,
        metavar="OUTPUT",
    )
    parser.add_argument(
        "-p",
        "--processes",
        help="specify processes to distribute solutions across",
        dest="process_count",
        type=int,
        default=1,
        metavar="PROCESSES",
    )
    parser.add_argument(
        "-q", "--quiet", help="suppress all output", action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = construct_and_parse_args()
    main(args)
