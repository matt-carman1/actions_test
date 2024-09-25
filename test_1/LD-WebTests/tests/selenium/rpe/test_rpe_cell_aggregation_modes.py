import pytest

from helpers.change.actions_pane import close_add_data_panel, open_add_compounds_panel, open_add_data_panel
from helpers.change.columns_action import add_column_by_name
from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.grid_columns import scroll_to_column_header
from helpers.flows.add_compound import search_by_id
from helpers.flows.grid import toggle_cell_aggregation_and_verify_column_content
from helpers.selection.general import MENU_ITEM
from helpers.selection.grid import GRID_HEADER_DROPDOWN_MENU
from helpers.selection.grid_menus import DEFAULT_AGGREGATION_MENU_ITEM
from library import dom, simulate


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rpe_cell_aggregation_modes(selenium):
    """
    Populate a new LR with 3 structures and RPE columns from 2 different experiments. The
    first structure will have values in both experiments. The second and third structure
    added will not have values for the same experiment.

    Verify:
    - rpe columns values are correct for different cell aggregation modes in RPC mode.
    """

    # Add compounds to the LR with search by ID
    open_add_compounds_panel(selenium)
    search_by_id(selenium, 'CRA-031137, CRA-033619, V055685')

    # Add RPE columns to the LR
    pk_po_rat_rpe = 'PK_PO_RAT (AUC)'
    pk_iv_rat_rpe = 'PK_IV_RAT (AnalysisComment)'
    open_add_data_panel(selenium)
    add_column_by_name(selenium, 'PK_PO_RAT (AUC)')
    add_column_by_name(selenium, pk_iv_rat_rpe)
    close_add_data_panel(selenium)

    # Sort compounds by ID
    sort_grid_by(selenium, 'ID')

    # ----- Testing Cell Aggregation for 'PK_PO_RAT (AUC)' ----- #
    hover_over_column_menu_item(selenium, pk_po_rat_rpe, 'Aggregate Values By')
    default_aggregation_menu_item = dom.get_element(selenium, DEFAULT_AGGREGATION_MENU_ITEM)
    # Verify that the default aggregation mode is Mean Arithmetic
    assert default_aggregation_menu_item.text == 'Mean(Arithmetic)(Default)'

    # Cell Aggregation = 'Median'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      pk_po_rat_rpe,
                                                      "Median", ['', '6.1', '0.2'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC) - MEDIAN')

    # Cell Aggregation = 'Mean(Arithmetic)'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      'PK_PO_RAT (AUC) - MEDIAN',
                                                      "Mean(Arithmetic)", ['', '6.1', '0.2'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC)')

    # Cell Aggregation = 'Mean(Geometric)'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      'PK_PO_RAT (AUC)',
                                                      "Mean(Geometric)", ['', '6.1', '0.182'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC) - GEO')

    # Cell Aggregation = 'Min'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      'PK_PO_RAT (AUC) - GEO',
                                                      "Min", ['', '6.1', '0.1'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC) - MIN')

    # Cell Aggregation = 'Max'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      'PK_PO_RAT (AUC) - MIN',
                                                      "Max", ['', '6.1', '0.3'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC) - MAX')

    # Cell Aggregation = 'Std Dev'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      'PK_PO_RAT (AUC) - MAX',
                                                      "Std Dev", ['', '0', '0.0816'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC) - STDDEV')

    # Cell Aggregation = 'Count'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      'PK_PO_RAT (AUC) - STDDEV',
                                                      "Count", ['', '1', '3'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC) - COUNT')

    # Cell Aggregation = 'Latest Result'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      'PK_PO_RAT (AUC) - COUNT',
                                                      "Latest Result", ['', '6.1', '0.3'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC) - LATEST')

    # Cell Aggregation = 'Unaggregated'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      'PK_PO_RAT (AUC) - LATEST',
                                                      "Unaggregated", ['', '6.1', '0.3\n0.2\n0.1'],
                                                      column_name_after_toggle='PK_PO_RAT (AUC) - UNAGGREGATED')

    # ----- Testing Cell Aggregation for 'PK_IV_RAT (AnalysisComment)' ----- #
    hover_over_column_menu_item(selenium, pk_iv_rat_rpe, 'Aggregate Values By')
    default_aggregation_menu_item = dom.get_element(selenium, DEFAULT_AGGREGATION_MENU_ITEM)
    # Verify that the default aggregation mode is Mean Arithmetic
    assert default_aggregation_menu_item.text == 'Mean(Arithmetic)(Default)'

    # Cell Aggregation = 'Count'
    toggle_cell_aggregation_and_verify_column_content(selenium,
                                                      pk_iv_rat_rpe,
                                                      "Count", ['1', '1', ''],
                                                      column_name_after_toggle='PK_IV_RAT (AnalysisComment) - COUNT')

    # Cell Aggregation = 'Mean(Arithmetic)'
    toggle_cell_aggregation_and_verify_column_content(
        selenium,
        'PK_IV_RAT (AnalysisComment) - COUNT',
        "Mean(Arithmetic)", [
            'PK analysis (WinNonlin Pro) two-compartment model with 1/y^ weighting',
            'WinNonlin Pro two-compartment model with 1/y^ and 1/y^2 weighting', ''
        ],
        column_name_after_toggle='PK_IV_RAT (AnalysisComment)')


def hover_over_column_menu_item(driver, column_name, column_option_name):
    """
    Scrolls to the column header into view then it opens the column context menu
    and then hovers over the menu item

    :param driver: webdriver
    :param column_name: str, column title
    :param column_option_name: str, column menu item label
    """
    column_header = scroll_to_column_header(driver, column_name)

    # simulate hover then click the button when it appears
    simulate.hover(driver, column_header)
    dom.click_element(driver, GRID_HEADER_DROPDOWN_MENU)

    # hover over the column menu item
    element = dom.get_element(driver, MENU_ITEM, text=column_option_name)
    simulate.hover(driver, element)
