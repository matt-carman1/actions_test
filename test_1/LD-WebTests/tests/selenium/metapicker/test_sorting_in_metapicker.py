import pytest

from helpers.change.live_report_picker import open_metapicker, sort_metapicker_column
from helpers.selection.live_report_picker import REPORT_LIST_TITLE, REPORT_LIST_ID, REPORT_PICKER, \
    REPORT_LIST_AUTHOR, REPORT_LIST_LAST_EDITED
from helpers.verification.live_report_picker import verify_sorted_metapicker_column
from library import dom


@pytest.mark.usefixtures("open_project")
def test_sorting_in_metapicker(selenium):
    """
    Test sorting data in LR Metapicker in ascending and descending order by: 
        * Last Edited date
        * Live Report Name
        * Live Report ID (alias)
        * Author.

    :param selenium: Webdriver
    :return:
    """

    # Open Metapicker and navigate to 'Test Sorting' Folder
    open_metapicker(selenium)
    picker = dom.get_element(selenium, REPORT_PICKER)
    dom.click_element(picker, 'a', 'Test Sorting')

    # ------ Test Sorting in Metapicker ------ #

    # LRs in Metapicker are sorted by Last Edited in descending order (Default sort order)
    # Note: We are Verifying the sort order using the alias(ID) because of an issue: SS-25305 we observed.
    verify_sorted_metapicker_column(selenium, REPORT_LIST_ID, 'ID', ['2305', '2306', '2309', '2307', '2308'])

    # Ascend sort by Last Edited
    sort_metapicker_column(picker, REPORT_LIST_LAST_EDITED, 'Last Edited', desc=False)
    # Verifying the sort order using the alias(ID) because of an issue: SS-25305 we observed.
    verify_sorted_metapicker_column(selenium, REPORT_LIST_ID, 'ID', ['2308', '2307', '2309', '2306', '2305'])

    # Ascend sort by Name
    sort_metapicker_column(picker, REPORT_LIST_TITLE, 'Name')
    verify_sorted_metapicker_column(picker, REPORT_LIST_TITLE, 'Name',
                                    ['1 compound', '9 compounds', '10 compounds', 'AA', 'zz'])

    # Descend sort by Name
    sort_metapicker_column(picker, REPORT_LIST_TITLE, 'Name', desc=True)
    verify_sorted_metapicker_column(picker, REPORT_LIST_TITLE, 'Name',
                                    ['zz', 'AA', '10 compounds', '9 compounds', '1 compound'])

    # Ascend sort by ID
    sort_metapicker_column(selenium, REPORT_LIST_ID, 'ID')
    verify_sorted_metapicker_column(selenium, REPORT_LIST_ID, 'ID', ['2305', '2306', '2307', '2308', '2309'])

    # Descend sort by ID
    sort_metapicker_column(selenium, REPORT_LIST_ID, 'ID', desc=True)
    verify_sorted_metapicker_column(selenium, REPORT_LIST_ID, 'ID', ['2309', '2308', '2307', '2306', '2305'])

    # Ascend sort by Username
    sort_metapicker_column(selenium, REPORT_LIST_AUTHOR, 'Author')
    verify_sorted_metapicker_column(selenium, REPORT_LIST_AUTHOR, 'Author', ['demo', 'demo', 'userB', 'userB', 'userC'])

    # Descend sort by Username
    sort_metapicker_column(selenium, REPORT_LIST_AUTHOR, 'Author', desc=True)
    verify_sorted_metapicker_column(selenium, REPORT_LIST_AUTHOR, 'Author', ['userC', 'userB', 'userB', 'demo', 'demo'])
