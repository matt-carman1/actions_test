import argparse
import os
import shlex
import sys
from socket import gethostname

# set LD_SERVER to localhost 8080
# os.environ["LD_SERVER"] = "http://localhost:8080/"
from library.runner_utils import run_pytest_commands

REPORT_DIR = os.path.join('..', 'SEURAT-InfoVis', 'build', 'test-reports', 'xml')

PYTHON_EXECUTABLE_PATH = sys.executable


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser',
                        action='store',
                        choices=['Chrome', 'Firefox', 'BrowserStack'],
                        help="Browser to test")
    parser.add_argument('--all_tests', action='store_true', help='run all tests, including slow and flaky')
    parser.add_argument('--smoke', action='store_true', help='run just the smoke test suite')
    parser.add_argument('--repeat', action='store', help='how often to repeat tests')
    parser.add_argument('--reruns', action='store', help='how often to rerun tests on failure')
    parser.add_argument('--extra_pytest_args', action='store', help='any extra args to pass to pytest')
    parser.add_argument('--error_on_fail', action='store_true', help='Specify to propagate exit codes on test failures')
    return parser.parse_args()


def get_subprocess_call(args):

    # Assign args to variables
    browser = args.browser
    all_tests = args.all_tests
    repeat = args.repeat
    reruns = args.reruns
    smoke = args.smoke
    extra_pytest_args = args.extra_pytest_args
    number_concurrent_tests = '8'

    report_xml = os.path.join(REPORT_DIR, '{}_{{}}_results.xml'.format(browser))
    cmds = []
    if browser == "Chrome" or browser == "Firefox":
        parallelized_tests_cmd = [
            PYTHON_EXECUTABLE_PATH, "-m", "pytest", "--driver", "{}".format(browser),
            "-n={}".format(number_concurrent_tests), "--html", "{}_parallel_results.html".format(browser), "--junitxml",
            report_xml.format('parallel')
        ]
        cmds.append(parallelized_tests_cmd)

        serial_tests_cmd = [
            PYTHON_EXECUTABLE_PATH, "-m", "pytest", '-m serial', "--driver", "{}".format(browser), "--html",
            "{}_serial_results.html".format(browser), "--customized_server_config", "--junitxml",
            report_xml.format('serial')
        ]
        cmds.append(serial_tests_cmd)
    else:
        browserstack_cmd = [
            PYTHON_EXECUTABLE_PATH, '-m', 'pytest', '--driver', "{}".format(browser), "--capability", "browserName",
            "IE", "--capability", "browser_version", "11.0", "--capability", "os", "Windows", "--capability",
            "os_version", "10", "--capability", "browserstack.local", "True", "--capability",
            "browserstack.localIdentifier",
            gethostname(), "--html", "{}_results.html".format(browser), "--junitxml", report_xml
        ]
        cmds.append(browserstack_cmd)

    # Update extra pytest command line flags based on our testrunner flags
    extra_cmd_args = []
    if all_tests:
        extra_cmd_args.extend(['--flaky', '--slow'])
    if smoke:
        extra_cmd_args.extend(['--types', 'smoke'])
    if repeat:
        extra_cmd_args.append('--count={}'.format(repeat))
    if reruns:
        extra_cmd_args.append('--reruns={}'.format(reruns))
    if extra_pytest_args:
        extra_cmd_args.extend(shlex.split(extra_pytest_args))

    # NOTE(fennell): ignore non-browser tests in the API directory. These are ran seperately
    extra_cmd_args.append('--ignore=tests/api')

    if extra_cmd_args:
        for cmd in cmds:
            cmd.extend(extra_cmd_args)

    # NOTE: Firefox headless is not compatible with webgl, so disable these tests remove this once we figure out a way
    # to enable webgl on Firefox.
    for cmd in cmds:
        if browser == "Firefox":
            cmd.append('-m serial and not require_webgl') if '-m serial' in cmd else cmd.append('-m not require_webgl')

    return cmds


def main():
    args = get_parser()
    pytest_cmds = get_subprocess_call(args)
    run_pytest_commands(pytest_cmds, args.error_on_fail)


if __name__ == '__main__':
    main()
