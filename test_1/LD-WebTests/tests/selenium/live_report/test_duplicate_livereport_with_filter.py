import pytest

from helpers.change.actions_pane import open_filter_panel
from helpers.change.filter_actions import add_filter, remove_all_filters, get_filter, set_filter_range
from helpers.flows.live_report_management import duplicate_livereport
from helpers.selection.filter_actions import TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE, FILTERS_BOX_WIDGET_HEADER_NAME
from helpers.selection.grid import Footer
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.usefixtures('open_livereport')
@pytest.mark.usefixtures("duplicate_live_report")
def test_duplicate_livereport_with_filter(selenium, duplicate_live_report):
    """
    Test duplicate liveReport with filter columns

    1. Duplicate the LiveReport with filter turned on and with selecting filtered column
    2. Verify columns present in LR and filter is on
    3. Duplicate the LR without selecting filtered columns
    4. Verify columns not present in LR but filter is on

    :param selenium: selenium webdriver
    """

    # input data
    filtered_column_name = 'Solubility (undefined)'

    # Remove any existing filters from the duplicated LR
    remove_all_filters(selenium)

    # Add filter on column "Solubility (undefined)". Leave min-value at auto, set max to 10
    add_filter(selenium, 'Solubility (undefined)')
    solubility_filter_element = get_filter(selenium, 'Solubility (undefined)', filter_position=3)
    set_filter_range(selenium, solubility_filter_element, filter_position=3, upper_limit=300)

    # Duplicate the LiveReport with filter turned on and with selecting filtered column
    duplicated_lr_with_filter_column = duplicate_livereport(selenium,
                                                            livereport_name=duplicate_live_report,
                                                            selected_columns=[filtered_column_name])

    # Verify columns present in LR and filter is on
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })
    verify_visible_columns_in_live_report(
        selenium, ['Compound Structure', 'ID', 'Rationale', 'Lot Scientist', filtered_column_name])
    open_filter_panel(selenium)
    verify_is_visible(selenium, TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE)
    verify_is_visible(selenium,
                      '.box-widget-header .header-name',
                      selector_text=filtered_column_name,
                      exact_selector_text_match=True)

    # Duplicate the LR without selecting filtered columns
    duplicate_livereport(selenium, livereport_name=duplicated_lr_with_filter_column, selected_columns=[])

    # Verify columns not present in LR but filter is on
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })
    verify_visible_columns_in_live_report(selenium, ['Compound Structure', 'ID', 'Rationale', 'Lot Scientist'])
    open_filter_panel(selenium)
    verify_is_visible(selenium, TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE)
    verify_is_not_visible(selenium, FILTERS_BOX_WIDGET_HEADER_NAME)
