import pytest

from helpers.change.actions_pane import open_add_data_panel, close_add_data_panel, open_advanced_search, \
    open_add_compounds_panel, close_add_compounds_panel
from helpers.change.columns_management_ui import open_column_mgmt_panel
from helpers.flows.live_report_management import duplicate_livereport
from helpers.selection.grid import Footer
from helpers.verification.advanced_search import verify_added_columns_in_advanced_query_panel
from helpers.verification.data_and_columns_tree import verify_columns_in_column_mgmt_ui
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report

test_livereport = 'FFC'


@pytest.mark.usefixtures('open_livereport')
def test_duplicate_livereport_with_advanced_search(selenium):
    """
    Test duplicate livereport with advanced search

    1. Duplicate the LR with selecting adv search query columns.
    2. verify columns present in LR and advanced search panel has query params.
    3. Duplicate the LR without selecting adv search query columns.
    4. verify columns not present in LR but adv query present in adv panel.

    :param selenium: selenium webdriver
    :param open_livereport: a fixture which opens live report
    """
    # input data
    column_name = 'Published Freeform Text Column'
    # ----- Duplicate the LR with selecting adv search query columns ----- #
    duplicated_lr = duplicate_livereport(selenium, livereport_name=test_livereport, selected_columns=[column_name])

    # ----- verify columns present in LR and advanced search panel has query params ----- #
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })
    verify_visible_columns_in_live_report(
        selenium, ['Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', column_name])
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)
    verify_added_columns_in_advanced_query_panel(selenium, [column_name])

    # ----- Duplicate the LR without selecting adv search query columns ----- #
    duplicate_livereport(selenium, livereport_name=duplicated_lr, selected_columns=[])

    # ----- verify columns not present in LR but adv query present in adv panel ----- #
    verify_added_columns_in_advanced_query_panel(selenium, [column_name])
    close_add_compounds_panel(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })
    verify_visible_columns_in_live_report(selenium,
                                          ['Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist'])
