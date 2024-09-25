import pytest

from helpers.change.live_report_picker import create_and_open_live_report
from helpers.change.project import open_project
from helpers.extraction.dialog import get_coordinates
from helpers.selection.forms import FORMS_ICON, ADD_WIDGET_BUTTON
from helpers.verification.draggable_dialog import verify_element_position
from library import dom, simulate
from helpers.selection.modal import CLOSE_BUTTON, CUSTOM_LAYOUT_DIV, DIV_LM_HEADER, \
    DIV_LM_STACK, GOLDEN_LAYOUT_GEAR_MENU_BUTTON, MODAL_DIALOG_HEADER, \
    NEW_LAYOUT_TITLE_INPUT, NEW_PLOT_WIDGET_ICON, OK_BUTTON, PLOT_OPTIONS_BB_MENU_ITEM, SCATTER_PLOT_ICON
from helpers.selection.general import MENU_ITEM
from library.actions import drag_and_drop_by_offset
from library.base import click_cancel


def test_dragging_project_picker_and_layout_picker(selenium, login_to_livedesign):
    """
    Test that OkCancel dialog rendered by ProjectPicker is undraggable
    and that OkCancel dialog rendered by LayoutPickerDialog is draggable
    """
    x_offset = 100
    y_offset = 50
    #### ProjectPicker is not draggable ####
    # Verify that OkCancel dialog rendered by ProjectPicker is undraggable
    header = dom.get_element(selenium, MODAL_DIALOG_HEADER)
    initial_x, initial_y = get_coordinates(header)
    drag_and_drop_by_offset(element=header, element_horz_displacement=x_offset, element_vert_displacement=y_offset)
    verify_element_position(header, expected_x=initial_x, expected_y=initial_y)

    # Transitioning to second test case
    open_project(selenium, 'JS Testing')
    create_and_open_live_report(selenium, 'New Live Report')

    #### LayoutPicker is draggable ####
    # Opening LayoutPicker dialog
    dom.click_element(selenium, FORMS_ICON)
    dom.click_element(selenium, MENU_ITEM, 'Create New Layout...')
    # Verify that OkCancel dialog rendered by LayoutPicker is draggable
    header = dom.get_element(selenium, MODAL_DIALOG_HEADER)
    initial_x, initial_y = get_coordinates(header)
    drag_and_drop_by_offset(element=header, element_horz_displacement=x_offset, element_vert_displacement=y_offset)
    verify_element_position(header, expected_x=initial_x + x_offset, expected_y=initial_y + y_offset)
    # Clicking close button so that Selenium can delete live report
    dom.click_element(selenium, CLOSE_BUTTON)


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_advanced_options_plots_can_be_dragged(selenium):
    """
    Test that OkCancel dialog rendered by AdvancedOptionsDialog is draggable
    """
    # Defining expected offsets of dialog
    x_offset = 100
    y_offset = 50
    # Creating a custom layout
    dom.click_element(selenium, FORMS_ICON)
    dom.click_element(selenium, MENU_ITEM, 'Create New Layout...')
    dom.click_element(selenium, CUSTOM_LAYOUT_DIV)
    dom.set_element_value(selenium, NEW_LAYOUT_TITLE_INPUT, 'Title of Custom Layout')
    dom.click_element(selenium, OK_BUTTON)
    # Creating a scatter plot
    add_widget_div = dom.get_elements(selenium, ADD_WIDGET_BUTTON, '+ ADD WIDGET')[0]
    simulate.click(selenium, add_widget_div)
    dom.click_element(selenium, NEW_PLOT_WIDGET_ICON)
    dom.click_element(selenium, SCATTER_PLOT_ICON)
    # Navigating to Advanced Options dialog and dragging it
    stack = dom.get_element(selenium, DIV_LM_STACK, 'Scatter')
    dom.click_element(stack, GOLDEN_LAYOUT_GEAR_MENU_BUTTON)
    dom.click_element(selenium, PLOT_OPTIONS_BB_MENU_ITEM, 'Plot Options…')
    # Adding dragging steps
    header = dom.get_element(selenium, MODAL_DIALOG_HEADER)
    initial_x, initial_y = get_coordinates(header)
    drag_and_drop_by_offset(element=header, element_horz_displacement=x_offset, element_vert_displacement=y_offset)
    verify_element_position(header, expected_x=initial_x + x_offset, expected_y=initial_y + y_offset)
    # Closing Advanced Options dialog and clicking cancel button in div#forms-toolbar so Selenium can delete live report
    dom.click_element(selenium, OK_BUTTON)
    click_cancel(selenium)
