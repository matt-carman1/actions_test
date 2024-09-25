from os.path import dirname, basename

import pytest
from library.utils import is_k8s


def pytest_addoption(parser):
    parser.addoption("--headless",
                     action="store",
                     help="Set to a nonzero character to run  test in headless "
                     "mode. By default, running multiple tests will run "
                     "in headless mode. Single tests do not run in "
                     "headless by default. To disable headless, "
                     "use --headless=0")
    parser.addoption('--functional_areas',
                     nargs='+',
                     help="Specify one or more space-separated functional areas of tests "
                     "to be run. Functional areas are the subfolder names under tests/,"
                     "for example, 'filter', 'grid', 'project'")
    parser.addoption('--types',
                     nargs='+',
                     choices=['smoke', 'happy_path', 'edge_case', 'regression'],
                     help="Specify one or more space-separated test types. Allowable types "
                     "are 'smoke', 'happy_path', 'edge_case', 'regression'")
    parser.addoption('--slow', action='store_true', help='Run slow tests')
    parser.addoption('--flaky', action='store_true', help='Run flaky tests')
    parser.addoption('--customized_server_config',
                     action='store_true',
                     help='Run tests w/ custom server configuration or serial marker')

    parser.addoption("--print_test_names",
                     action="store_true",
                     default=None,
                     help="Print test names such that Tiltfile can use them as arguments in test commands")


def pytest_collection_finish(session):
    if session.config.option.print_test_names is not None:
        for item in session.items:
            print(item.name)
        pytest.exit('Done!', 0)


def pytest_collection_modifyitems(config, items):
    driver = config.getoption('--driver')
    functional_areas = config.getoption('--functional_areas', default=())
    types = config.getoption('--types', default=())
    run_slow_tests = config.getoption('--slow', default=False)
    run_flaky_tests = config.getoption('--flaky', default=False)
    customized_server_config = config.getoption('--customized_server_config', default=False)

    if functional_areas:
        skip_func_area = pytest.mark.skip(reason='Not in requested functional areas')
        for item in items:
            parent_dir = basename(dirname(item.fspath))
            if parent_dir not in functional_areas:
                item.add_marker(skip_func_area)

    if types:
        types_set = set(types)
        skip_type = pytest.mark.skip(reason='Not the requested test type')
        for item in items:
            has_marker_gen = (marker.name for marker in item.iter_markers() if marker.name in types_set)
            has_marker = next(has_marker_gen, None)

            if not has_marker:
                item.add_marker(skip_type)

    if not run_slow_tests:
        skip_slow = pytest.mark.skip(reason='Skipping slow tests')
        for item in items:
            if item.get_closest_marker('slow'):
                item.add_marker(skip_slow)

    if not run_flaky_tests:
        for item in items:
            flaky_marker = item.get_closest_marker('flaky')
            if flaky_marker:
                skip_marker = pytest.mark.skip(reason=flaky_marker.kwargs.get('reason', 'Skipping flaky test'))
                item.add_marker(skip_marker)

            xfail_markers = {
                "app_defect": "Xfailing tests affected by Application/LiveDesign defect",
                "script_issue": "Xfailing tests affected by script issue/Test Data Issue",
                "fw_issue": "Xfailing tests affected by framework issue",
                "env_issue": "Xfailing tests affected by environment issue",
                "unclear_cause": "Xfailing tests with unclear cause"
            }
            for marker in xfail_markers:
                xfail_marker = item.get_closest_marker(marker)
                if xfail_marker:
                    xfail_marker = pytest.mark.xfail(reason=xfail_marker.kwargs.get('reason', xfail_markers[marker]))
                    item.add_marker(xfail_marker)

            k8s_defect_marker = item.get_closest_marker('k8s_defect')
            if k8s_defect_marker and is_k8s():
                xfail_marker = pytest.mark.xfail(
                    reason=k8s_defect_marker.kwargs.get('reason', 'Xfailing tests affected by k8s_defect'))
                item.add_marker(xfail_marker)

    # Handle skipping browserstack tests
    if driver == 'BrowserStack':
        bstack_skip = pytest.mark.skip(reason='Test failing/flaky on BrowserStack -- skipping')
        for item in items:
            if item.get_closest_marker('browserstack_skip'):
                item.add_marker(bstack_skip)

    # Handle custom server configuration
    if customized_server_config:
        skip_noncustom = pytest.mark.skip(reason='Skipping tests w/ neither custom server config nor serial marker')
        for item in items:
            if item.get_closest_marker('serial'):
                continue
            elif 'customized_server_config' in item.fixturenames:
                # Mark all tests with customized_server_config fixture as serial
                item.add_marker('serial')
            else:
                item.add_marker(skip_noncustom)

        # NOTE: Idea for dynamically creating groups of LD Prop tests to be run in parallel
        # custom_configs = []
        # for item in custom_config_items:
        # if not item.module.LD_PROPERTIES in custom_configs:
        # custom_configs.append(item.module.LD_PROPERTIES)

    else:
        skip_custom_server = pytest.mark.skip(name="skip_custom_server",
                                              reason='Skipping tests w/ custom server config')
        skip_serial = pytest.mark.skip(name="skip_serial", reason='Skipping tests w/ serial marker')
        for item in items:
            if 'customized_server_config' in item.fixturenames:
                item.add_marker(skip_custom_server)
            if item.get_closest_marker('serial'):
                item.add_marker(skip_serial)

    if driver != None:
        for item in items:
            # NOTE:
            # Not changing the Item name for legacy admin_pannel test cases as they are failing with "AttributeError" if we change
            if ("/admin_panel/" not in item._nodeid):
                item.name = item.name + "_" + driver
            item.originalname = item.originalname + "_" + driver
            item._nodeid = item._nodeid + "_" + driver

    for item in items:
        if item.get_closest_marker('serial'):
            if ("/admin_panel/" not in item._nodeid):
                item.name = item.name + "_serial"
            item.originalname = item.originalname + "_serial"
            item._nodeid = item._nodeid + "_serial"

    # Excluding the test cases from the execution based for the below markers
    excluded_marker_names = ['skip_custom_server', 'skip_serial', 'skip_report']
    index = 0
    while index < len(items):
        item = items[index]
        excluded = False
        for marker in item.own_markers:
            marker_name = marker.kwargs.get('name', marker.name)
            if marker_name in excluded_marker_names:
                items.pop(index)
                excluded = True
                break
        if not excluded:
            index += 1


@pytest.fixture
def chrome_options(chrome_options, is_headless):
    if is_headless:
        chrome_options.add_argument('headless')
    chrome_options.add_argument("--window-size=1366,768")
    chrome_options.add_argument("--ignore-gpu-blocklist")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options


@pytest.fixture
def firefox_options(firefox_options, is_headless):
    if is_headless:
        firefox_options.headless = True
    firefox_options.add_argument("--width=1366")

    if is_k8s():
        # Set the height to 11px over 768 to handle a change in browser height in k8s
        firefox_options.add_argument("--height=779")
    else:
        firefox_options.add_argument("--height=768")
    return firefox_options


@pytest.fixture(scope='session')
def is_headless(pytestconfig, request):
    """
    Default to headless mode when running more than one test, and not headless
    when just running one test

    :param pytestconfig: pytest configuration options
    :param request: pytest request object
    :return: bool
    """
    # Set defaults when headless option is not set
    if not pytestconfig.getoption('--headless'):
        return len(request.node.items) > 1

    # Set defaults when headless option has been specified
    else:
        return pytestconfig.getoption('--headless') != '0'
