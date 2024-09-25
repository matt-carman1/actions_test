import pytest

import time

from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.selection.project import PROJECT_TITLE
from library import dom

live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}
test_project_id = 4
test_username = 'userC'
test_password = 'userC'


@pytest.mark.skip(name="skip_report", reason="Test for fixture but skipping it to reduce the run time of test suite")
def test_duplicate_livereport_via_ldclient_different_user_login(selenium, duplicate_live_report, open_livereport):
    """
    Basic Test for duplicate_live_report_via_ldclient fixture by duplicating the LR in the JS Testing Project but
    logging in as a different user "userC".

    :param selenium:
    """

    assert dom.get_element(selenium, PROJECT_TITLE).text == 'JS Testing'
    assert dom.get_element(selenium, '#user-name-element').text == test_username
    assert duplicate_live_report

    time.sleep(2)
    assert dom.get_element(selenium, TAB_ACTIVE).text == duplicate_live_report
