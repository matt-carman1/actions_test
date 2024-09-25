import pytest

from helpers.change.formula_actions import create_a_custom_formula, add_expression_to_formula, create_expression
from helpers.change.grid_column_menu import click_column_menu_item, open_edit_formula_window
from helpers.change.live_report_picker import open_live_report
from helpers.change.project import open_project
from helpers.selection.formula import FORMULA_SAVE_BUTTON
from helpers.selection.grid import ColumnMenuOptionName
from helpers.verification.data_and_columns_tree import verify_column_exists_in_column_tree
from helpers.verification.element import verify_column_menu_items_visible
from helpers.verification.grid import verify_column_contents
from library import dom, utils
from library.authentication import login, logout

test_username = 'userC'
test_password = 'userC'
live_report_to_duplicate = {'livereport_name': 'Test Date Assay Column', 'livereport_id': '2699'}


@pytest.mark.k8s_defect(reason="SS-43928: Duplicates shown in column tree for newly created Formulas")
@pytest.mark.smoke
def test_published_formula(selenium, duplicate_live_report, open_livereport):
    """
    Test published formula with different users.

    1. test formula with the user who is author and also publishes the formula but is a non-admin user.
    2. test formula with the user who is neither an author nor an admin user.
    3. test formula with admin user.
    :param selenium: a fixture that returns Selenium Webdriver
    :param duplicate_live_report: fixture that duplicates live report
    :return:
    """

    # ----- test formula with the user who is author and also publishes the formula but is a non-admin user ----- #
    formula_name = utils.make_unique_name('Formula_On_number')
    # create published formula
    create_a_custom_formula(selenium,
                            formula_name,
                            lambda driver: create_expression(driver, 'log', 'Test Dates Assay (value)', '*2'),
                            description='description for formula testing',
                            output_data_type='Number',
                            is_publish=True)

    # verification of formula column in D&C tree
    verify_column_exists_in_column_tree(selenium, formula_name, search_retries=3)

    # Verify the contents of the formula
    verify_column_contents(selenium, formula_name, ['0', '0.602', '0.954', '1.2'])

    # Editing expression of the formula
    click_column_menu_item(selenium, formula_name, ColumnMenuOptionName.EDIT_FORMULA)
    add_expression_to_formula(selenium, '+2')
    dom.click_element(selenium, FORMULA_SAVE_BUTTON, text='Save', exact_text_match=True)

    # verifying formula column values based on expression
    verify_column_contents(selenium, formula_name, ['2', '2.6', '2.95', '3.2'])

    logout(selenium)

    # ----- test formula with the user who is neither an author nor an admin user ----- #
    # login with the user who is neither an author nor an admin user
    login(selenium, 'userB', 'userB')
    open_project(selenium, 'JS Testing')
    open_live_report(selenium, name=duplicate_live_report)
    # verifying 'Edit Formula' not present for the user who is neither an author nor an admin user
    verify_column_menu_items_visible(selenium,
                                     formula_name,
                                     menu_items=[ColumnMenuOptionName.EDIT_FORMULA],
                                     is_present=False,
                                     close_menu_at_the_end=False)
    # verifying 'View Formula' is present for the user who is neither an author nor an admin user
    verify_column_menu_items_visible(selenium, formula_name, menu_items=[ColumnMenuOptionName.VIEW_FORMULA])

    logout(selenium)

    # ----- test formula with admin user ----- #
    # login with admin user
    login(selenium, 'demo', 'demo')
    open_project(selenium, 'JS Testing')
    open_live_report(selenium, name=duplicate_live_report)

    # opening edit formula window by clicking Edit Formula menu item and verifying whether it is opened
    open_edit_formula_window(selenium, formula_name)

    # Editing expression of the formula
    add_expression_to_formula(selenium, '-2')
    dom.click_element(selenium, FORMULA_SAVE_BUTTON, text='Save', exact_text_match=True)
    # verifying formula column values based on expression
    verify_column_contents(selenium, formula_name, ['0', '0.602', '0.954', '1.2'])
