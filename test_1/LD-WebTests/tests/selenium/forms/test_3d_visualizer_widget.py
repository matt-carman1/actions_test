"""
3D Visualizer widget smoke test for forms
"""
import pytest

from helpers.change.forms import add_spreadsheet_widget, add_3d_visualizer_widget, create_new_layout, save_forms_layout
from helpers.change.visualize import click_visualize_icon
from helpers.selection.forms import ADD_WIDGET_TOOLBAR_BUTTON, VISUALIZER_WIDGET_ICON, FORM_STACK, CLOSE_TAB
from helpers.selection.grid import GRID_ICON
from helpers.selection.visualize import WEBPYMOL_CANVAS
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from library import dom, simulate, wait

live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}


@pytest.mark.smoke
def test_3d_visualizer_widget(selenium, duplicate_live_report, open_livereport):
    """
    Tests to ensure:
    1. an added 3D Visualizer widget shows receptor and ligands and
    2. only one 3D Visualizer can be added via the 'Add a widget' dialog
    """
    # ----- TEST SETUP ----- #
    create_new_layout(selenium, title=duplicate_live_report, layout="Create New Layout")
    # Close last widget space
    wait.until_visible(selenium, selector=CLOSE_TAB)
    element_to_click = dom.get_elements(selenium, selector=CLOSE_TAB)[1]
    simulate.click(selenium, element_to_click)
    # Add Spreadsheet widget
    add_spreadsheet_widget(selenium)
    # Add 3d Visualizer widget
    add_3d_visualizer_widget(selenium, duplicate_live_report)

    # click the visualize eye icon
    spreadsheet_widget = dom.get_elements(selenium, FORM_STACK)[0]
    click_visualize_icon(spreadsheet_widget, column_name='Fake 3D model with 2 Poses (3D)', structure_id='CRA-035000')

    # ----- VALIDATION ----- #
    # Validate a second 3d Visualizer can not be added
    dom.click_element(selenium, ADD_WIDGET_TOOLBAR_BUTTON)
    verify_is_not_visible(selenium, VISUALIZER_WIDGET_ICON)

    dom.click_element(selenium, 'button', 'X')
    wait.until_visible(selenium, ADD_WIDGET_TOOLBAR_BUTTON)

    # Check the 3d container is up
    verify_is_visible(selenium, WEBPYMOL_CANVAS)
    save_forms_layout(selenium)
    dom.click_element(selenium, GRID_ICON)
    click_visualize_icon(selenium, column_name='Fake 3D model with 2 Poses (3D)', structure_id='CRA-035000')
    verify_is_visible(selenium, WEBPYMOL_CANVAS)
