"""
Selenium test to verify if the export options are visible from all loactions
"""

from library import dom
from library.simulate import hover, right_click

from helpers.verification.element import verify_is_visible
from helpers.change.live_report_menu import open_live_report_menu
from helpers.change.grid_row_actions import select_all_rows
from helpers.selection.grid import GRID_ROW_CHECKBOX_
from helpers.selection.grid_menus import SUB_MENU_ITEM
from helpers.selection.general import MENU_ITEM

live_report_to_duplicate = {'livereport_name': 'Coloring Rules', 'livereport_id': '879'}


def test_exporting_lr_in_all_formats(selenium, duplicate_live_report, open_livereport):
    """
    Testing that the  export options are available for all chemical file formats
    :param selenium: Selenium Webdriver
    :param duplicate_live_report: The duplicate_live_report created
    """

    # Verify that the Export options are available from the LR dropdown
    open_live_report_menu(selenium, duplicate_live_report)
    elem = dom.get_element(selenium, MENU_ITEM, text='Export Report')
    hover(selenium, elem)
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='CSV')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='SDF')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='XLS', exact_selector_text_match=True)
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='XLS (Aligned)')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='PPTX')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='PDF')

    # Verify that the Export options are available from the row dropdown
    # Testing only for sub_menu_text CSV
    select_all_rows(selenium)
    verify_row_submenu_options(selenium, entity_id='CRA-031437', menu_text='Export as', sub_menu_text='CSV...')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='SDF...')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='XLS...', exact_selector_text_match=True)
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='XLS (Aligned)...')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='PPTX...')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='PDF...')

    # Verify that the Export options are available from the row dropdown for one selected compound
    select_all_rows(selenium)
    verify_row_submenu_options(selenium, entity_id='CRA-031437', menu_text='Export as', sub_menu_text='CSV...')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='SDF...')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='XLS...', exact_selector_text_match=True)
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='XLS (Aligned)...')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='PPTX...')
    verify_is_visible(selenium, SUB_MENU_ITEM, selector_text='PDF...')


def verify_row_submenu_options(driver, entity_id, menu_text=None, sub_menu_text=None):
    """
    This function does the following :
    a) Selects a compound.
    b) Right-clicks it.
    c) Navigates through the row menu and sub-menu.
    d) Ensures that the sub-menu options are visible.

    Navigating through the row submenu
    :param driver: Selenium Webdriver
    :param entity_id: str, The entity id on which the right click is to be done.
    :param menu_text: str, The immediate menu option to hover
    :param sub_menu_text: str, The sub_menu option to verify if visible or not.
    """

    element = dom.get_element(driver, GRID_ROW_CHECKBOX_.format(entity_id))
    right_click(element)
    menu_to_hover = dom.get_element(driver, MENU_ITEM, text=menu_text)
    hover(driver, menu_to_hover)
    verify_is_visible(driver, SUB_MENU_ITEM, selector_text=sub_menu_text)
