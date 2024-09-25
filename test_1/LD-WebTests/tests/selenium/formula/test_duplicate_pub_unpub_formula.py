import pytest
from helpers.change.formula_actions import create_expression, create_formula_and_wait_for_cells_to_load
from helpers.change.live_report_menu import switch_to_live_report
from helpers.flows.live_report_management import copy_active_live_report, duplicate_livereport
from helpers.verification.grid import verify_column_contents
from library import utils
from tests.selenium.formula.test_create_formula import make_custom_edit_to_formula

test_livereport = 'Test Date Assay Column'
verification_data = {
    'original_published': ['0', '0.602', '0.954', '1.2'],
    'original_unpublished': ['0', '0.602', '0.954', '1.2'],
    'edited_published': ['2', '2.3', '2.48', '2.6'],
    'edited_unpublished': ['2', '2.3', '2.48', '2.6']
}


@pytest.mark.usefixtures('open_livereport')
def test_duplicate_pub_unpub_formula(selenium):
    """
    test to duplicate an LR containing a Published and an Unpublished formula column

    :param selenium: Selenium WebDriver instance.
    :type selenium: selenium.webdriver.WebDriver
    :param duplicate_live_report: Details of the live report to be duplicated.
    :type duplicate_live_report: dict
    :param open_livereport: Details of the live report to be opened for initial testing.
    :type open_livereport: dict
    """
    duplicated_lr = duplicate_livereport(selenium, livereport_name=test_livereport)
    formula_pub_name = utils.make_unique_name('Formula_on_number_pub')
    formula_unpub_name = utils.make_unique_name('Formula_on_number_unpub')
    create_formula_and_wait_for_cells_to_load(
        selenium,
        formula_pub_name,
        lambda driver: create_expression(driver, 'log', 'Test Dates Assay (value)', '*2'),
        is_publish=True)
    create_formula_and_wait_for_cells_to_load(
        selenium,
        formula_unpub_name,
        lambda driver: create_expression(driver, 'log', 'Test Dates Assay (value)', '*2'),
        is_publish=False)
    # Duplicate the specified live report to create a new live report.
    copy_active_live_report(selenium, duplicated_lr, 'formula copy')

    # Verify the content of the original published and unpublished live report formulas in the copied live report.
    verify_column_contents(selenium, formula_pub_name, verification_data['original_published'])
    verify_column_contents(selenium, formula_unpub_name, verification_data['original_unpublished'])

    # Make custom edit by adding "+2" to the formula to increment the values by 2 in the copied Live Report.
    make_custom_edit_to_formula(selenium,
                                formula_column_name=formula_pub_name,
                                formula_function='log',
                                formula_column='Test Dates Assay (value)',
                                expression='+2',
                                is_exp_box_clear=True,
                                characters_to_remove=35)
    make_custom_edit_to_formula(selenium,
                                formula_column_name=formula_unpub_name,
                                formula_function='log',
                                formula_column='Test Dates Assay (value)',
                                expression='+2',
                                is_exp_box_clear=True,
                                characters_to_remove=35)

    # Verify the content of the edited formulas in the copied live report.
    verify_column_contents(selenium, formula_pub_name, verification_data['edited_published'])
    verify_column_contents(selenium, formula_unpub_name, verification_data['edited_unpublished'])

    # Switching back to original live report.
    switch_to_live_report(selenium, duplicated_lr)
    verify_column_contents(selenium, formula_pub_name, verification_data['edited_published'])
    verify_column_contents(selenium, formula_unpub_name, verification_data['original_unpublished'])

    # Open the edit formula window for the published formula, remove the whole formula expression and keep the first
    # expression which is "log(Test Dates Assay (value))*2" and save the changes in the original live report.
    make_custom_edit_to_formula(selenium,
                                formula_column_name=formula_pub_name,
                                formula_function='log',
                                formula_column='Test Dates Assay (value)',
                                expression='*2',
                                is_exp_box_clear=True,
                                characters_to_remove=35)

    # Verify the content of the published formula in the original live report.
    verify_column_contents(selenium, formula_pub_name, verification_data['original_published'])
