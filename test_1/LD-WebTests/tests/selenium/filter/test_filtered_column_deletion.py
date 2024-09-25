from helpers.change.grid_column_menu import remove_column
from helpers.flows.columns_tree import search_and_check_column_name_highlight
from helpers.selection.filter_actions import HEADER_TITLE
from helpers.selection.grid import Footer
from helpers.verification.element import verify_is_not_visible
from helpers.verification.grid import verify_footer_values


def test_filtered_column_deletion(selenium, prepare_live_report_filter):
    """
    Test to remove a column on the LR which has an active filter and verifying the filter behaviour
    We are applying text filters on compounds retrieved by ID search on "CHEMBL105*,CHEMBL103*", for AlogP.

    :param selenium: Selenium Webdriver
    :param prepare_live_report_filter: fixture, Prepares LR with a predefined column filter.
    """
    column_name = "{} ({})".format("AlogP", "AlogP")
    remove_column(selenium, column_name=column_name)
    # Searches for column name in Column Management UI and checks if the column exists or not
    search_and_check_column_name_highlight(selenium, search_term=column_name, expected=[])
    verify_is_not_visible(prepare_live_report_filter, selector=HEADER_TITLE)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE_NONE
        })
