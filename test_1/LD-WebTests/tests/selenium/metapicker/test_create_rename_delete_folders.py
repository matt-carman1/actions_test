"""
This test validates whether or not folders and subfolders in the Metapicker can be created, renamed, and deleted.
"""
from helpers.change.live_report_picker import open_metapicker, create_new_lr_folder, close_metapicker, create_subfolder, \
    delete_folder
from helpers.selection.general import MENU_ITEM
from helpers.selection.live_report_picker import METAPICKER_FOLDER, METAPICKER_FOLDER_MENU,\
    METAPICKER_FOLDER_ACTIVE_EXPANDER
from helpers.selection.modal import MODAL_WINDOW, OK_BUTTON
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from library import dom
from library.base import set_input_text


def test_create_rename_delete_folders(selenium, open_project):
    """
    Validates folders and their subfolders can be created, renamed, and deleted.

    This test:
    1. Creates a new folder
    2. renames the new folder
    3. creates a subfolder in the renamed folder
    4. renames the created subfolder
    5. deletes the renamed subfolder
    6. deletes the previously (renamed) folder only if it is empty
    """
    # ----- Test Setup ----- #
    open_metapicker(selenium)

    # ----- Verify created folder created via Metapicker exists ----- #
    folder_name = create_new_lr_folder(selenium, test_create_rename_delete_folders.__name__)
    verify_is_visible(selenium, METAPICKER_FOLDER, folder_name)

    # ----- Verify folder can be renamed ----- #
    folder_name_renamed = "renamed_{}".format(folder_name)
    # rename the folder and verify name
    _rename_folder(selenium, folder_name=folder_name, new_name=folder_name_renamed)
    verify_is_visible(selenium, METAPICKER_FOLDER, folder_name_renamed)

    # ----- Verify subfolder created ----- #
    subfolder_name = test_create_rename_delete_folders.__name__
    subfolder_name = create_subfolder(selenium, folder_name_renamed, subfolder_name)
    # expand folder to show subfolders
    dom.click_element(selenium, METAPICKER_FOLDER, folder_name_renamed)
    dom.click_element(selenium, METAPICKER_FOLDER_ACTIVE_EXPANDER)
    verify_is_visible(selenium, METAPICKER_FOLDER, subfolder_name)

    # ----- Verify subfolder can be renamed ----- #
    subfolder_name_renamed = 'renamed_{}'.format(subfolder_name)
    _rename_folder(selenium, folder_name=subfolder_name, new_name=subfolder_name_renamed)
    verify_is_visible(selenium, METAPICKER_FOLDER, subfolder_name_renamed)

    # ----- Verify a nested subfolder can't be created in a subfolder ----- #
    dom.click_element(selenium, METAPICKER_FOLDER, subfolder_name_renamed)
    dom.click_element(selenium, METAPICKER_FOLDER_MENU)
    verify_is_visible(selenium, "{}.disabled".format(MENU_ITEM), "Create Nested Folder")

    # ----- Verify folder can't be deleted if not empty ----- #
    dom.click_element(selenium, METAPICKER_FOLDER, folder_name_renamed)
    dom.click_element(selenium, METAPICKER_FOLDER_MENU)
    verify_is_visible(selenium, "{}.disabled".format(MENU_ITEM), "Delete Folder")

    # ----- Verify subfolder can be deleted ----- #
    delete_folder(selenium, subfolder_name_renamed)
    verify_is_not_visible(selenium, METAPICKER_FOLDER, subfolder_name_renamed)

    # ----- Verify an empty folder can be deleted ----- #
    delete_folder(selenium, folder_name_renamed)
    verify_is_not_visible(selenium, METAPICKER_FOLDER, folder_name_renamed)

    # ----- Teardown ----- #
    close_metapicker(selenium)


def _rename_folder(driver, folder_name, new_name):
    """
    Renames a folder or subfolder. Assumes the Metapicker is already open.

    :param driver: webdriver
    :param folder_name: str, name of the folder
    :param new_name: str, new name the folder will be renamed to
    """
    dom.click_element(driver, METAPICKER_FOLDER, folder_name)
    dom.click_element(driver, METAPICKER_FOLDER_MENU)
    dom.click_element(driver, MENU_ITEM, 'Rename Folder')
    set_input_text(driver, new_name, input_label='Folder name:')
    rename_folder_dialog = dom.get_element(driver, MODAL_WINDOW, 'Rename folder')
    dom.click_element(rename_folder_dialog, OK_BUTTON)
