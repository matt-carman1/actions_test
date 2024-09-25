import pytest
from library import dom
from library.eventually import eventually_equal

from helpers.change.live_report_menu import click_live_report_menu_item, close_live_report
from helpers.selection.modal import DUPLICATE_LR_RADIO_BUTTON_LABEL, MODAL_LR_COLUMN_SEARCH_BOX, \
    MODAL_LR_COLUMN_SEARCH_BOX_SEARCH_ICON, MODAL_LR_COLUMN_SEARCH_BOX_CLEAR_BUTTON, \
    MODAL_LR_COLUMN_SEARCH_BOX_INPUT, MODAL_LR_COLUMNS_LIST, MODAL_LR_COLUMN_SELECTION_LINK, \
    MODAL_DIALOG_BUTTON
from helpers.verification.element import verify_is_visible
from helpers.verification.live_report import verify_columns_visible_in_duplicate_lr_dialog

test_livereport = '3 Compounds 2 Poses'


@pytest.mark.usefixtures('open_livereport')
def test_duplicate_livereport_dialog_search_box(selenium):
    """
    Test search box in duplicate live report dialog

    1. Opening the duplicate LR dialog
    2. click 'Choose Subset' option and verify search box
    3. Test single character search and verify results
    4. Test entire column name search and verify results
    5. Remove text using X button and verify results
    6. test invalid column name search and verify the message

    :param selenium: Selenium webdriver
    """
    # ----- Opening the duplicate LR dialog ----- #
    click_live_report_menu_item(selenium, test_livereport, 'Duplicate...')

    dom.click_element(selenium, DUPLICATE_LR_RADIO_BUTTON_LABEL, text='Choose Subset')

    # ---- click 'Choose Subset' option and verify search box ----- #
    verify_is_visible(selenium, MODAL_LR_COLUMN_SEARCH_BOX)
    verify_is_visible(selenium, MODAL_LR_COLUMN_SEARCH_BOX_SEARCH_ICON)
    verify_is_visible(selenium, MODAL_LR_COLUMN_SEARCH_BOX_CLEAR_BUTTON)

    # ----- Test single character search and verify results ----- #
    dom.set_element_value(selenium, MODAL_LR_COLUMN_SEARCH_BOX_INPUT, value='r')
    verify_columns_visible_in_duplicate_lr_dialog(selenium, ['Fake 3D model with 2 Poses (Docking Score)'])

    # ----- Test entire column name search and verify results ----- #
    dom.set_element_value(selenium,
                          MODAL_LR_COLUMN_SEARCH_BOX_INPUT,
                          value='Fake 3D model with 2 Poses (3D)',
                          clear_existing_value=True)
    verify_columns_visible_in_duplicate_lr_dialog(selenium, ['Fake 3D model with 2 Poses (3D)'])

    # ----- Remove text using X button and verify results ----- #
    dom.click_element(selenium, MODAL_LR_COLUMN_SEARCH_BOX_CLEAR_BUTTON)
    # verify text removed from input box
    verify_is_visible(selenium, MODAL_LR_COLUMN_SEARCH_BOX_INPUT, selector_text='')
    # verify all columns visible in columns section
    verify_columns_visible_in_duplicate_lr_dialog(selenium, [
        'Lot Scientist', 'Fake 3D model with 2 Poses (3D)', 'Fake 3D model with 2 Poses (Docking Score)',
        'Model async (3D)'
    ])

    # ----- test invalid column name search and verify the message ----- #
    dom.set_element_value(selenium, MODAL_LR_COLUMN_SEARCH_BOX_INPUT, value='invalid column')

    # When No columns found, the message is located in pseudocode element(::after), So using javascript to extracting
    # pseudocode element content and using it for verification
    def get_pseudocode_element_content(driver):
        return driver.execute_script(
            """return window.getComputedStyle(document.querySelector(arguments[0]), 
            ':after').getPropertyValue('content')""", MODAL_LR_COLUMNS_LIST)

    assert eventually_equal(selenium,
                            get_pseudocode_element_content,
                            expected_value='"No columns match the search filter."')

    # ----- Search with substring when columns are selected ----- #
    # select all columns using column selection buttons
    dom.click_element(selenium, MODAL_LR_COLUMN_SELECTION_LINK, text='All')
    dom.set_element_value(selenium, MODAL_LR_COLUMN_SEARCH_BOX_INPUT, value='pose', clear_existing_value=True)
    verify_columns_visible_in_duplicate_lr_dialog(
        selenium, ['Fake 3D model with 2 Poses (3D)', 'Fake 3D model with 2 Poses (Docking Score)'])
    # clicking cancel button of duplicate live report dialog
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, 'Cancel')
    # close live report
    close_live_report(selenium, test_livereport)
