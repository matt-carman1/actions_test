import pytest

from helpers.change import actions_pane, columns_action, grid_columns
from helpers.change.filter_actions import get_filter, add_filter
from helpers.flows import add_compound


@pytest.fixture(scope='function')
def prepare_live_report_filter(selenium, new_live_report, open_livereport):
    # Search Compounds by ID
    actions_pane.open_add_compounds_panel(selenium)
    add_compound.search_by_id(selenium, "CHEMBL105*,CHEMBL103*")

    # Add a column to the LR
    actions_pane.open_add_data_panel(selenium)
    columns_action.add_column_by_name(selenium, "AlogP")

    # Verify that the Live Report is correct
    # Added columns on selenium-testserver are represented by column(column).
    # e.g. "Alog (AlogP)"
    column_name = "{} ({})".format("AlogP", "AlogP")
    # check that the column is added to the LR
    grid_columns.scroll_to_column_header(selenium, column_name)

    ##### Set up filter testing #####
    # get the filter element for AlogP column
    column_name = "{} ({})".format("AlogP", "AlogP")
    actions_pane.open_filter_panel(selenium)
    add_filter(selenium, column_name)
    filter_element = get_filter(selenium, column_name, filter_position=3)

    yield filter_element
