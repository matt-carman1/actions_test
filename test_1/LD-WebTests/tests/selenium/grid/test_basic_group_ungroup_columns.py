import pytest

from helpers.flows.add_compound import search_by_id
from helpers.change.actions_pane import open_add_data_panel, close_add_data_panel
from helpers.change.columns_action import add_column_by_name
from helpers.change.grid_column_menu import ungroup_columns, hide_column
from helpers.flows.grid import group_columns_selectively, group_columns_in_bulk
from helpers.selection.grid import GRID_GROUP_HEADER_CELL, GRID_HEADER_BOTTOM
from library import dom, style, wait


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('new_live_report')
def test_basic_group_ungroup_columns(selenium):
    """
    Basic Test to group and Ungroup Columns
    1. Group columns selectively using the Control Key
    2. Group MPO column with a column on the right.
    3. Group continuous columns using the Shift Key
    For each of the above case:
        a. Verify the grouping is done
        b. Ungroup them
    :param selenium: Selenium webdriver
    :return:
    """

    # ----- Setup the LiveReport ----- #
    search_by_id(selenium, 'CRA-031137, CRA-031437, CRA-031925, CRA-031965')

    open_add_data_panel(selenium)

    add_column_by_name(selenium, 'PK_PO_RAT (AUC)')
    add_column_by_name(selenium, 'ABL-TRFRET (Ki)')
    add_column_by_name(selenium, 'EGFR-TRFRET (Ki)')
    add_column_by_name(selenium, '(Global) Higher is Good')
    add_column_by_name(selenium, 'Number - published')

    close_add_data_panel(selenium)
    # ----- Hide MPO desirability Score column group ------#
    hide_column(selenium, 'Higher is Good Desirability Scores and Number of Missing Inputs')

    # ----- Grouping Columns Selectively ----- #
    group_one = 'TEST'
    group_columns_selectively(selenium, group_one, 'PK_PO_RAT (AUC) [uM.min]', 'EGFR-TRFRET (Ki) [uM]')

    group_header_element = dom.get_element(selenium, GRID_GROUP_HEADER_CELL)
    assert group_header_element.text == group_one, \
        "No Group with name {} was found, instead found group with name {}".format(group_one, group_header_element.text)

    # Ungroup the columns
    ungroup_columns(selenium, group_column_name='TEST')
    wait.until_not_visible(selenium, GRID_HEADER_BOTTOM)

    # Group a MPO column with a column on the right
    group_two = 'TEST_MPO'
    group_columns_selectively(selenium, group_two, 'Higher is Good', 'Number - published')

    # Verify that the Epsilon Symbol does not show up in the column group header. Check SS-21257
    group_header_element = dom.get_element(selenium, GRID_GROUP_HEADER_CELL)
    background_image = style.get_css_value(group_header_element, 'background-image')
    assert background_image == 'none'

    # Ungroup them
    ungroup_columns(selenium, group_column_name=group_two)
    wait.until_not_visible(selenium, GRID_HEADER_BOTTOM)

    # ----- Group Continuous Columns ----- #
    group_three = 'TEST2'
    group_columns_in_bulk(selenium,
                          start_column_name='PK_PO_RAT (AUC) [uM.min]',
                          end_column_name='Number - published',
                          group_name=group_three)

    group_header_element = dom.get_element(selenium, GRID_GROUP_HEADER_CELL)
    assert group_header_element.text == group_three, "No Group with name {} was found, instead found group with name " \
                                                     "{}".format(group_one, group_header_element.text)

    # Ungroup the columns
    ungroup_columns(selenium, group_column_name=group_three)
