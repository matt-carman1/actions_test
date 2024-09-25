import pytest
from selenium.webdriver.common.by import By
from helpers.change.plots import open_advanced_options_panel, open_a_new_scatter_plot, \
    default_shape_selection_on_style_tab
from helpers.flows.plots import add_rule_with_data_and_verify_shape_counts
from helpers.selection.plots import PLOT_OPTIONS_TAB_NAME_STYLE, SHAPE_BY, X_AXIS_SELECT, Y_AXIS_SELECT, SELECT_BY_RADIO
from library import dom
from library.select import select_option_by_text
from library.utils import is_k8s

live_report_to_duplicate = {'livereport_name': '50 Compounds 10 Assays', 'livereport_id': '881'}


@pytest.mark.xfail(not is_k8s(), reason="SS-42516:fails on Old Jenkins")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_scatter_plot_by_shape(selenium):
    """
    test for scatterplot shape by functionality.

    :param selenium: selenium Webdriver
    """
    # Create a new scatter plot.
    open_a_new_scatter_plot(selenium)
    # Select the axes
    select_option_by_text(selenium, X_AXIS_SELECT, 'ID')
    select_option_by_text(selenium, Y_AXIS_SELECT, 'i_i_glide_lignum (undefined)')
    # Open plot options panel with style tab
    open_advanced_options_panel(selenium, PLOT_OPTIONS_TAB_NAME_STYLE)
    # Select shape by column
    select_option_by_text(selenium, SHAPE_BY, 'i_i_glide_XP_nbrot (undefined)')
    # Select radio button "123"
    radio_button = "123"
    dom.click_element(selenium, SELECT_BY_RADIO.format(radio_button), selector_type=By.XPATH)
    # default shape selection
    default_shape_selection_on_style_tab(selenium, 'square')
    # Add another rule for shape as circle, set shapeby values and verify both point & shape counts
    add_rule_with_data_and_verify_shape_counts(selenium, 'circle', '1', '5', 50)
    # Open plot options panel with style tab
    open_advanced_options_panel(selenium, PLOT_OPTIONS_TAB_NAME_STYLE)
    # Add another rule for shape as diamond, set shapeby values and verify both point & shape counts
    add_rule_with_data_and_verify_shape_counts(selenium, 'diamond', '7', '9', 50)