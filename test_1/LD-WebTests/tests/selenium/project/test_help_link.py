import pytest

from helpers.selection.actions_pane import HELP_LINK
from library import dom


@pytest.mark.usefixtures('open_project')
def test_help_link(selenium):
    """
    Test to check if the Help button (?) in the west panel works.
    :param selenium: Webdriver
    :return:
    """
    help_link = dom.get_element(selenium, HELP_LINK)
    assert help_link.get_attribute('href').endswith('documentation')
