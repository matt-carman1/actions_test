"""
This file contains fixtures that setup the initial state of LiveDesign before executing tests.
These include things such as logging in, creating a new LR, opening a project..etc.

### OVERRIDING FIXTURE DEFAULT PARAMETERS (login name, password, project name...etc) ###
Defaults, such as the login name and password parameters, are defined within the fixture using the function:

    getattr(object, name, default=None)

getattr will return any variable that matches the 'name' argument. If there is no matching variable found,
it will return the value set by the default argument (or None if no default defined).

To override fixture defaults, define the parameters explicitly in the test before calling the fixture. These parameters
should be the same name as defined in the 'name' argument of the getattr() function.

### EXAMPLE OVERRIDE ###
The open_project(request, selenium) fixture defaults to login to LD as 'demo'/'demo' and opens project 'JS Testing'.
To change these default settings, in the test define global variables:

    test_project_name = 'Project A'
    test_username = 'userA'
    test_password = 'userA'
    def test_a_different_project(selenium, open_project):
        assert open_project == test_project_name, 'The specified test project was opened'

This will modify the open_project fixture to log into LiveDesign as 'userA' and open project 'Project A'.
To validate whether 'Project A' was opened, an assert statement in the test module was also added to confirm that the
value returned by the yield statement (in the open_project fixture) matched the test_project_name variable defined.
"""
import allure
import pytest
from helpers.change import project
from helpers.change.live_report_menu import delete_open_live_report
from helpers.change.live_report_picker import create_and_open_live_report, open_live_report
from ldclient import LDClient

from helpers.selection.live_report_tab import TAB_ACTIVE, TAB_DOWNARROW, TAB_NAMED_
from library import dom, wait
from library.authentication import login
from library.api.urls import LDCLIENT_HOST


@pytest.fixture(scope='function')
def new_live_report_via_ui(request, selenium, open_project):
    """
    Login, open project and create a new, empty live report. By default, the
    report will be named after the test name, but this may be overridden by
    setting module variable `test_report_name`

    :param open_project: invoke fixture to open a project
    :param request: request object with test metadata (from pytest fixture)
    :param selenium: selenium fixture
    :return: <str>, newly created Live Report name
    """
    new_report_name = getattr(request.module, 'test_report_name', request.node.name)

    test_project_name = getattr(request.module, 'test_project_name', None)

    folder_name = '{project} Home'.format(project=test_project_name) if test_project_name else None
    lr_name = create_and_open_live_report(selenium, new_report_name, folder_name=folder_name)

    def finalizer():
        delete_open_live_report(selenium, lr_name)

    request.addfinalizer(finalizer)

    return lr_name


@pytest.fixture(scope='function')
def open_project(request, selenium, login_to_livedesign):
    """
    Login and open a project. By default, the credentials are demo/demo and the
    project is 'JS Testing'

    Defaults may be overridden by adding module variables named
    `test_project_name`, `test_username`, and `test_password`. For example:

        test_project_name = 'Project A'
        test_username = 'userA'
        test_password = 'userA'

    :param request: request object with test metadata (from pytest fixture)
    :param selenium: webdriver (from pytest-selenium fixture)
    :param login_to_livedesign: fixture to login into LiveDesign
    :return: <str>, name of project opened
    """
    project_to_open = getattr(request.module, 'test_project_name', 'JS Testing')
    project.open_project(selenium, project_to_open)

    return project_to_open


@pytest.fixture(scope='function')
def login_to_livedesign(request, selenium):
    """
    Login. By default, the credentials are demo/demo

    Defaults may be overridden by adding module variables named
    `test_username`, and `test_password`. For example:

        test_username = 'userA'
        test_password = 'userA'

    :param request: request object with test metadata (from pytest fixture)
    :param selenium: webdriver (from pytest-selenium fixture)
    """
    try:
        # This is because request.param is not available if we are doing indirect parametrization else it would
        # generate attribute error.
        test_username = request.param[0]
        test_password = request.param[1]
    except AttributeError:
        test_username = getattr(request.module, 'test_username', 'demo')
        test_password = getattr(request.module, 'test_password', 'demo')

    login(selenium, test_username, test_password)
    return test_username


@pytest.fixture(scope="function")
def customized_server_config(request, selenium):
    """
    Logs in a user using custom LD_PROPERTIES (w/o restart required)
    Defaults:
        test_username: "demo"
        test_password: "demo"

    Example Usage:
        import pytest


        LD_PROPERTIES = {'ENABLE_INTERNAL_ENUMERATION': 'true'}


        @pytest.mark.usefixtures('customized_server_config')
        def test_new_enumeration(selenium):
            print('breakpoint')
    :param request: request object with test metadata (from pytest fixture)
    :param selenium: Selenium Webdriver
    :return: updated properties
    """
    test_username = getattr(request.module, 'test_username', 'demo')
    test_password = getattr(request.module, 'test_password', 'demo')

    try:
        properties = request.param
    except AttributeError:
        properties = getattr(request.module, 'LD_PROPERTIES', {})

    # If no properties were provided for override, there's nothing to do here..
    # NOTE: This was only done to support a workaround for the legacy E2E Admin
    #       Tests which required us to run tests in serial, via --custom_server_config
    # SEE:  AdminSeleniumWebDriverTestCase.LD_PROPERTIES for info
    if len(properties) == 0:
        return properties

    client = LDClient(host=LDCLIENT_HOST, username=test_username, password=test_password, compatibility_mode=(8, 10))

    config = client.config()
    original_properties = {
        config_item.get('key'): config_item.get('value')
        for config_item in config
        if config_item.get('key') in properties.keys()
    }

    def fin():
        client.update_properties(original_properties)

    request.addfinalizer(fin)
    properties = client.update_properties(properties)
    selenium.refresh()
    return properties


@pytest.fixture(scope="function")
def open_livereport(request, selenium, open_project):
    """
    Opens a LiveReport that is set in "test_livereport" variable. Make sure to set it before calling the fixture in
    the test. This fixture is created to ideally supplement duplicate_live_report_via_client fixture to open the
    duplicated LR generated by it.
    To override login user/password and project, refer to the docstring in the fixture open_project for variables to
    set.

    :param request: request object with test metadata (from pytest fixture)
    :param selenium: selenium fixture that returns Webdriver (from pytest-selenium plugin)
    :param open_project: fixture that opens the project. Default is 'JS Testing' project. Default
                        can be overridden by setting "test_project_name" before the start of the test. For e.g.
                        test_project_name = 'Project A'
    """

    try:
        report_to_open = getattr(request.module, 'test_livereport', None)
        assert report_to_open
    except AssertionError:
        raise dom.LiveDesignWebException('Variable "test_livereport" must be defined either manually or by '
                                         'another fixture before calling the open_livereport fixture')

    open_live_report(selenium, name=report_to_open)
    wait.until_visible(selenium, f"{TAB_ACTIVE}{TAB_NAMED_.format(report_to_open)} {TAB_DOWNARROW}")


@pytest.fixture(scope="function")
def is_rdkit_registration_enabled(ld_client):
    return 'true' == [
        property['value'] for property in ld_client.config() if property['key'] == 'USE_RDKIT_STRUCTURE_REGISTRATION'
    ][0]


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    set up a hook to be able to check if a test has failed.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(selenium, request):
    """
    Take screenshot on test failure
    """
    yield
    try:
        if request.node.rep_call.failed:
            screenshotName = request.node.name + ".png"
            allure.attach(selenium.get_screenshot_as_png(),
                          name=screenshotName,
                          attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print("Unable to take screenshot:", str(e))
