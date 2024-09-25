"""
This test performs a series of operations to check the urls are properly set on selecting projects and
live reports and again checking the reverse functionality, i.e., on hitting the url of a livereport, it opens
properly as verified from the UI
"""

import pytest

from helpers.change.live_report_picker import open_live_report
from helpers.change.project import open_project
from helpers.selection.grid import GRID_ALL_ROWS_CHECKBOX
from helpers.selection.modal import MODAL_DIALOG
from helpers.verification.live_report_picker import verify_live_report_tab_present
from library import wait


@pytest.mark.smoke
def test_project_and_lr_aware_url(selenium, login_to_livedesign):
    """
    Test URLs:
    1. Login into LD and Open the Project Picker.
    2. Select Global project to Open and verify the URL is correct.
    3. Open a LiveReport and verify the URL is as expected.
    4. Open Project Picker and select a different Project and verify that the URL is correct.
    5. Open a LiveReport and verify the URL is as expected.
    6. set the URL hash and verify the correct project and LiveReport opens.
    """
    custom_timeout = 5
    # ProjectID = 0
    open_project(selenium, 'Global')
    wait.until_not_visible(selenium, MODAL_DIALOG)
    current_url_hash = selenium.current_url.partition('#/')[2]
    assert current_url_hash == 'projects/0'

    # LiveReportID = 865
    open_live_report(selenium, name='(Global) 20 Compounds 3 Assays')
    wait.until_not_visible(selenium, MODAL_DIALOG)
    wait.until_visible(selenium, GRID_ALL_ROWS_CHECKBOX, timeout=custom_timeout)
    current_url_hash = selenium.current_url.partition('#/')[2]
    assert current_url_hash == 'projects/0/livereports/865'

    # ProjectID = 4
    open_project(selenium, 'JS Testing')
    wait.until_not_visible(selenium, MODAL_DIALOG)
    current_url_hash = selenium.current_url.partition('#/')[2]
    assert current_url_hash == 'projects/4'

    # LiveReportID = 2248
    open_live_report(selenium, name='5 Fragments 4 Assays')
    wait.until_not_visible(selenium, MODAL_DIALOG)
    wait.until_visible(selenium, GRID_ALL_ROWS_CHECKBOX, timeout=custom_timeout)
    current_url_hash = selenium.current_url.partition('#/')[2]
    assert current_url_hash == 'projects/4/livereports/2248'

    # Set URL directly and check if correct LR opens
    url_partitions = selenium.current_url.partition('#')
    new_url = url_partitions[0] + url_partitions[1] + 'projects/0/livereports/873'
    selenium.get(new_url)
    wait.until_visible(selenium, GRID_ALL_ROWS_CHECKBOX, timeout=custom_timeout)
    verify_live_report_tab_present(selenium, '(Global) 100 Compounds 10 Assays')
