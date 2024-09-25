import pytest

from helpers.change.actions_pane import open_visualize_panel
from helpers.change.plots import set_equal_bin_count
from helpers.selection.plots import VISUALIZATION_PIE, X_AXIS_SELECT
from helpers.verification.plots import verify_display_ranges_and_tooltips_for_pie_chart
from library import dom
from library.select import select_option_by_text

live_report_to_duplicate = {'livereport_name': '50 Compounds 10 Assays', 'livereport_id': '881'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_pie_equal_bins(selenium):
    """
    Test Pie chart Equal Binning

    1. Check default equal bins and verification
    2. Change Equal binning count to 15 and verification
    3. Change Equal binning count to 20 and verification
    """
    # Create a new pie chart.
    open_visualize_panel(selenium)
    dom.click_element(selenium, VISUALIZATION_PIE)

    # Select the axes.
    select_option_by_text(selenium, X_AXIS_SELECT, 'i_i_glide_lignum (undefined)')

    # ----- Check default equal bins and verification ----- #
    set_equal_bin_count(selenium, 10)
    verify_display_ranges_and_tooltips_for_pie_chart(selenium,
                                                     bin_count=10,
                                                     display_ranges=[
                                                         '162 - 545.4 (5)', '545.4 - 928.8 (7)', '928.8 - 1312.2 (4)',
                                                         '1312.2 - 1695.6 (6)', '1695.6 - 2079 (2)',
                                                         '2079 - 2462.4 (1)', '2462.4 - 2845.8 (6)',
                                                         '2845.8 - 3229.2 (6)', '3229.2 - 3612.6 (7)',
                                                         '3612.6 - 3996 (6)'
                                                     ],
                                                     display_range_for_tooltip_check='162-545-4',
                                                     tooltip_text='Data Range\n162 <= x < 545.4\nCount\n5')

    # ----- Change Equal binning count to 15 and verification ----- #
    set_equal_bin_count(selenium, 15)
    verify_display_ranges_and_tooltips_for_pie_chart(
        selenium,
        bin_count=15,
        display_ranges=[
            '162 - 417.6 (4)', '417.6 - 673.2 (1)', '673.2 - 928.8 (7)', '928.8 - 1184.4 (3)', '1184.4 - 1440 (3)',
            '1440 - 1695.6 (4)', '1695.6 - 1951.2 (2)', '1951.2 - 2206.8 (0)', '2206.8 - 2462.4 (1)',
            '2462.4 - 2718 (1)', '2718 - 2973.6 (9)', '2973.6 - 3229.2 (2)', '3229.2 - 3484.8 (5)',
            '3484.8 - 3740.4 (6)', '3740.4 - 3996 (2)'
        ],
        display_range_for_tooltip_check='162-417-6',
        tooltip_text='Data Range\n162 <= x < 417.6\nCount\n4')
