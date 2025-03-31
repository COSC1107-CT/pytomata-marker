""" """

import pytomata


def handle_script_invocation():
    """ """
    args = construct_and_parse_args()
    return pytomata.calculate_and_output_student_results(
        args.questions_script_path,
        args.output_directory_path,
        args.student_solution_paths,
        process_count=args.process_count,
    )


def construct_and_parse_args():
    """ """
    args = {
        "description": "",
        "epilog": "standard output is used for results and feedback by default",
        "allow_abbrev": False,
    }
    parser = argparse.ArgumentParser(**args)
    args = {
        ("questions_script_path",): {
            "help": "path to script containing instructor-defined question functions",
            "type": pathlib.Path,
            "metavar": "QUESTIONS",
        },
        ("student_solution_paths",): {
            "help": "paths to scripts and directories containing student solutions",
            "nargs": "+",
            "type": pathlib.Path,
            "metavar": "SOLUTIONS",
        },
        ("-o", "--output"): {
            "help": "directory for saving results and feedback",
            "dest": "output_directory_path",
            "type": pathlib.Path,
            "metavar": "OUTPUT",
        },
        ("-p", "--processes"): {
            "help": "specify processes to distribute solutions across",
            "dest": "process_count",
            "type": int,
            "default": 1,
            "metavar": "PROCESSES",
        },
    }
    for values, config in args.items():
        parser.add_argument(*values, **config)
    return parser.parse_args()


if __name__ == "__main__":
    handle_script_invocation()
