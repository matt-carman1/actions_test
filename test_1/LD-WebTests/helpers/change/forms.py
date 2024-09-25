from helpers.selection.forms import (ADD_WIDGET_BUTTON, ASSAY_VIEWER, COMPOUND_DETAIL, CUSTOM_LAYOUT_DIV, FORMS_ICON,
                                     FORMS_TOOLBAR, PLOT_VIEW, SAVE_LAYOUT_TOOLBAR_BUTTON, SPREADSHEET_WIDGET_ICON,
                                     VISUALIZER_WIDGET_ICON, VISUALIZER_WIDGET_NAME_INPUT)
from helpers.selection.modal import MODAL_DIALOG_HEADER, NEW_LAYOUT_TITLE_INPUT
from helpers.selection.general import MENU_ITEM
from library import dom, wait, simulate
from library.base import click_ok
from library.dom import LiveDesignWebException


def create_new_layout(driver, title, layout='Compound Detail'):
    """
    Creates a new layout

    :param driver: webdriver
    :param title: str, name of the new layout
    :param layout: str, name of the layout option.
                    Options:
                        1. 'Compound Detail'
                        2. 'Plot View'
                        3. 'Assay Viewer'
                        4. 'Create New Layout'
    """
    options = {
        'Compound Detail': COMPOUND_DETAIL,
        'Plot View': PLOT_VIEW,
        'Assay Viewer': ASSAY_VIEWER,
        'Create New Layout': CUSTOM_LAYOUT_DIV
    }
    if layout not in options:
        raise LiveDesignWebException('option must be one of the following: {}'.format(options.keys()))
    dom.click_element(driver, FORMS_ICON)
    dom.click_element(driver, MENU_ITEM, 'Create New Layout...')
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Add a Layout\nX')
    dom.click_element(driver, options[layout])
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Create New Layout')
    dom.set_element_value(driver, NEW_LAYOUT_TITLE_INPUT, title)
    click_ok(driver)


def open_saved_layout(driver, title):
    """
    Open a saved forms layout

    :param driver: webdriver
    :param title: str, name of the saved layout to open
    """
    dom.click_element(driver, FORMS_ICON)
    dom.click_element(driver, MENU_ITEM, title)


def add_spreadsheet_widget(driver, nth_element=0):
    """
    Use while in forms layout. Adds a spreadsheet widget

    :param driver: webdriver
    :param nth_element: int, the nth "+ ADD WIDGET" button
    """
    wait.until_visible(driver, ADD_WIDGET_BUTTON)
    button_to_click = dom.get_elements(driver, ADD_WIDGET_BUTTON)[nth_element]
    simulate.click(driver, button_to_click)
    dom.click_element(driver, SPREADSHEET_WIDGET_ICON)


def add_3d_visualizer_widget(driver, title, nth_element=0):
    """
    Use while in forms layout. Adds a 3D Visualizer widget

    :param driver: webdriver
    :param title: str, name of the 3D Visualizer
    :param nth_element: int, the nth "+ ADD WIDGET" button
    """
    wait.until_visible(driver, ADD_WIDGET_BUTTON)
    button_to_click = dom.get_elements(driver, ADD_WIDGET_BUTTON)[nth_element]
    simulate.click(driver, button_to_click)
    wait.until_visible(driver, VISUALIZER_WIDGET_ICON)
    dom.click_element(driver, VISUALIZER_WIDGET_ICON)
    dom.set_element_value(driver, VISUALIZER_WIDGET_NAME_INPUT, title)
    click_ok(driver)


def save_forms_layout(driver):
    """
    Use while in forms layout. Saves and closes the forms editor.

    :param driver: webdriver
    """
    dom.click_element(driver, SAVE_LAYOUT_TOOLBAR_BUTTON)
    wait.until_not_visible(driver, FORMS_TOOLBAR)
    wait.sleep_if_k8s(1)
