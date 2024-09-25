import re

from helpers.selection.project import PROJECT_TITLE
from library import dom

test_project_name = 'YOYO'


def test_create_project(selenium, use_module_isolated_project, open_project):
    """
    Test to create a new project.
    :param selenium: Webdriver
    :param open_project: fixture used to create a new project using ldclient.
    :return:
    """
    project_title = dom.get_element(selenium, PROJECT_TITLE)
    assert project_title.text == open_project
    assert re.match("^YOYO", project_title.text) is not None
