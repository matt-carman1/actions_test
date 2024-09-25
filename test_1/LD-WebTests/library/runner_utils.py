"""
This file is meant to deduplicate code between the API test runner & the selenium test runner
"""
from enum import Enum

import os
import subprocess


class PytestExitCode(Enum):
    SUCCESS = 0
    FAILURE = 1
    INTERRUPTED = 2
    INTERNAL_ERROR = 3
    USAGE_ERROR = 4
    NO_TESTS_COLLECTED = 5


SHOULD_ERROR_SET = {
    PytestExitCode.FAILURE, PytestExitCode.INTERRUPTED, PytestExitCode.INTERNAL_ERROR, PytestExitCode.USAGE_ERROR
}
SHOULD_SUCCEED_SET = {PytestExitCode.SUCCESS, PytestExitCode.NO_TESTS_COLLECTED}


def run_pytest_commands(pytest_cmds, error_on_fail):
    """
    :param pytest_cmds: pytest commands to run
    :type pytest_cmds: list of list of str
    :param error_on_fail: Whether or not to propagate the first error exit code
    :type error_on_fail: bool
    """
    exit_codes = []
    for cmd in pytest_cmds:
        proc = subprocess.Popen(cmd, cwd=os.getcwd())
        proc.communicate()
        exit_codes.append(proc.returncode)
    if error_on_fail:
        print(exit_codes)
        for e in exit_codes:
            if PytestExitCode(e) in SHOULD_ERROR_SET:
                print("Error exit codes returned for one or more subprocesses: {}".format(exit_codes))
                exit(e)
