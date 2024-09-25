import time

import pytest
from helpers.change.project_landing_page import delete_bookmark, switch_to_landing_page_bookmark_tab
from helpers.change import project_landing_page
from helpers.selection.project_landing_page import BookmarkDialog
from helpers.verification.project_landing_page import verify_is_bookmark_present, verify_is_bookmark_absent
from library import wait
from library.utils import make_unique_name


@pytest.mark.usefixtures('login_to_livedesign')
def test_create_project_landing_page(selenium):
    """
    Tests Project landing page , creates and saves a new bookmark. Validate the saved bookmark

    :param selenium: Selenium Webdriver
    """
    # Go to project landing page
    project_landing_page.open_project_landing_page(selenium)
    # Switch to bookmark tab
    switch_to_landing_page_bookmark_tab(selenium)
    # Details required for creating new bookmark
    bookmark_title = make_unique_name("Test Bookmark")
    lr_name = "50 Compounds 10 Assays"
    label = "sample"
    description = "Bookmarking a LR"
    # create a new bookmark
    project_landing_page.add_new_bookmark(selenium, bookmark_title, lr_name, label, description)
    # verify the saved bookmark
    verify_is_bookmark_present(selenium, bookmark_title)
    # Delete the created bookmark as part of teardown
    delete_bookmark(selenium, bookmark_to_be_deleted=bookmark_title)
    # verify if bookmark is deleted successfully
    verify_is_bookmark_absent(selenium, bookmark_title)
