import pytest

from helpers.change.actions_pane import open_add_compounds_panel, open_sar_panel, open_tools_pane
from helpers.change.live_report_menu import switch_to_live_report, close_live_report
from helpers.change.live_report_picker import open_live_report
from helpers.selection.actions_pane import ACTION_PANE_HEADER_TITLE, TOOLS_BUTTON, ADD_COMPOUND_PANEL
from helpers.selection.grid import GRID_HEADER_CELL
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.verification.color import verify_element_color
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from library import dom
from helpers.verification.features_enabled_disabled import verify_import_from_file_is_disabled, \
    verify_import_from_file_is_enabled, verify_structure_search_is_enabled, verify_sar_button_is_disabled, \
    verify_sar_button_is_enabled, verify_compound_design_tab_is_disabled, verify_structure_search_is_disabled

LD_PROPERTIES = {'LIVEDESIGN_MODE': 'MATERIALS_SCIENCE', 'ENABLE_DEVICE_LIVE_REPORTS': 'true'}
test_report_type = 'device'


@pytest.mark.usefixtures("customized_server_config")
def test_device_live_report(selenium, new_live_report, open_livereport):
    """
    Basic smoke test of device-type LR. Verify
    * tab color, icon
    * enabled state of various add entity options
    * various text strings
    * the add entities panel remembers previously opened panel in a compound LR after switching from device-type LR

    :param selenium: Selenium Webdriver
    :param customized_server_config: fixture to set the custom LD properties
    :param: new_live_report: fixture to create a new LiveReport
    :param: open_livereport: fixture to open a LiveReport
    """
    # device_lr_name = create_and_open_live_report(selenium, report_name='device', lr_type='Devices')
    device_lr_name = new_live_report
    tab = dom.get_element(selenium, TAB_ACTIVE, text=device_lr_name)

    # Tab should have blue background
    verify_element_color(tab, (211, 229, 234))

    # Tab should have icon
    verify_is_visible(tab, '.device-report-icon')

    # LR should not have Compound Structure column
    verify_is_not_visible(selenium, GRID_HEADER_CELL + '[title="Compound Structure"]')

    # LR should have "Device Recipe" column
    verify_is_visible(selenium, GRID_HEADER_CELL + '[title="Device Recipe"]')

    # Only "Add by ID" should be visible for device LRs...
    open_add_compounds_panel(selenium)

    # In other words, clicking on other headers should do nothing
    verify_compound_design_tab_is_disabled(selenium)
    verify_structure_search_is_disabled(selenium)
    verify_import_from_file_is_disabled(selenium)

    # Pane title should be "DEVICES"
    add_devices_pane_title_selector = '{} {}'.format(ADD_COMPOUND_PANEL, ACTION_PANE_HEADER_TITLE)
    verify_is_visible(selenium, add_devices_pane_title_selector, selector_text='DEVICES')

    # SAR should be disabled for Device LRs
    verify_is_visible(selenium, TOOLS_BUTTON)
    # NOTE(jordan) This check is disabled until SS-42428 is fixed
    # verify_sar_button_is_disabled(selenium)

    # Switching to a compound LR should cause other accordion panes to become active and panel title should
    # change to "COMPOUNDS"
    compounds_live_report = '5 Compounds 4 Assays'
    open_live_report(selenium, compounds_live_report)

    open_add_compounds_panel(selenium)
    verify_structure_search_is_enabled(selenium)
    verify_import_from_file_is_enabled(selenium)
    verify_is_visible(selenium, add_devices_pane_title_selector, selector_text='COMPOUNDS')

    # SAR should be visible but should not have the "disabled" tooltip text
    verify_is_visible(selenium, TOOLS_BUTTON)
    verify_sar_button_is_enabled(selenium)

    # Switching back to the device LR should cause other accordion panes to become disabled and panel title should
    # change to "DEVICES"
    switch_to_live_report(selenium, device_lr_name)

    open_add_compounds_panel(selenium)
    verify_structure_search_is_disabled(selenium)
    verify_import_from_file_is_disabled(selenium)
    verify_is_visible(selenium, add_devices_pane_title_selector, selector_text='DEVICES')
    verify_is_not_visible(selenium, add_devices_pane_title_selector, selector_text='COMPOUNDS')
    # NOTE(jordan) This check is disabled until SS-42428 is fixed
    # verify_sar_button_is_disabled(selenium)

    close_live_report(selenium, compounds_live_report)
