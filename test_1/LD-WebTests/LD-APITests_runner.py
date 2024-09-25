import argparse
import os
import sys

from library.runner_utils import run_pytest_commands

REPORT_DIR = os.path.join('..', 'SEURAT-InfoVis', 'build', 'test-reports', 'xml')

PYTHON_EXECUTABLE_PATH = sys.executable


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all_tests', action='store_true', help='run all tests, including slow and flaky')
    parser.add_argument('--smoke', action='store_true', help='run just the smoke test suite')
    parser.add_argument('--repeat', action='store', help='how often to repeat tests')
    parser.add_argument('--reruns', action='store', help='how often to rerun tests on failure')
    parser.add_argument('--extra_pytest_args', action='store', help='any extra args to pass to pytest')
    parser.add_argument('--error_on_fail', action='store_true', help='Specify to propagate exit codes on test failures')
    return parser.parse_args()


def get_subprocess_call(args):

    # Assign args to variables
    all_tests = args.all_tests
    repeat = args.repeat
    reruns = args.reruns
    smoke = args.smoke
    extra_pytest_args = args.extra_pytest_args

    report_xml = os.path.join(REPORT_DIR, 'api_{}_results.xml')

    cmds = []
    parallel_tests_cmd = [PYTHON_EXECUTABLE_PATH, "-m", "pytest", "--junitxml", report_xml.format('parallel')]
    cmds.append(parallel_tests_cmd)

    serial_tests_cmd = [
        PYTHON_EXECUTABLE_PATH, "-m", "pytest", '-m serial', "--customized_server_config", "--junitxml",
        report_xml.format('serial')
    ]
    cmds.append(serial_tests_cmd)

    # Update extra pytest command line flags based on our testrunner flags
    extra_cmd_args = []
    extra_cmd_args.append('--ignore=tests/selenium')
    if all_tests:
        extra_cmd_args.extend(['--flaky', '--slow'])
    if smoke:
        extra_cmd_args.extend(['--types', 'smoke'])
    if repeat:
        extra_cmd_args.append('--count={}'.format(repeat))
    if reruns:
        extra_cmd_args.append('--reruns={}'.format(reruns))
    if extra_pytest_args:
        for arg in extra_pytest_args.split(' '):
            extra_cmd_args.append(arg)

    if extra_cmd_args:
        for cmd in cmds:
            cmd.extend(extra_cmd_args)
    return cmds


def main():
    args = get_parser()
    pytest_cmds = get_subprocess_call(args)
    run_pytest_commands(pytest_cmds, args.error_on_fail)


if __name__ == '__main__':
    main()
