import pytest

from helpers.change.actions_pane import close_add_data_panel, open_add_compounds_panel, open_add_data_panel
from helpers.change.columns_action import add_column_by_name
from helpers.change.freeform_column_action import edit_ffc_cell
from helpers.change.grid_column_menu import sort_grid_by, hide_column
from helpers.change.grid_row_actions import scroll_to_row
from helpers.flows.add_compound import search_by_id
from helpers.selection.grid import AGGREGATE_TOOLTIP, AGGREGATE_TOOLTIP_STRIPE, AGGREGATE_TOOLTIP_TEXT, Footer
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values, verify_grid_contents
from library import dom, simulate, wait
from library.utils import is_k8s

test_username = 'commaDecimalUser'
test_password = 'commaDecimalUser'


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('new_live_report')
def test_comma_format_in_grid(selenium):
    """
    Check that the period in decimal values are replaced with a comma in:
        1. FFC, MPO cells
        2. Check Date and Text Columns not affected
        3. React Grid, Tooltips
    :param selenium: Webdriver
    :return:
    """
    # ----- Adding compounds and columns to the Livereport ----- #
    # TODO: Get rid of this by placing an LR with the same data in starter data.
    # Add Compounds
    compound_ids = 'CRA-031137, CRA-032370, CRA-032372, CRA-032661, CRA-032547, CRA-032662'
    open_add_compounds_panel(selenium)
    search_by_id(selenium, compound_ids)

    # Add Columns
    open_add_data_panel(selenium)
    add_column_by_name(selenium, 'AlogP')
    add_column_by_name(selenium, 'BTK-TRFRET (Ki)')
    add_column_by_name(selenium, 'Number - published')
    add_column_by_name(selenium, 'Date - published')
    add_column_by_name(selenium, '(Global) Lower is Good')
    close_add_data_panel(selenium)
    mpo_desirability_score_column_group = 'Lower is Good Desirability Scores and Number of Missing Inputs'

    # Verify that the LR has expected count of compounds and columns.
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(12),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    # Edit FFC with comma value and verify. Note: Editing would not be needed once this in starter data
    edit_ffc_cell(selenium, 'Number - published', 'CRA-032372', value='2,75')

    # Hide Desirability Score column group
    hide_column(selenium, mpo_desirability_score_column_group)

    # Verify grid contents for Comma format
    sort_grid_by(selenium, 'ID')
    verify_grid_contents(
        selenium, {
            'Lot Scientist': [
                'demo\nJ.PALMER\nJ.PALMER\nJ.PALMER\nJ.PALMER', 'E.LEAHY', 'E.LEAHY', 'demo\nM.SENDZIK',
                'demo\nA.KOLESNIKOV', 'demo\nA.KOLESNIKOV\ndemo'
            ],
            'AlogP (AlogP)': ['3,2', '2,0', '4,0', '1,5', '5,5', '5,9'],
            'BTK-TRFRET (Ki) [uM]': ['300++', '>300', '>300', '1600', '10,12', '3,87'],
            'Number - published': ['123', '4', '2,75', '', '', ''],
            'Date - published': ['', '', '2016-07-05', '', '', ''],
            'Lower is Good': ['0', '0', '0', '0', '0,984', '0,993']
        })

    # reverting the FFC value back to null to avoid any conflict with any other test using this.
    edit_ffc_cell(selenium, 'Number - published', 'CRA-032372', value='')

    # ----- Check for comma format values in the tooltip ----- #
    scroll_to_row(selenium, 'CRA-032662')
    simulate.hover(selenium, dom.get_element(selenium, AGGREGATE_TOOLTIP, text='10,12'))
    wait.until_visible(selenium, AGGREGATE_TOOLTIP_STRIPE)
    verify_is_visible(selenium, AGGREGATE_TOOLTIP_TEXT, selector_text='6,4 uM')
