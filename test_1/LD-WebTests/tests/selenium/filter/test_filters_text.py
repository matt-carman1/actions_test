import pytest

from helpers.change.filter_actions import change_filter_settings, \
    type_and_select_filter_item, select_filter_checkbox_item
from helpers.change.dropdown_actions import remove_dropdown_bubble_value
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.smoke
def test_filter_text(selenium, prepare_live_report_filter):
    """
    Test LD text filters.
    We are applying text filters on compounds retrieved by ID search on "CHEMBL105*,CHEMBL103*", for AlogP.

    :param selenium: Selenium Webdriver
    :param prepare_live_report_filter: A fixture to prepare LR for Filter tests
    """

    # Filters by default open as Range, so converting to text filter first
    prepare_live_report_filter = change_filter_settings(prepare_live_report_filter, "Show as text", 3)

    # ----- Test "(undefined)" text filter (selection and deselection) ----- #
    # Selecting "(undefined)" from the multiselect picklist and applying filter
    type_and_select_filter_item(prepare_live_report_filter, "(undefined)")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(0)
        })

    # Deselecting "(undefined)" from the multiselect picklist
    select_filter_checkbox_item(prepare_live_report_filter, "(undefined)", do_select=False)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22)
        })

    # ----- Test two filters, "-1.9" and "3.8" ----- #
    type_and_select_filter_item(prepare_live_report_filter, "-1.9")
    type_and_select_filter_item(prepare_live_report_filter, "3.8")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(3)
        })

    # removing filter value by clicking on 'x' mark
    remove_dropdown_bubble_value(selenium, prepare_live_report_filter, "-1.9")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(2)
        })
