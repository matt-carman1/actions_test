from helpers.selection.add_compound_panel import IMPORT_FROM_FILE_PLACEHOLDER_TITLE, IMPORT_FROM_FILE_INPUT_ELEMENT, \
    COMPOUND_SEARCH_BUTTON, COMPOUND_SEARCH_BY_ID_TEXTAREA
from helpers.selection.modal import MODAL_DIALOG_BODY_LABEL, OK_BUTTON
from library import dom, wait
from library.dom import select_cut_and_paste_text


def set_upload_file_path(driver, path_str):
    """
    Set the contents of the file upload input.

    Note that this function DOES NOT upload the file.

    :param driver: selenium webdriver
    :param path_str: the local path of the file to upload
    :return:
    """
    # Wait for the Import from File pane to appear
    wait.until_visible(driver, IMPORT_FROM_FILE_PLACEHOLDER_TITLE)
    file_input = dom.get_element(driver, IMPORT_FROM_FILE_INPUT_ELEMENT, must_be_visible=False)
    file_input.send_keys(path_str)


def search_and_add_compounds_by_pasting_id(driver, separator_option, compound_ids):
    """
    This method searches the compounds by ID where IDs are pasted in the textarea. Make sure to open
    the search by ID tab using open_search_by_id_tab().

    :param driver: Selenium Webdriver
    :param separator_option: str, 'Comma','None', 'White space', 'Semicolon', etc.
    :param compound_ids: str, containing compound IDs
     """
    search_by_id_textarea = dom.get_element(driver, COMPOUND_SEARCH_BY_ID_TEXTAREA)

    # Used Javascript to inject values because set_element_value was flaky when called multiple times in the test. It
    # was also not working fine in Firefox, so used this approach.
    driver.execute_script(
        """
                 var inputElement = arguments[0];
                 inputElement.value = arguments[1]; 
                 """, search_by_id_textarea, compound_ids)

    # We are clicking in the textarea to get the focus back there, otherwise the copy(cut-paste)
    # in the next line would try to copy everything on the page
    search_by_id_textarea.click()

    select_cut_and_paste_text(driver)
    # clicking on the given radio button
    dom.click_element(driver, MODAL_DIALOG_BODY_LABEL, text=separator_option, exact_text_match=True)
    dom.click_element(driver, OK_BUTTON)
    dom.click_element(driver, COMPOUND_SEARCH_BUTTON)
