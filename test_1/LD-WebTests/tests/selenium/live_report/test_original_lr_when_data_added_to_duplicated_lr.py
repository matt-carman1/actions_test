import pytest

from helpers.change.grid_column_menu import remove_column
from helpers.selection.grid import Footer
from library import base
from helpers.change.actions_pane import open_add_compounds_panel, open_add_data_panel
from helpers.change.columns_action import add_column_by_name
from helpers.change.grid_row_actions import select_rows_and_pick_context_menu_item
from helpers.change.live_report_picker import open_live_report
from helpers.change.sar_action import create_sar_scaffold
from helpers.flows.add_compound import search_by_id
from helpers.verification.grid import verify_footer_values

live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}


@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('duplicate_live_report')
def test_original_lr_when_data_added_to_duplicated_lr(selenium):
    """
    Test checks that the content of the original LR remains unchanged when the data is added to the duplicated LR.

    1. Add compounds and columns to the Duplicated LR
    2. Remove compounds and columns from the Duplicated LR
    3. Verify footer values in duplicated LR
    4. Switch to original LR
    5. Verify that columns count and compounds count have not changed

    :param selenium: Webdriver, a fixture that returned selenium webdriver
    """
    # ----- Add compounds and columns to the Duplicated LR ----- #
    # Add Compounds
    open_add_compounds_panel(selenium)
    search_by_id(selenium, 'CRA-032913, CRA-033084')

    # Add Columns
    open_add_data_panel(selenium)
    add_column_by_name(selenium, '(JS Testing) Test RPE MPO')
    add_column_by_name(selenium, 'Published Freeform Text Column')
    sar_02_molv3 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 8 8 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 R# -1.142571 -2.045714 0.000000 101 RGROUPS=(1 1)\nM  V30 2 C 0.095143 -1.332286 0.000000 0\nM  V30 3 C 0.096286 0.096286 0.000000 0\nM  V30 4 R# -1.140286 0.811429 0.000000 102 RGROUPS=(1 2)\nM  V30 5 C 1.334000 0.809429 0.000000 0\nM  V30 6 C 2.570571 0.094286 0.000000 0\nM  V30 7 C 2.569429 -1.334286 0.000000 0\nM  V30 8 C 1.331714 -2.047714 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 1 3 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 2 8\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    create_sar_scaffold(selenium, sar_02_molv3)

    # ----- Remove compounds and columns from the Duplicated LR ----- #
    # Remove Compounds
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['CRA-035000'], option_to_select='Remove')
    base.click_ok(selenium)

    # Remove Columns
    remove_column(selenium, "Fake 3D model with 2 Poses (3D)")

    # ----- Verify footer values in duplicated LR ----- #
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(14),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })

    # ----- Switch to original LR ----- #
    open_live_report(selenium, name=live_report_to_duplicate['livereport_name'])
    # ----- Verify that columns count and compounds count have not changed ----- #s
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(7),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })
