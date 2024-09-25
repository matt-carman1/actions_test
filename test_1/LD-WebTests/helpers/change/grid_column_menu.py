from helpers.change.grid_columns import scroll_to_column_header
from helpers.change.menus import click_submenu_option
from helpers.selection.coloring_rules import COLOR_RULES_DIALOG
from helpers.selection.general import MENU_ITEM
from helpers.selection.grid import GRID_HEADER_DROPDOWN_MENU, GRID_COLUMN_MENU_OPEN, GRID_HEADER_CELL
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.selection.modal import WINDOW_HEADER_TEXT, MODAL_DIALOG_HEADER
from library import dom, wait, simulate, base

ASC = 'Ascending'
DESC = 'Descending'


def open_coloring_rules(driver, column_name):
    """
    Open coloring rules for the named column

    :param driver: webdriver
    :param column_name: name of the column to color.
    """
    click_column_menu_item(driver, column_name, 'Color', 'Edit Coloring Rules…')
    wait.until_visible(driver, COLOR_RULES_DIALOG)


def sort_grid_by(driver, column_name, sort_ascending=True):
    """
    Sort the grid by the named column, in either direction

    :param driver: webdriver
    :param column_name: name of the column to sort by.
    :param sort_ascending: Boolean, default True, for whether we should sort
                           ascending (True) or descending.
    """
    direction = ASC if sort_ascending else DESC
    click_column_menu_item(driver, column_name, 'Sort', direction, exact_text_match=True)
    wait.until_loading_mask_not_visible(driver)


def toggle_show_smiles(driver):
    """
    Press the "Show as text" menu item in the Compound Structure column drop down
    menu. This will either show or hide the smiles representation of the
    structure.

    :param driver: webdriver
    """
    click_column_menu_item(driver, 'Compound Structure', 'Show as text')


def hide_column(driver, column_name):
    """
    Press the "Hide" menu item in the specified column's drop down
    menu.

    :param driver: webdriver
    :param column_name: name of the column to sort by.
    """
    click_column_menu_item(driver, column_name, 'Hide')


def freeze_a_column_via_menu_option(driver, column_name):
    """
    Press the "Freeze" menu item in the specified column's drop down
    menu.

    :param driver: webdriver
    :param column_name: name of the column to freeze.
    """
    click_column_menu_item(driver, column_name, 'Freeze')


def click_column_menu_item(driver, column_name, column_option_name, submenu_name=None, exact_text_match=False):
    """
    Scrolls to the column header into view then it opens the column context menu
    and then selects the menu item or sub-menu item by name.

    :param driver: webdriver
    :param column_name: str, column title
    :param column_option_name: str, column menu item label
    :param submenu_name: str, column menu item's sub menu label
    :param exact_text_match: bool, Whether text match should be exact or not. Disabled by default.
    """
    open_column_menu(driver, column_name)

    if submenu_name:
        click_submenu_option(driver, column_option_name, submenu_name, exact_text_match)
    else:
        # click the column menu item
        dom.click_element(driver, MENU_ITEM, column_option_name, exact_text_match=exact_text_match)


def open_limiting_condition_dialog(driver, column_name, sub_menu):
    """
    Navigate to "Limit Assay Data" option from column context menu and open Limited Assay Column
    dialog. This option is only available for assay columns.

    :param driver: Webdriver
    :param column_name: str, Assay Column for which the Define Limiting Condition dialog needs to be
                        opened
    :param sub_menu: str, column menu item's sub menu label. Limit Assay Data currently has two
                     sub-menu options Viz. Define Limiting Conditions and Edit Limiting
                     Conditions with latter being only available for existing limiting assay column.
    """

    # Open "Define Limiting Conditions" sub-menu item
    click_column_menu_item(driver, column_name, "Limit Assay Data", sub_menu)
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text="Create Limited Assay Column")


def open_reorder_column_dialog(driver, column_name):
    """
    Navigate to "Reorder Columns…" option from column context menu and open "Reorder Column"
    dialog.

    :param driver: Webdriver
    :param column_name: str, Column from where the Reorder Column dialog needs to be opened
    """

    # Open "Reorder Columns" menu item
    click_column_menu_item(driver, column_name, "Reorder Columns…")
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text="Reorder Columns")


def open_show_or_hide_column_menu(driver, column_name, sub_menu, exact_text_match=True):
    """
    Wrapping click_column_menu_item function to navigate to "Columns" option from column context
    menu and then show or hide columns from there.

    :param driver: Webdriver
    :param column_name: str, Column for which the the context menu needs to be accessed
    :param sub_menu: str, column menu item's sub menu label
    :param exact_text_match: bool, Whether text match should be exact or not. Disabled by default.
    """

    # Open "Reorder Columns" menu item and show a column.
    click_column_menu_item(driver, column_name, "Columns", sub_menu, exact_text_match=exact_text_match)


