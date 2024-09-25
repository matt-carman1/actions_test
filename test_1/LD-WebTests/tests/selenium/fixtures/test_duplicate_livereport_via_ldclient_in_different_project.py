import time

import pytest

from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.selection.project import PROJECT_TITLE
from library import dom

live_report_to_duplicate = {'livereport_name': '20 Compounds 2 Poses', 'livereport_id': '868'}
test_project_id = 2
test_project_name = 'Project A'


@pytest.mark.skip(name="skip_report", reason="Test for fixture but skipping it to reduce the run time of test suite")
def test_duplicate_livereport_via_ldclient_in_different_project(selenium, duplicate_live_report, open_livereport):
    """
    Basic Test for duplicate_live_report_via_ldclient fixture by duplicating the LR in the JS Testing Project but
    performing everything for a different project than 'JS Testing'.

    :param selenium: Selenium Webdriver
    """

    assert dom.get_element(selenium, PROJECT_TITLE).text == test_project_name
    assert duplicate_live_report

    time.sleep(2)
    assert dom.get_element(selenium, TAB_ACTIVE).text == duplicate_live_report
