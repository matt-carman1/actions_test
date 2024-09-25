import pytest

import time

from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.selection.project import PROJECT_TITLE
from library import dom

live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}
test_project_id = 4


@pytest.mark.skip(name="skip_report", reason="Test for fixture but skipping it to reduce the run time of test suite")
def test_duplicate_live_report_via_ldclient(selenium, duplicate_live_report, open_livereport):
    """
    Basic Test for duplicate_live_report_via_ldclient fixture by duplicating the LR in JS Testing project.
    :param selenium: Selenium Webdriver
    """
    assert dom.get_element(selenium, PROJECT_TITLE).text == 'JS Testing'
    assert duplicate_live_report

    time.sleep(2)
    assert dom.get_element(selenium, TAB_ACTIVE).text == duplicate_live_report
