import pytest

from helpers.change.columns_action import rename_grouped_column
from helpers.change.footer_actions import show_hidden_columns
from helpers.change.grid_column_menu import click_column_menu_item, freeze_a_column_via_menu_option, hide_column
from helpers.flows.grid import group_columns_selectively
from helpers.selection.grid import GRID_HEADER_CELL
from helpers.verification.element import verify_is_visible, verify_column_menu_items_visible
from helpers.verification.grid import verify_frozen_columns_in_grid, verify_footer_values, verify_columns_not_visible
from library import base

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('duplicate_live_report')
def test_column_operations_on_grouped_columns(selenium):
    """
    Test for do column operations on grouped columns.

    1. Group Columns
    2. Freeze Grouped column and verify whether it is frozen
    3. Rename Grouped column
    4. Hide Grouped column
    5. Show Grouped column
    6. Unfreeze Grouped column
    7. Remove Grouped column
    """
    # ----- Group columns ----- #
    grp_name = 'Group'
    group_columns_selectively(selenium, grp_name, 'PK_PO_RAT (AUC) [uM]', 'Test RPE Formula')

    # ----- Freeze grouped column and verify whether it is frozen ----- #
    freeze_a_column_via_menu_option(selenium, grp_name)
    verify_frozen_columns_in_grid(selenium, ['Compound Structure', 'ID', grp_name])

    # ----- Rename Grouped column ----- #
    new_grouped_column_name = 'New Group'
    rename_grouped_column(selenium, grp_name, new_grouped_column_name)
    # verify old column name is not there in Grid
    verify_columns_not_visible(selenium, [grp_name])
    # verify column name changed to new column name
    verify_is_visible(selenium, GRID_HEADER_CELL, selector_text=new_grouped_column_name)

    # ----- Hide Grouped column ----- #
    hide_column(selenium, new_grouped_column_name)
    # verify footer values for hidden columns
    verify_footer_values(selenium, {'column_all_count': '9 Columns', 'column_hidden_count': '3 Hidden'})
    # verify hidden columns not visible in grid
    verify_columns_not_visible(selenium, [new_grouped_column_name, 'PK_PO_RAT (AUC) [uM]', 'Test RPE Formula'])

    # ----- Show Grouped column ----- #
    show_hidden_columns(selenium, 3)
    verify_is_visible(selenium, GRID_HEADER_CELL, selector_text=new_grouped_column_name)

    # ----- Unfreeze Grouped column ----- #
    click_column_menu_item(selenium, new_grouped_column_name, 'Unfreeze')
    # verify grouped column is in unfreeze state
    verify_frozen_columns_in_grid(selenium, ['Compound Structure', 'ID'])

    # ----- Remove Grouped column ----- #
    click_column_menu_item(selenium, new_grouped_column_name, 'Remove')
    base.click_ok(selenium)

    # verify footer values
    verify_footer_values(selenium, {'column_all_count': '10 Columns'})
    # verify removed columns not visible in grid
    verify_columns_not_visible(selenium, [new_grouped_column_name, 'PK_PO_RAT (AUC) [uM]', 'Test RPE Formula'])
