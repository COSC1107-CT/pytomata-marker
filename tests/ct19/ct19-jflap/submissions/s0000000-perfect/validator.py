from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import os
import sys
import re
import zipfile
import argparse

"""
Constant literal defining specs. Decided to code it here instead of including it in a JSON as this allows the whole
script to be self contained and allows a student to simply drag and drop a zip file into the script for execution.
"""

EXPECTED = [
    "E1-Qa1.txt",
    "E1-Qa2.txt",
    "E1-Qa3.txt",
    "E1-Qa4.txt",
    "E1-Qa5.txt",
    "E1-Qa6.txt",
    "E1-Qa7.txt",
    "E1-Qb1.txt",
    "E1-Qb2.txt",
    "E1-Qb3.txt",
    "E1-Qb4.txt",
    "E2-Qa1.txt",
    "E2-Qa2.txt",
    "E2-Qa3.txt",
    "E2-Qa4.txt",
    "E2-Qb1.txt",
    "E2-Qc1.txt",
    "E2-Qc2.txt",
    "E3-Qa1.txt",
    "E3-Qa2.txt",
    "E3-Qa3.txt",
    "E3-Qa4.jff",
    "E3-Qa5.jff",
    "E3-Qb1.jff",
    "E3-Qb2.txt",
    "E3-Qc1.txt",
    "E3-Qc2.txt",
    "E4-Qa1.jff",
    "E4-Qb1.jff",
    "E5-Qa1.txt"
]


def ok(output):
    print("OK: " + output)

def fail(output):
    print("FAIL: " + output)
    success = False


def extract_file_name_from_path(path):
    # Split by unix/linux file seperator first
    file_name = path.split("/")[-1]

    # resplit by windows seperator
    # This ensures that the file name is extracted on windows and linux platforms.
    file_name = file_name.split("\\")[-1]
    return file_name

"""
Code to validate that the zip file is named correctly.
Expected naming standard is 7 digits followed by zip (Case insensitive)
"""
def validate_zip_name(zip_path):

    zip_name = extract_file_name_from_path(zip_path)

    if re.match(r"[0-9]{7}.zip", zip_name, re.IGNORECASE):
        ok("ZIP file name: " + zip_name + " is ok.")
        return True
    else:
        fail("ZIP file name: " + zip_name + " must be your student number without the leading s. e.g. 3215678.zip")
        return False

"""
Code to validate expected files as specified above.
"""
def validate_files(zip_path):

    #Initially set to false as the file may fail to open.
    success = False

    with zipfile.ZipFile(zip_path) as z:
        #File openned successfully, set to true so that any failure downstream to re flag it as false.
        success = True
        x = [i.filename for i in z.infolist()]

        for expected_filename in EXPECTED:
            if expected_filename in x:
                ok("File: " + expected_filename + " is named correctly")
            else:
                fail("File: " + expected_filename + " is not found in the zip root.")
                success = False

        for existing_file in x:
            if existing_file in EXPECTED:
                pass
            else:
                fail("File: " + existing_file + " is in the zip but it's not expected. "
                                                "Please ensure the file is in the zip root.")
                success = False

    return success


def validate(zip_path):
    return validate_zip_name(zip_path) and validate_files(zip_path)

def main():
    parser = argparse.ArgumentParser(
        description= 'Validate file content in zip submission file for COSC1107/1105 Assignment 1. \n'
                     'Will check if it is a zip file and if the name of the files inside are correct.'
                     'Note it does NOT check the encoding of the files or their types (text or JFLAP).'
    )
    parser.add_argument('domain-problem',
                        help='.zip file containing the submission')

    zip_path = vars(parser.parse_args())['domain-problem']

    if not os.path.isfile(zip_path):
        print("\n FILE '{}' NOT FOUND. The file does not seem to exist. Please double check.".format(zip_path))
        sys.exit(2)

    if not zipfile.is_zipfile(zip_path):
        print("\n FILE '{}' IS NOT A ZIP FILE. Seems it is not a legal zip file, please check.".format(zip_path))
        sys.exit(2)

    if validate(zip_path):
        print("\n ALL TESTS SUCCESSFUL, your zip file is correctly formatted.")
        print()
        sys.exit(0)
    else:
        print("\n ONE OR MORE TESTS FAILED. Please check the results above for details.")
        print()
        sys.exit(2)


def print_usage():
    print("Usage: python validate.py <path to zip file>.zip")
    sys.exit(1)

if __name__ == "__main__":
    main()