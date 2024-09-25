import pytest

from helpers.change.actions_pane import open_visualize_panel
from helpers.change.plots import set_active_custom_binning_rule_type, show_bin_options, add_custom_bin_rule
from helpers.selection.plots import CUSTOM_BINNING_BUTTON, CUSTOM_BINNING_RULE_TYPE_TOGGLE, PIE_SLICE_BY_ID, \
    VISUALIZATION_PIE, X_AXIS_SELECT
from helpers.verification.grid import verify_footer_values
from helpers.verification.plots import verify_custom_binning_active_rule_type, verify_pie_slice_count, \
    verify_bin_tooltip_bin_count
from library import dom, wait
from library.select import select_option_by_text
from helpers.verification import plots

live_report_to_duplicate = {'livereport_name': '50 Compounds 10 Assays', 'livereport_id': '881'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
@pytest.mark.app_defect(
    reason="SS-40507: Plots tooltip is not getting removed when we move the focus out from the tooltip")
def test_pie_custom_numeric_bins(selenium):
    """
    Test the following:
    Creation of a pie chart based on binned numeric data
    Creating and modifying a custom binning scheme

    :param selenium: selenium Webdriver
    """
    # Create a new pie chart.
    open_visualize_panel(selenium)
    dom.click_element(selenium, VISUALIZATION_PIE)

    # Select the axes.
    select_option_by_text(selenium, X_AXIS_SELECT, 'i_i_glide_lignum (undefined)')
    verify_pie_slice_count(selenium, 8)

    # Set custom binning and verify the active rule type is numeric.
    show_bin_options(selenium)
    dom.click_element(selenium, CUSTOM_BINNING_BUTTON)
    wait.until_visible(selenium, CUSTOM_BINNING_RULE_TYPE_TOGGLE)
    set_active_custom_binning_rule_type(selenium, 'numeric_range')
    verify_custom_binning_active_rule_type(selenium, 'numeric_range')

    # Add a rule, set the range and verify the number of bars and that the label for the bar is present.
    add_custom_bin_rule(selenium, min_value=0, max_value=380, index=1)
    verify_bin_rule_applied_in_pie_chart(selenium, bin_name='Bin-1', pie_slice_count=1, selected_rows_count=4)

    # Add a second rule.340
    show_bin_options(selenium)
    add_custom_bin_rule(selenium, min_value=380, max_value=599, index=2)
    verify_bin_rule_applied_in_pie_chart(selenium, bin_name='Bin-2', pie_slice_count=2, selected_rows_count=1)

    # Add a third rule
    plots.verify_plot_tooltip_removed(selenium)
    show_bin_options(selenium)
    add_custom_bin_rule(selenium, min_value=600, max_value=None, index=3)
    verify_bin_rule_applied_in_pie_chart(selenium, bin_name='Bin-3', pie_slice_count=3, selected_rows_count=45)


def verify_bin_rule_applied_in_pie_chart(driver, bin_name, pie_slice_count, selected_rows_count):
    """
    Verify pie chart, includes verification of 'number of slices', 'footer count for selected rows' and 'bin tooltip'

    :param driver: selenium webdriver
    :param bin_name: str, name of the bin
    :param pie_slice_count: int, number of pie slices
    :param selected_rows_count: int, number of selected rows
    """
    verify_pie_slice_count(driver, pie_slice_count)
    dom.click_element(driver, PIE_SLICE_BY_ID.format(bin_name))
    verify_footer_values(driver, {'row_selected_count': '{} Selected'.format(selected_rows_count)})
    verify_bin_tooltip_bin_count(driver, PIE_SLICE_BY_ID.format(bin_name), selected_rows_count)
