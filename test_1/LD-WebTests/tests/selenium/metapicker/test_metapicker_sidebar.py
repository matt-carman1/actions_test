import pytest

from helpers.change.live_report_picker import open_metapicker, close_metapicker
from helpers.verification.live_report_picker import verify_count_of_live_report_per_folder

test_username = 'userC'
test_password = 'userC'
test_project_name = 'Project B'
test_report_project_id = '3'
test_report_is_private = True


@pytest.mark.app_defect(reason='SS-42590: Failing due to LRs left behind by test_copy_live_report_role')
@pytest.mark.serial
@pytest.mark.usefixtures("open_project")
@pytest.mark.usefixtures("new_live_report")
def test_metapicker_sidebar(selenium):
    """
    Tests availabilities of UI options in the metapicker sidebar:
    1. Open the LR Metapicker
    2. Verify sidebar folders are visible and clickable
        . All LiveReports
        . Authored by me
        . Private to me
        . Project B Home
    3. Click on "All LiveReports", check the count of the LRs is 2
    4. Click on "Authored by me", check that the count of LRs is 1
    5. Click on "Private to me", check that the count of LRs is 1
    6. Click on "Project B Home", check that the count of LRs is 1

    :param selenium: Webdriver
    """

    # Open the LR Metapicker
    open_metapicker(selenium)

    # Verify sidebar folders are visible and clickable, and check the count of LRs
    verify_count_of_live_report_per_folder(selenium, {
        'All LiveReports': 2,
        'Authored by me': 1,
        'Private to me': 1,
        'Project B Home': 1
    })

    close_metapicker(selenium)
