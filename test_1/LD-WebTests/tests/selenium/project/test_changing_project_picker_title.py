import pytest

from helpers.verification.element import verify_is_visible
from library.base import go_to_project_picker

project_picker_title = 'Test Changing title'
LD_PROPERTIES = {'PROJECT_PICKER_AREA_TITLE': project_picker_title}


@pytest.mark.usefixtures('login_to_livedesign')
@pytest.mark.usefixtures('customized_server_config')
def test_changing_project_picker_title(selenium):
    """
    Test changing the project picker area title but setting some text to the FeatureFlag PROJECT_PICKER_AREA_TITLE.
    :param selenium: Selenium Webdriver
    """

    project_picker_dialog = go_to_project_picker(selenium)

    # Verify that the project picker has a new title.
    verify_is_visible(project_picker_dialog,
                      '#therapeutic-search .project-picker-column-header',
                      selector_text=project_picker_title.upper())