def open_edit_formula_window(driver, formula_column_name):
    """
    Click on the Formula Column context menu, navigate and click on 'Edit Formula…'

    :param driver: Selenium Webdriver
    :param formula_column_name: str, name of the formula column to edit
    :return:
    """

    click_column_menu_item(driver, column_name=formula_column_name, column_option_name='Edit Formula…')
    wait.until_visible(driver, WINDOW_HEADER_TEXT, text='Edit Formula Column')


def open_edit_mpo_window(driver, mpo_column_name):
    """
    Click on the MPO Column context menu, navigate and click on 'Edit MPO…'

    :param driver: Selenium Webdriver
    :param mpo_column_name: str, name of the MPO column to edit
    :return:
    """

    click_column_menu_item(driver, column_name=mpo_column_name, column_option_name='Edit MPO…')
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Edit Existing Multi-Parameter Optimization')


def toggle_cell_aggregation(driver, column_name, aggregation='Default'):
    options = ("Median", "Mean(Arithmetic)", "Mean(Geometric)", "Min", "Max", "Std Dev", "Count", "Latest Result",
               "Unaggregated")

    assert aggregation in options, "{} is not a cell aggregation option.".format(aggregation)

    # click the column menu item
    click_column_menu_item(driver, column_name, "Aggregate Values By", aggregation)


def open_group_column_dialog(driver, column_name):
    """
    Navigate to "Group" option from column context menu and open Group Name dialog.

    :param driver: Webdriver
    :param column_name: str, Column name from which Group dialog needs to be opened
    """

    # Open "Group" Dialog
    click_column_menu_item(driver, column_name, column_option_name='Group…', exact_text_match=True)
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Name Group')


def ungroup_columns(driver, group_column_name):
    """
    Navigate to the "Ungroup" option of the column group and clicks it. This option is only available for
    column group.

    :param driver: Selenium Webdriver
    :param group_column_name: str, group name
    :return:
    """
    click_column_menu_item(driver, column_name=group_column_name, column_option_name='Ungroup', exact_text_match=True)


def ungroup_column(driver, column_name):
    """
    Navigate to the "Ungroup" option of the column context menu and clicks it. This option is only available for
    individual columns that are part of a column group.

    :param driver: Selenium Webdriver
    :param column_name: str, column name
    :return:
    """
    click_column_menu_item(driver, column_name, column_option_name='Ungroup', exact_text_match=True)


def open_set_alignment_dialog(driver):
    """
    Navigate to "Set Alignment" option from the Compound column context menu and open the set alignment dialog.

    :param driver: Webdriver
    """
    click_column_menu_item(driver, 'Compound Structure', column_option_name='Set Alignment…', exact_text_match=True)
    wait.until_visible(driver, WINDOW_HEADER_TEXT, text='Set Alignment for Compound Structures')


def open_column_menu(driver, column_name):
    """
    Scrolls to the column header and open the column context menu.
    :param driver: Selenium Webdriver
    :param column_name: str, column name for which the context menu needs to be opened.
    """

    column_header = scroll_to_column_header(driver, column_name)

    # simulate hover then click the button when it appears
    simulate.hover(driver, column_header)
    dom.click_element(driver, GRID_HEADER_DROPDOWN_MENU)
    wait.until_visible(driver, GRID_COLUMN_MENU_OPEN, timeout=2)


def close_column_menu(driver):
    """
    closing column menu by clicking on live report tab
    :param driver:
    :return:
    """
    # clicking on active live report tab to close the column menu
    dom.get_element(driver, TAB_ACTIVE)


def remove_column(driver, column_name):
    """
    Removes the given column from the LR via the Column context menu option "Remove".

    :param driver: Selenium Webdriver
    :param column_name: str, Name of the column to be removed from the grid via column context menu.
    :return:
    """

    column_header = dom.get_element(driver, GRID_HEADER_CELL, text=column_name)

    simulate.hover(driver, column_header)
    dom.click_element(driver, GRID_HEADER_DROPDOWN_MENU)

    dom.click_element(driver, MENU_ITEM, 'Remove', exact_text_match=True)

    wait.until_visible(driver, WINDOW_HEADER_TEXT, text='Confirm Remove Column')
    base.click_ok(driver)

    wait.until_not_visible(driver, GRID_HEADER_CELL, text=column_name)
