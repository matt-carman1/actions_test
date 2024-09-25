"""
Changes to the webmol for 3D columns
"""
from library import dom, wait, iframe
from helpers.selection.visualize import BUILDER_PANEL_EXIT, BUILDER_PANEL


@iframe.within_iframe('#webmol')
def close_webmol_builder_panel(driver):
    wait.until_visible(driver, '{} .builder-label-container'.format(BUILDER_PANEL), timeout=180)
    dom.click_element(driver, BUILDER_PANEL_EXIT)
