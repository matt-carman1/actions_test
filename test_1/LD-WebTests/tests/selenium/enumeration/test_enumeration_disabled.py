"""
Selenium test for validating Enumeration Tab visibility
"""
import pytest

from helpers.change.actions_pane import open_tools_pane
from helpers.selection.actions_pane import TOOLS_PANE_TOOL
from helpers.verification.element import verify_is_visible, verify_is_not_visible

LD_PROPERTIES = {'ENABLE_ENUMERATION': 'false'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures('customized_server_config')
def test_enumeration_disabled(selenium):
    """
    Test that the enumeration tools aren't visible

    :param selenium: Selenium Webdriver
    """
    open_tools_pane(selenium)
    verify_is_not_visible(selenium, TOOLS_PANE_TOOL, 'R-Group')
    verify_is_not_visible(selenium, TOOLS_PANE_TOOL, 'Reaction')


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_enumeration_enabled(selenium):
    """
    Test that the enumeration tab is visible

    :param selenium: Selenium Webdriver
    """
    open_tools_pane(selenium)
    verify_is_visible(selenium, TOOLS_PANE_TOOL, 'R-Group', True)
    verify_is_visible(selenium, TOOLS_PANE_TOOL, 'Reaction', True)
