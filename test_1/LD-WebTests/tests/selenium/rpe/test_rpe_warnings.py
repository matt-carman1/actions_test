"""
Checks RPE, Row per Experiment, messages/warnings are present in plots, MPOs, formula, and when bulk copying.
"""
import pytest

from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search, open_visualize_panel, \
    open_add_data_panel, close_add_data_panel
from helpers.change.advanced_search_actions import add_query
from helpers.change.columns_action import add_column_by_name
from helpers.change.data_and_columns_tree import clear_column_tree_search, search_column_tree
from helpers.change.formula_actions import open_create_formula_window, add_column_to_formula
from helpers.change.freeform_column_action import create_ffc
from helpers.change.grid_columns import get_cell
from helpers.change.plots import add_scatterplot, add_histogram_plot, add_radar_plot, add_box_plot, add_pie_plot
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON
from helpers.selection.column_tree import COLUMN_TREE_PICKER_TEXT_NODE
from helpers.selection.formula import FORMULA_NOTICE
from helpers.selection.freeform_columns import FreeformColumnCellEdit, FreeformColumnBulkEdit
from helpers.selection.grid import GRID_HEADER_CELL, Footer
from helpers.change.grid_column_menu import open_edit_mpo_window
from helpers.selection.mpo import CELL_TIP_MESSAGE, CONSTITUENT_OPTION, NON_AVG_COLUMN_NOTICE, MPO_CANCEL_BUTTON, \
    MPO_EDIT
