""" """

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
    print(student_solution_partitions)


def calculate_and_output_results_for_student_solution_partition():
    """ """

    # TODO: Generator.
    def calculate_results_for_student_solution_partition():
        """ """
        pass

    # TODO: File and standard output. Exclusion lock for standard output.
    def output_individual_student_results():
        """ """
        pass

    for _ in calculate_results_for_student_solution_partition():
        pass


# TODO: Lock should be here.
def print_individual_student_results_to_standard_output():
    """ """
    pass


if __name__ == "__main__":
    calculate_and_output_student_results()
