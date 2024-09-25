import pytest

from helpers.change.live_report_menu import make_live_report_hidden, make_live_report_visible, \
    click_live_report_menu_item
from helpers.change.live_report_picker import create_and_open_live_report, search_for_live_report, close_metapicker, \
    open_metapicker, open_live_report
from helpers.verification.live_report_picker import verify_private_icon_on_live_report, \
    verify_live_report_not_present, verify_live_report_tab_present
from helpers.change.project import open_project
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_DIALOG_BUTTON
from library.authentication import logout, login
from library.url import get_page_hash, set_page_hash
from library import dom


@pytest.mark.usefixtures("open_project")
def test_private_live_report(selenium):
    """
    Test creating and features of private LR.
    1. Set LR to private
    2. Private LR should be visible in 'Hidden from others' folder of metapicker
    3. Convert Private LR to Public LR and check its ACLs
    4. Private LR should not be searchable in metapicker for non-owner.
    5. Private LR accessible through URL for non-owner
    6. Non-Admin non-owner should not be able to rename, delete the LR whereas Non-owner user with Admin privileges
    should be able to do so.

    :param selenium: Webdriver
    :return:
    """

    # ----- Create a LiveReport and make it Private ----- #
    created_lr_name = create_and_open_live_report(selenium)

    # Make the LiveReport Hidden
    make_live_report_hidden(selenium, created_lr_name)

    # Verify Private LiveReport icon
    verify_private_icon_on_live_report(selenium, created_lr_name)

    # Get the URL of the LiveReport
    live_report_page_hash = get_page_hash(selenium)

    # Search for LiveReport in 'Hidden from others' folder in the Metapicker
    search_for_live_report(selenium, name=created_lr_name, directory='Hidden from others')
    close_metapicker(selenium)

    # Make LiveReport Visible
    make_live_report_visible(selenium, created_lr_name)

    # Check the LiveReport is no longer visible in 'Hidden from others' folder in the Metapicker
    open_metapicker(selenium)
    verify_live_report_not_present(selenium, created_lr_name, folder_name='Hidden from others')
    close_metapicker(selenium)

    # Make LiveReport Hidden again to test with different user
    make_live_report_hidden(selenium, created_lr_name)

    logout(selenium)

    # ----- Login as different user. Search and test for private LR ----- #
    login(selenium, uname='userB', pword='userB')
    open_project(selenium)  # Opens 'JS Testing Home' project by default

    open_metapicker(selenium)
    verify_live_report_not_present(selenium, created_lr_name)
    close_metapicker(selenium)

    # go_to_url(selenium, live_report_url)
    set_page_hash(selenium, live_report_page_hash)

    # Verify the LiveReport is open
    verify_live_report_tab_present(selenium, created_lr_name)

    # Renaming a private LR by non-owner non-admin is not allowed
    click_live_report_menu_item(selenium, created_lr_name, 'Rename')
    verify_is_not_visible(selenium,
                          MODAL_DIALOG_HEADER,
                          selector_text='Rename LiveReport',
                          message='Renaming a private LR by non-owner non-admin is prohibited')

    # Deleting a private LR by non-owner non-admin is not allowed
    click_live_report_menu_item(selenium, created_lr_name, 'Delete')
    verify_is_not_visible(selenium,
                          MODAL_DIALOG_HEADER,
                          selector_text='Delete LiveReport',
                          message='Deleting a private LR by non-owner non-admin is prohibited')

    # ----- Login as a different Admin user and search and test for private LR ----- #
    login(selenium, uname='seurat', pword='seurat')

    # Private LR should be searchable for non-owner Admin user
    open_project(selenium)  # Opens 'JS Testing Home' project by default
    open_live_report(selenium, name=created_lr_name)

    # Renaming a private LR by non-owner non-admin is allowed
    click_live_report_menu_item(selenium, created_lr_name, 'Rename')
    verify_is_visible(selenium,
                      MODAL_DIALOG_HEADER,
                      selector_text='Rename LiveReport',
                      message='Renaming a private LR by non-owner Admin is allowed')
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text='Cancel')

    # Deleting a private LR by non-owner non-admin is not allowed
    click_live_report_menu_item(selenium, created_lr_name, 'Delete')
    verify_is_visible(selenium,
                      MODAL_DIALOG_HEADER,
                      selector_text='Delete LiveReport',
                      message='Deleting a private LR by non-owner non-admin is prohibited')
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text='Cancel')
