"""
Test removal of SAR scaffold and SAR columns.
"""
import pytest

from helpers.change.actions_pane import open_add_compounds_panel, close_add_data_panel, close_sar_panel
from helpers.change.columns_management_ui import open_column_mgmt_panel, hide_columns_selectively, show_columns_selectively
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.change.sar_action import create_sar_scaffold, remove_sar_scaffold
from helpers.flows.add_compound import search_by_id
from helpers.selection.sar_analysis import SAR_HEADER
from helpers.selection.grid import GRID_HEADER_TOP, GRID_HEADER_SELECTOR_
from helpers.verification.grid import verify_footer_values
from library import dom, wait


@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_remove_scaffold_column(selenium):
    """
    Verifies:
     - SAR columns are not removable via the "Remove Column" option in the column dropdown while a SAR scaffold exists.
     - SAR columns are all removed if there are not SAR Scaffolds in the LR.

    :param selenium: webdriver
    """
    # ----- LR setup ----- #
    # Open the Compounds Panel and add compound to LR via Search by ID
    open_add_compounds_panel(selenium)
    search_by_id(selenium, 'V035752, V038399, V041170, V041471, V044401, V044929, V047455, V047535, V053230, V054379')

    # Hide irrelevant columns
    open_column_mgmt_panel(selenium)
    hide_columns_selectively(selenium, "ID", "All IDs", "Rationale", "Lot Scientist")
    close_add_data_panel(selenium)

    # ----- Create a SAR Scaffold ----- #
    sar_01_molv3 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 8 8 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 R# -1.273429 -2.533143 0.000000 102 VAL=1 RGROUPS=(1 2)\nM  V30 2 C -0.035714 -1.820000 0.000000 0\nM  V30 3 C -0.034571 -0.391429 0.000000 0\nM  V30 4 C 1.203143 0.322000 0.000000 0\nM  V30 5 R# 1.204286 1.750571 0.000000 101 VAL=1 RGROUPS=(1 1)\nM  V30 6 C 2.439714 -0.393429 0.000000 0\nM  V30 7 C 2.438571 -1.822000 0.000000 0\nM  V30 8 C 1.200857 -2.535143 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 1 4 5\nM  V30 5 2 4 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 8 2\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    create_sar_scaffold(selenium, sar_01_molv3)

    # ----- Verify SAR columns added are not removable ----- #
    # try to remove irremovable sar column
    click_column_menu_item(selenium, "Matched Scaffold", "Remove")
    click_column_menu_item(selenium, "Scaffold Name", "Remove")
    click_column_menu_item(selenium, "R1 (SAR)", "Remove")
    click_column_menu_item(selenium, "R2 (SAR)", "Remove")
    # assert sar columns are present in LR
    lr_column_names = dom.get_element(selenium, GRID_HEADER_TOP).text
    assert "Matched Scaffold" in lr_column_names, "Column `Matched Scaffold` expected to be in LR"
    assert "Scaffold Name" in lr_column_names, "Column `Scaffold Name` expected to be in LR"
    assert "R1 (SAR)" in lr_column_names, "Column `R1 (SAR)` expected to be in LR"
    assert "R2 (SAR)" in lr_column_names, "Column `R2 (SAR)` expected to be in LR"

    # ----- Verify SAR columns are removed when last SAR scaffold is removed ----- #
    # Remove SAR scaffold
    remove_sar_scaffold(selenium, name="Scaffold 1")
    # wait for scaffold to be removed
    wait.until_not_visible(selenium, SAR_HEADER, text="Scaffold 1")
    close_sar_panel(selenium)

    # verify footer shows correct column count
    verify_footer_values(selenium, {'column_all_count': '1 Columns', 'column_hidden_count': '5 Hidden'})

    # assert sar columns are not present in LR
    lr_column_names = dom.get_element(selenium, GRID_HEADER_TOP).text
    assert "Matched Scaffold" not in lr_column_names, "Column `Matched Scaffold` not expected to be in LR"
    assert "Scaffold Name" not in lr_column_names, "Column `Scaffold Name` not expected to be in LR"
    assert "R1 (SAR)" not in lr_column_names, "Column `R1 (SAR)` not expected to be in LR"
    assert "R2 (SAR)" not in lr_column_names, "Column `R2 (SAR)` not expected to be in LR"