from helpers.selection.plots import Y_AXIS_SELECT, X_AXIS_SELECT, ADD_RADAR_AXIS_BUTTON, RADAR_AXIS_SELECT, \
    PLOT_WARNING, INFO_CIRCLE
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from helpers.verification.grid import check_for_butterbar, verify_footer_values
from helpers.verification.plots import verify_radar_axis_count
from library import base, dom, simulate
from library.select import select_option_by_text
from selenium.webdriver.support.ui import Select


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rpe_warnings(selenium):
    """
    Ticket instructions:
    Verifies RPE messages are shown for:

    1. Formula
    2. MPO, tooltip on hover while in Compound mode
    3. MPO RPE message in the 'Edit Existing Multi-Parameter Optimization' profile
    4. Bulk Copying in Compound mode
    5. Plots, when an RPE column is added

    :param selenium: Selenium Webdriver
    """
    mpo_name = 'Test RPE MPO'
    mpo_name_tree = '(JS Testing) {}'.format(mpo_name)
    rpe_assay_name = 'PK_PO_RAT (AUC)'
    lot_scientist = 'Lot Scientist'
    ffc_name = 'FFC bulk from RPE'
    structure_id = 'CRA-031437'

    # ----- RPE MESSAGES ----- #
    formula_rpe_warning = "*Formulas cannot be applied to cells containing list of values. Switch to " \
                          "Row Per Experiment mode to see formula’s results for all values in " \
                          "each cell of the following columns: {}"
    mpo_rpe_celltip = 'MPOs cannot be applied to cells containing list of values. ' \
                      'Switch to Row Per Experiment mode for MPO to be applied to all cells of this column'
    mpo_rpe_distribution_notice = 'MPOs cannot be applied to cells containing list of values. ' \
                                  'Switch to Row Per Experiment mode for MPO to be applied to all cells of this column.'
    bulk_copy_rpe_warning = 'Only cells with single values will be copied over to the Freeform Column.'
    plot_rpe_warning = "*Only cells with a single value for these assays [{}], using either a column " \
                       "aggregation or using row per experiment mode, will be plotted.".format(rpe_assay_name)
    plot_point_enum_warning = "*Points are only enumerated for a combination of multi-value cells from aligned columns"

    # ----- LR SETUP ----- #
    # Open the Advanced Query Tab
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)
    # Add range query and search
    add_query(selenium, rpe_assay_name)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(18)})

    # ----- Formula -----#
    # create a formula with an rpe column as part of the expression
    open_create_formula_window(selenium)
    add_column_to_formula(selenium, rpe_assay_name)
    # validate rpe message in the 'Create and Add New Formula Column' dialog
    verify_is_visible(selenium, FORMULA_NOTICE, formula_rpe_warning.format(rpe_assay_name))

    # Save button is off the screen because of the RPE message.
    dom.press_esc(selenium)

    # ----- MPO -----#
    open_add_data_panel(selenium)
    add_column_by_name(selenium, mpo_name_tree)
    clear_column_tree_search(selenium)
    check_for_butterbar(selenium, notification_text='Adding columns to LiveReport', visible=False)
    cell = get_cell(selenium, structure_id, mpo_name)
    close_add_data_panel(selenium)

    # validate rpe message in celltip that appears when hovering over the ! icon
    simulate.hover(selenium, cell)
    verify_is_visible(selenium, CELL_TIP_MESSAGE, mpo_rpe_celltip)

    # open the 'Edit Existing Multi-Parameter Optimization' dialog
    open_edit_mpo_window(selenium, mpo_name)
    dom.click_element(selenium, CONSTITUENT_OPTION.format(rpe_assay_name))

    # validate rpe message
    verify_is_visible(selenium, NON_AVG_COLUMN_NOTICE, mpo_rpe_distribution_notice)

    dom.click_element(selenium, MPO_CANCEL_BUTTON)

    # ----- BULK COPY FFC -----#
    # create a ffc column & setup bulk copy from rpe assay column
    create_ffc(selenium, ffc_name)
    cell = get_cell(selenium, structure_id, ffc_name)
    dom.click_element(selenium, GRID_HEADER_CELL, text=ffc_name, exact_text_match=True)
    simulate.hover(selenium, cell)
    dom.click_element(cell, FreeformColumnCellEdit.FFC_EDIT_ICON)
    dropdown = Select(dom.click_element(selenium, FreeformColumnBulkEdit.COLUMN_DROPDOWN))
    dropdown.select_by_visible_text('PK_PO_RAT (AUC)')
    verify_is_visible(selenium, FreeformColumnBulkEdit.RPE_EDIT_WARNING, bulk_copy_rpe_warning)
    base.click_cancel(selenium)

    # ----- PLOTS -----#
    open_visualize_panel(selenium)

    # scatter plot
    add_scatterplot(selenium)
    select_option_by_text(selenium, X_AXIS_SELECT, rpe_assay_name)
    select_option_by_text(selenium, Y_AXIS_SELECT, lot_scientist)
    # validate rpe plot message is visible
    verify_is_visible(selenium, PLOT_WARNING.format(plot_point_enum_warning))

    # histogram plot
    add_histogram_plot(selenium)
    select_option_by_text(selenium, X_AXIS_SELECT, rpe_assay_name)
    # validate that no warnings exist
    verify_is_not_visible(selenium, INFO_CIRCLE)

    # radar plot
    add_radar_plot(selenium)
    dom.click_element(selenium, 'button', text="None selected. Click to change...", exact_text_match=True)
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    select_option_by_text(selenium, RADAR_AXIS_SELECT.format(0), rpe_assay_name)
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    select_option_by_text(selenium, RADAR_AXIS_SELECT.format(1), rpe_assay_name)
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    base.click_ok(selenium)
    verify_radar_axis_count(selenium, 3)
    # validate rpe plot message is not visible
    verify_is_not_visible(selenium, PLOT_WARNING.format(plot_rpe_warning))

    # box plot
    add_box_plot(selenium)
    select_option_by_text(selenium, X_AXIS_SELECT, lot_scientist)
    select_option_by_text(selenium, Y_AXIS_SELECT, rpe_assay_name)
    # validate rpe plot message is visible
    dom.click_element(selenium, INFO_CIRCLE)
    verify_is_visible(selenium, PLOT_WARNING.format(plot_point_enum_warning))

    # pie plot
    add_pie_plot(selenium)
    select_option_by_text(selenium, X_AXIS_SELECT, rpe_assay_name)
    # validate that no warnings exist
    verify_is_not_visible(selenium, INFO_CIRCLE)


def edit_mpo(driver, mpo_name):
    """
    Opening the 'Edit Existing Multi-Parameter Optimization' via the dc tree.

    :param driver:  selenium webdriver
    :param mpo_name: name of the mpo in the dc tree
    """
    search_column_tree(driver, mpo_name)
    simulate.hover(driver, dom.get_element(driver, COLUMN_TREE_PICKER_TEXT_NODE, mpo_name, exact_text_match=True))
    dom.click_element(driver, MPO_EDIT)
