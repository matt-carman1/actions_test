import pytest

from library import utils, dom
from library.api.urls import LDCLIENT_HOST
from library.url_endpoints import HOST
from ldclient import LDClient, models
from ldclient.models import LiveReport
from library.api.exceptions import LiveDesignAPIException
import requests

from library.utils import make_unique_name


@pytest.fixture(scope="session")
def ld_client():
    return LDClient(host=LDCLIENT_HOST, username="demo", password="demo", compatibility_mode=(8, 10))


@pytest.fixture(scope="module")
def use_module_isolated_project(request, ld_client):
    """
    Create a new project through LD Client.

    NOTE: This fixture will only run once per module, which means that it will
    not open the newly created project automatically, since we don't have access
    to the selenium webdriver at the module level. You will likely need to use
    the 'open_project' fixture alongside this.

    Defaults:
        test_project_name: request.module.__name__[1]
        test_username: "demo"
        test_password: "demo"
        test_project_description: "scratch project"
        test_project_is_restricted: True

    Yields a string of the project name, not the project object.

    :param request: request object with test metadata (from pytest fixture)
    :param ld_client: fixture that returns the LDClient object
    :return: <str>, name of new project
    """
    module_name = request.module.__name__.split('.')[1]
    project_name = getattr(request.module, 'test_project_name', module_name)
    project_name = utils.make_unique_name(project_name)
    project_restricted = getattr(request.module, 'test_project_is_restricted', True)
    project_description = getattr(request.module, 'test_project_description', 'scratch project')

    # Creating ldclient model Project object
    new_project = models.Project(name=project_name, description=project_description, restricted=project_restricted)

    try:
        new_project_object = ld_client.create_project(new_project)
    except requests.exceptions.RequestException as e:
        print("An error occurred while creating a new Project")
        raise SystemExit(e)

    # TODO when it's possible to delete a project via the client, add a finalizer to do so

    # Set the module's test_project_name to the newly created project, allowing other tests in the same module to use it
    request.module.test_project_name = new_project_object.name
    request.module.test_report_project_id = new_project_object.id

    return project_name


# Note: Currently there is no method to get the addable column ID for a column given it's column name. We could
# either use column_descriptors() or live_report_results_metadata() and write a method to get the addable column IDs.
# This would increase the setup time but definitely would be easier for the test writer and improves readability.
# Other option is to treat columns_ids_subset as a dict such that the readability is not compromised and we can
# easily get the addable column ids rather than calling the ldclient methods to give us Addable column IDs given
# column names. Check out LDIDEAS-4988
"""
When writing the test you could you use the following lines of code to get the addable column ID for now by just 
providing the server name and livereport ID. Run this in your pycharm python console for ease.

import ldclient
ld_client = ldclient.LDClient(<SERVER_NAME> + '/livedesign/api', 'demo', 'demo', compatibility_mode=(8, 10))
lr_column_desc = ld_client.column_descriptors(live_report_id='54852')
livereport_column_details = {}
for col_desc in lr_column_desc:
    livereport_column_details[col_desc.display_name] = col_desc.addable_column_id
print(livereport_column_details)
"""


@pytest.fixture(scope='function')
def duplicate_live_report(request, ld_api_client):
    """
    Duplicates a live report using ldclient and sets "test_livereport variable" to the duplicated LR name.
    The Live Report to duplicate is set by defining variable 'live_report_to_duplicate' before calling this fixture.
    Also, set the test_project_id for copying the LR. It should be same as the existing LRs project ID.

    For example, to duplicate the LR "3 Compounds 2 Poses":
        live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}
        test_project_id = 4
        @pytest.mark.usefixtures("duplicate_live_report")

    NOTE: This fixture will not open the newly created LiveReport automatically. You will likely need to use the
    'open_livereport' fixture alongside this. For e.g.
    a) Otherwise use it in the standard way:
        @pytest.mark.usefixtures("open_livereport")
        @pytest.mark.usefixtures("duplicate_live_report_via_client")
        def test_one(selenium):
    b) Use it like this if you want to get the LR name in the test from the fixture:
        def test_one(selenium, duplicate_live_report_via_client, open_livereport):
            duplicate_lr_name = duplicate_live_report_via_client


    :param request: request object with test metadata (from pytest fixture)
    :param ld_api_client: fixture that returns the LDClient object
    :return: None
    """

    # set LiveReport name, LiveReport id and Project ID to look for and duplicate
    try:
        report_to_duplicate = getattr(request.module, 'live_report_to_duplicate', None)

        # Defaulting the project to "JS Testing" i.e project_id ='4'
        report_to_duplicate_project_id = getattr(request.module, 'test_project_id', '4')
        assert report_to_duplicate and report_to_duplicate_project_id

        # Getting LiveReport Name and ID from the report_to_duplicate dictionary
        report_to_duplicate_name = report_to_duplicate['livereport_name']
        report_to_duplicate_alias = report_to_duplicate['livereport_id']

    except AssertionError:
        raise dom.LiveDesignWebException('Variable "live_report_to_duplicate" and "test_project_id" must be defined '
                                         'before calling the duplicate_live_report fixture')
    except KeyError:
        raise dom.LiveDesignWebException('Keys "livereport_name" and "livereport_id" for the dictionary '
                                         '"live_report_to_duplicate" must be defined.')

    # Getting the attributes in case a subset of the LR is to be duplicated. Default is None which means all the
    # compounds and columns would be copied
    entity_ids_to_copy = getattr(request.module, 'entity_ids_subset', None)
    column_ids_to_copy = getattr(request.module, 'column_ids_subset', None)

    # set duplicate Live Report name (the new Live Report name)
    new_report_name = getattr(request.module, 'test_report_name', request.node.name)
    duplicate_report_new_name = make_unique_name(new_report_name if new_report_name else report_to_duplicate_name)

    # Set params by creating LiveReport model for duplicate LR. Just providing the LR name and project ID for now.
    livereport_params = LiveReport(title=duplicate_report_new_name, project_id=report_to_duplicate_project_id)

    # Duplicate Live Report
    try:
        duplicate_livereport_object = ld_api_client.copy_live_report(template_id=report_to_duplicate_alias,
                                                                     live_report=livereport_params,
                                                                     entity_ids=entity_ids_to_copy,
                                                                     projections=column_ids_to_copy)
    except Exception as e:
        raise LiveDesignAPIException(e)

    # Setting the "test_livereport" variable to the duplicated LR name. This could be used by open_livereport fixture
    # to open this LR
    request.module.test_livereport = duplicate_livereport_object.title
    test_type = getattr(request.module, 'test_type', 'selenium')

    def finalizer():
        ld_api_client.delete_live_report(duplicate_livereport_object.id)

    request.addfinalizer(finalizer)
    if test_type == 'selenium':
        return duplicate_report_new_name
    return duplicate_livereport_object


