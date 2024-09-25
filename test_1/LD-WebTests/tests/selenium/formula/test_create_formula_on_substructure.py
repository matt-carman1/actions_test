import pytest

from helpers.change.formula_actions import create_a_custom_formula
from helpers.extraction.grid import wait_until_cells_are_loaded
from helpers.flows.formula import select_function_import_sketcher
from helpers.selection.grid import Footer
from helpers.verification.formula import verify_compound_structure_image_count_on_formula_column

from helpers.verification.grid import verify_footer_values
from library.utils import make_unique_name

live_report_to_duplicate = {'livereport_name': 'Test Date Assay Column', 'livereport_id': '2699'}
test_report_name = 'Test Date Assay Column'


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
@pytest.mark.require_webgl
def test_create_formula_on_substructure(selenium):
    """
    Test case for creating a custom formula on a substructure.

    1. Creates a custom formula.
    2. Verify the created formula in the grid

    :param selenium: The Selenium WebDriver instance
    :type selenium: WebDriver
    :return: None
    :rtype: None
    """

    formula_name = make_unique_name("Formula")
    # create published formula
    create_a_custom_formula(selenium,
                            formula_name,
                            select_function_import_sketcher,
                            description='creating formula substructure search function and adding column to LR',
                            output_data_type='Structure Image')

    wait_until_cells_are_loaded(selenium, column_title=formula_name)

    # Verify the presence of the created formula in the data columns
    expected_compounds = 4
    verify_compound_structure_image_count_on_formula_column(selenium, expected_compounds)
    # Verify the footer values
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(4),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5)
        })
