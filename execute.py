""" """

import multiprocessing

import pytomata
import utilities


def calculate_and_output_student_results():
    """ """

    def derive_and_partition_student_solution_files():
        """ """
        student_solution_partitions = [[] for _ in range(args.process_count)]
        partition_index = 0
        for path in args.student_solution_paths:
            if path.is_file() and path.suffix == ".py":
                student_solution_partitions[partition_index].append(path)
                partition_index = (partition_index + 1) % args.process_count
            elif path.is_dir():
                for script_path in path.glob("*.py"):
                    student_solution_partitions[partition_index].append(script_path)
                    partition_index = (partition_index + 1) % args.process_count
        return student_solution_partitions

    args = utilities.construct_and_parse_args()
    student_solution_partitions = derive_and_partition_student_solution_files()
    process_context = (args.questions_script_path, args.output_directory_path)
    with multiprocessing.Pool(args.process_count) as process_pool:
        process_pool.starmap(
            calculate_and_output_results_for_student_solution_partition,
            zip(student_solution_partitions, [process_context] * args.process_count),
        )


def calculate_and_output_results_for_student_solution_partition(student_solution_partition, process_context):
    """ """

    def calculate_results_for_student_solution_partition():
        """ """
        for student_solution_path in student_solution_partition:
            solutions = utilities.load_using_path(student_solution_path)
            student_id = student_solution_path.stem
            student_results = pytomata.calculate_student_results_and_feedback(
                questions.construct_questions_and_solutions(solutions)
            )
            yield student_id, student_results

    # TODO: File and standard output. Exclusion lock for standard output.
    def output_individual_student_results():
        """ """
        print(identifier, results)

    questions_script_path, output_directory_path = process_context
    questions = utilities.load_using_path(questions_script_path)
    for identifier, results in calculate_results_for_student_solution_partition():
        output_individual_student_results()


# TODO: Lock should be used here.
def print_individual_student_results_to_standard_output():
    """ """
    pass


if __name__ == "__main__":
    calculate_and_output_student_results()
