import pytest
from helpers.change.actions_pane import open_add_compounds_panel, close_add_compounds_panel, close_add_data_panel
from helpers.change.columns_management_ui import open_column_mgmt_panel
from helpers.change.sar_action import create_sar_scaffold
from helpers.flows.add_compound import search_by_id
from helpers.change.grid_columns import get_cell
from helpers.selection.sar_analysis import SAR_MATCH_SCAFFOLD_LINK
from helpers.verification.grid import verify_column_contents, verify_footer_values
from helpers.verification.data_and_columns_tree import verify_columns_in_column_mgmt_ui
from library import dom, simulate


@pytest.mark.smoke
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_basic_sar(selenium):
    """
    Creates an initial SAR scaffold. And then creates another scaffold that
    matches both a structure that matched the first scaffold and one that
    didn't.

    :param selenium: Webdriver
    """
    # ----- Get standard LR ----- #
    # Open the Compounds Panel and add compound to LR via search by ID
    open_add_compounds_panel(selenium)
    search_by_id(selenium, 'V035752, V038399, V041170, V041471, V044401, V044929, V047455, V047535, V053230, V054379')
    close_add_compounds_panel(selenium)

    # ----- Create a Scaffold ----- #
    # We need to use molv3 here since that seems to be the only way
    # to include R groups
    sar_01_molv3 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 8 8 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 R# -1.273429 -2.533143 0.000000 102 VAL=1 RGROUPS=(1 2)\nM  V30 2 C -0.035714 -1.820000 0.000000 0\nM  V30 3 C -0.034571 -0.391429 0.000000 0\nM  V30 4 C 1.203143 0.322000 0.000000 0\nM  V30 5 R# 1.204286 1.750571 0.000000 101 VAL=1 RGROUPS=(1 1)\nM  V30 6 C 2.439714 -0.393429 0.000000 0\nM  V30 7 C 2.438571 -1.822000 0.000000 0\nM  V30 8 C 1.200857 -2.535143 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 1 4 5\nM  V30 5 2 4 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 8 2\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    create_sar_scaffold(selenium, sar_01_molv3)
    open_column_mgmt_panel(selenium)
    verify_columns_in_column_mgmt_ui(selenium,
                                     expected_columns=[
                                         'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Lot Date Registered',
                                         'Scaffold Name', 'R1 (SAR)', 'R2 (SAR)', 'Matched Scaffold'
                                     ])
    close_add_data_panel(selenium)
    verify_footer_values(selenium, {'column_all_count': '9 Columns', 'column_hidden_count': '1 Hidden'})

    # Verify contents of Scaffold Name column
    verify_column_contents(selenium, 'Scaffold Name',
                           ['', 'Scaffold 1', '', 'Scaffold 1', 'Scaffold 1', '', 'Scaffold 1', '', '', ''])

    # ----- Create a second Scaffold ----- #
    # In row without scaffold, click on "Match another Scaffold"
    empty_r_cell = get_cell(selenium, 'V035752', 'R1 (SAR)')
    simulate.hover(selenium, empty_r_cell)
    dom.click_element(empty_r_cell, SAR_MATCH_SCAFFOLD_LINK)
    # Create a scaffold that will match that row and will also match another row that already has scaffold 1.
    sar_02_molv3 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 8 8 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 R# -1.142571 -2.045714 0.000000 102 VAL=1 RGROUPS=(1 2)\nM  V30 2 C 0.095143 -1.332286 0.000000 0\nM  V30 3 C 0.096286 0.096286 0.000000 0\nM  V30 4 R# -1.140286 0.811429 0.000000 101 VAL=1 RGROUPS=(1 1)\nM  V30 5 C 1.334000 0.809429 0.000000 0\nM  V30 6 C 2.570571 0.094286 0.000000 0\nM  V30 7 C 2.569429 -1.334286 0.000000 0\nM  V30 8 C 1.331714 -2.047714 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 1 3 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 8 2\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    create_sar_scaffold(selenium, sar_02_molv3)
    open_column_mgmt_panel(selenium)
    verify_columns_in_column_mgmt_ui(selenium,
                                     expected_columns=[
                                         'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Lot Date Registered',
                                         'Scaffold Name', 'R1 (SAR)', 'R2 (SAR)', 'Matched Scaffold'
                                     ])
    close_add_data_panel(selenium)
    verify_footer_values(selenium, {'column_all_count': '9 Columns', 'column_hidden_count': '1 Hidden'})
    # the row with two Scaffolds should say "Scaffold 1"
    verify_column_contents(selenium, 'Scaffold Name',
                           ['', 'Scaffold 1', '', 'Scaffold 1', 'Scaffold 1', 'Scaffold 2', 'Scaffold 1', '', '', ''])
