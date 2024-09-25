import pytest

from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.freeform_column_action import create_ffc, edit_ffc_cell
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from helpers.verification.grid import verify_column_contents
from library.utils import make_unique_name

live_report_to_duplicate = {'livereport_name': 'FFC Selenium Test LR', 'livereport_id': '2304'}


@pytest.mark.smoke
@pytest.mark.usefixtures('open_livereport')
@pytest.mark.usefixtures('duplicate_live_report')
def test_ffc_unpublished_bool(selenium):
    """
    Tests an unpublished boolean FFC. Verifies the FFC:
        1. is 'Unpublished' (not in the D&C Tree)
        2. retains boolean values set
        3. values set persist after page refresh
        4. values can be changed
    """
    # ----- Test setup ----- #
    ffc_name = make_unique_name('ffc_unpublished_boolean')

    # sort to make LR ordered
    sort_grid_by(selenium, 'ID')
    # create an unpublished boolean FFC
    create_ffc(selenium, column_name=ffc_name, column_type='True/false')

    # ----- Verify FFC is 'Unpublished' (not in the D&C Tree) ----- #
    verify_no_column_exists_in_column_tree(selenium, ffc_name)

    # ----- Verify FFC retains boolean values set ----- #
    edit_ffc_cell(selenium, ffc_name, 'CRA-031437', 'false', is_boolean=True)
    edit_ffc_cell(selenium, ffc_name, 'CRA-035504', 'true', is_boolean=True)
    expected_ffc_values = ['false', '', 'true', '', '']
    verify_column_contents(selenium, ffc_name, expected_content=expected_ffc_values)

    # ----- Verify FFC values persist after page refresh ----- #
    selenium.refresh()
    verify_column_contents(selenium, ffc_name, expected_content=expected_ffc_values)

    # ----- Verify FFC values can be changed ----- #
    # clear and change one value
    edit_ffc_cell(selenium, ffc_name, 'CRA-031437', '', is_boolean=True)
    edit_ffc_cell(selenium, ffc_name, 'CRA-035504', 'false', is_boolean=True)
    # verification of FFC values
    verify_column_contents(selenium, ffc_name, expected_content=['', '', 'false', '', ''])
