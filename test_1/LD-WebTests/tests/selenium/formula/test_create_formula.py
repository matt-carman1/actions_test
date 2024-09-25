import pytest

from helpers.change.formula_actions import create_a_custom_formula, make_custom_edit_to_formula, create_expression
from helpers.selection.grid import Footer
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from helpers.verification.grid import verify_footer_values, verify_column_contents, check_for_butterbar

live_report_to_duplicate = {'livereport_name': 'Import Data', 'livereport_id': '878'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('duplicate_live_report')
def test_create_formula(selenium):
    """
    Test creating and editing a formula.
        1. Create a custom formula and add it to the LR
        2. Check the formula is not searchable in D&C Tree
        3. Verify the formula column content.
        4. Edit the formula created and then save it.
        5. Verify the formula column content.
    """
    formula_name = 'Log and add five'

    # Create a formula based on the numeric column-IT Solubility (undefined)
    formula_expression = create_a_custom_formula(
        selenium,
        formula_name,
        lambda driver: create_expression(driver, 'log', 'IT Solubility (undefined)', '+ 5'),
        description='Testing Description',
        output_data_type='Number',
        is_publish=False)

    # Check the formula expression is correct
    assert formula_expression == 'log(IT Solubility (undefined))+ 5'

    # Check for the butter bar to appear
    check_for_butterbar(selenium, notification_text='Adding column {}'.format(formula_name))
    # Check for the butter bar to go away
    check_for_butterbar(selenium, notification_text='Adding column {}'.format(formula_name), visible=False)

    # Verify that the Formula is added by checking the footer values
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })

    # Since this is an unpublished formula, it should not be searchable in D&C Tree
    verify_no_column_exists_in_column_tree(selenium, formula_name)

    # Verify contents of the Formula column
    verify_column_contents(selenium, formula_name, ['6.48', '6.61'])

    # Editing the formula
    new_formula_expression = make_custom_edit_to_formula(selenium,
                                                         formula_name,
                                                         expression=' * 2',
                                                         is_only_expression=True)
    assert new_formula_expression == 'log(IT Solubility (undefined))+ 5 * 2'

    # Check for the butter bar
    check_for_butterbar(selenium, notification_text='Saving Formula')
    # Check for the butter bar
    check_for_butterbar(selenium, notification_text='Saving Formula', visible=False)

    # Verify contents of the Formula column
    verify_column_contents(selenium, formula_name, ['11.48', '11.61'])
