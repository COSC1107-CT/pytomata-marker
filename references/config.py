# SAMPLE CONFIGURATION FILE AS PER AI24 - MINECRAFT
import os
from pathlib import Path

CONFIG_SCRIPT_PATH = Path(os.path.realpath(__file__)).parent

# max student query time, per query (in seconds)
QUERY_TIMEOUT = 100

# test suites
PATH_TEST_DIR = CONFIG_SCRIPT_PATH / "domains/ct19"
PATH_TESTS = PATH_TEST_DIR / "tests.yaml"
PATH_ANSWERS = PATH_TEST_DIR / f"{PATH_TESTS.stem}_answers{PATH_TESTS.suffix}"

# solution template files (contains model solution)
PATH_SOL = PATH_TEST_DIR / "solution/"

# submission folders (contains student folders)
PATH_SUB = Path("submissions/ai24/")
DEFAULT_SUBMISSION_FILE = "minecraft.pl"

# where repors should be placed
PATH_REPORTS = Path("reports/")


## MARKING WEIGHTS
W_REDUNDANT = 0.1
W_COMPLETENESS = 0.9
W_INCORRECT = 0.7

## Precision expected for float comparisons
FLOAT_PRECISION = 3