def get_api_client(username=None, password=None):
    """
    Get the ldclient for specified username and password

    :param username: str, Username for the ldclient
    :param password:str, password for the specified username
    """
    try:
        # Note: Any wrong input for either LDCLIENT_HOST or username or password throws HTTPError.
        client = LDClient(host=LDCLIENT_HOST, username=username, password=password, compatibility_mode=(8, 10))
    except requests.exceptions.HTTPError as e:
        raise LiveDesignAPIException(
            "Unable to get LDClient object for Host:{}, username:{} and password:{}, Getting Error:{}".format(
                LDCLIENT_HOST, username, password, e),
            error=e)
    try:
        ping_return = client.ping()
        if ping_return:
            return client
        else:
            raise LiveDesignAPIException("ldclient ping returned False, It may not be able to hit the about path")
    except RuntimeError as e:
        raise LiveDesignAPIException("Ping returned error: {}".format(e), error=e)


@pytest.fixture(scope="function")
def ld_api_client(request):

    try:
        # This is because request.param is not available if we are doing indirect parametrization else it would
        # generate attribute error.
        test_username = request.param[0]
        test_password = request.param[1]
    except AttributeError:
        test_username = getattr(request.module, 'test_username', 'demo')
        test_password = getattr(request.module, 'test_password', 'demo')

    return get_api_client(username=test_username, password=test_password)


@pytest.fixture(scope="function")
def new_live_report(request, ld_api_client):
    """
    Fixture to create a new live report via ldclient API.
    :param request:
    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    """
    new_report_name = make_unique_name(getattr(request.module, 'test_report_name', request.node.name))
    live_report_description = getattr(request.module, 'test_report_description', '')
    live_report_template = getattr(request.module, 'test_report_template', False)
    live_report_rationale = getattr(request.module, 'test_report_rationale', None)
    live_report_alias = getattr(request.module, 'test_report_alias', None)
    live_report_project_id = getattr(request.module, 'test_report_project_id', 4)
    live_report_owner = getattr(request.module, 'test_report_owner', None)
    live_report_is_private = getattr(request.module, 'test_report_is_private', False)
    live_report_type = getattr(request.module, 'test_report_type', 'compound')
    live_report_folder = getattr(request.module, 'test_report_folder', 'JS Testing Home')
    # Get the list of available folders (tags) for LRs in the current project
    project_folders_list = ld_api_client.list_folders(project_ids=[live_report_project_id])
    # Given the 'JS Testing Home' folder name, find the folder's id
    # to pass it to the LiveReport LDClient model to set it when creating the LR.
    live_report_tag_ids = []
    for folder in project_folders_list:
        if folder.name == live_report_folder:
            live_report_tag_ids.append(folder.id)
            break

    live_report = LiveReport(title=new_report_name,
                             description=live_report_description,
                             update_policy='by_cachebuilder',
                             template=live_report_template,
                             shared_editable=True,
                             default_rationale=live_report_rationale,
                             assay_view=None,
                             id=None,
                             alias=live_report_alias,
                             project_id=live_report_project_id,
                             owner=live_report_owner,
                             is_private=live_report_is_private,
                             active=True,
                             addable_columns=None,
                             tags=live_report_tag_ids,
                             last_saved_date=None,
                             sorted_columns=None,
                             hidden_rows=None,
                             scaffolds=None,
                             report_level='parent',
                             type=live_report_type)

    try:
        new_live_report_object = ld_api_client.create_live_report(live_report)
    except requests.exceptions.RequestException as e:
        print("An error occurred while creating a LiveReport")
        raise SystemExit(e)

    # set request.module.test_livereport attribute to the newly created LR
    request.module.test_livereport = new_live_report_object.title
    test_type = getattr(request.module, 'test_type', 'selenium')

    def finalizer():
        ld_api_client.delete_live_report(new_live_report_object.id)

    request.addfinalizer(finalizer)

    # return the LR name when this fixture is being used for a selenium test
    if test_type == 'selenium':
        return new_report_name
    # return the LR object when this fixture is being used for an API test
    return new_live_report_object
