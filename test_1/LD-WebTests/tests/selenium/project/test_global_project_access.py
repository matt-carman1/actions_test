"""

Test to determine whether user has access to appropriate projects.

"""
import pytest

from helpers.change.project import open_project
from helpers.selection.project import PROJECT_LIST_ITEMS, INVALID_PROJECT_MODAL
from helpers.selection.splash_page import CREATE_LR_TITLE
from helpers.verification.project import verify_project_not_present, verify_project_present
from library import dom, url, wait
from library.authentication import login, logout

import time

#Note: We are using fixtures from 2022.1.0 release
#HIDE_GLOBAL_PROJECT is deleted from the ld_property_override table.

RESTRICTED_PROJECTS = ["Default Restricted Project", "JS Testing", "NoMod Testing", "RestrictedBC"]
LD_PROPERTIES = {'HIDE_GLOBAL_PROJECT': 'false'}


@pytest.mark.usefixtures('customized_server_config')
@pytest.mark.smoke
def test_global_project_access(selenium):
    """
    Selenium test function

    :param selenium: Selenium webdriver
    """

    # Login as demo user (this user has admin privileges)
    login(selenium, 'demo', 'demo')

    # Get the list of available projects
    admin_user_projects = dom.get_elements(selenium, PROJECT_LIST_ITEMS)

    # Ensure that the global project is visible in this list
    verify_project_present(admin_user_projects, project_name='Global')

    # Ensure that all restricted projects are visible in that list
    for project_name in RESTRICTED_PROJECTS:
        verify_project_present(admin_user_projects, project_name)

    # Log out of demo/demo
    logout(selenium)

    # Log in as different, non-admin user (userA)
    login(selenium, 'userA', 'userA')

    # Get the list of projects available to non-admin user (userA)
    restricted_user_projects = dom.get_elements(selenium, PROJECT_LIST_ITEMS)

    # Ensure that restricted projects are NOT visible in that list
    for project_name in RESTRICTED_PROJECTS:
        verify_project_not_present(restricted_user_projects, project_name)

    # Ensure that the restricted project accessible to non-admin user(userA) is visible at the least
    verify_project_present(restricted_user_projects, project_name='RestrictedAB')

    # Select a project and click OK
    open_project(selenium, "Global")
    # Added a wait for the project page to load properly.
    wait.until_visible(selenium, CREATE_LR_TITLE, text='Create a\nNew LiveReport')

    # Navigate to project 7 and verify no access.
    # Note that here we **directly modify the URL in the location bar**,
    # as if we were a user trying to gain access to a project that they can't
    # see in the project window.
    check_no_project_access(selenium, 7)


def check_no_project_access(driver, project_id):
    """
    Helper function to ensure user does not have access to a given project when
    navigating to that project link

    :param driver: Selenium webdriver
    :param project_id: Project ID in link
    """
    id_str = str(project_id)
    url.set_page_hash(driver, "/projects/" + id_str)
    # Adding a wait for the test to wait for the project page to load after setting the URL hash.
    time.sleep(0.5)
    invalid_text = dom.get_element(driver, INVALID_PROJECT_MODAL).text
    assert invalid_text == 'The project with ID {} does not exist or is ' \
                           'currently not accessible. Please ensure that the ' \
                           'project ID is valid or contact your system ' \
                           'administrator.'.format(id_str)
