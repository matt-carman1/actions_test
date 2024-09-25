import pytest

from helpers.change.actions_pane import open_add_compounds_panel, open_sar_panel
from helpers.selection.actions_pane import ACTION_PANE_HEADER_TITLE, TOOLS_BUTTON
from helpers.selection.grid import GRID_HEADER_CELL
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.selection.sketcher import ADD_SAR_BUTTON
from helpers.verification.color import verify_element_color
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from library import dom

LD_PROPERTIES = {'LIVEDESIGN_MODE': 'MATERIALS_SCIENCE', 'ENABLE_DEVICE_LIVE_REPORTS': 'true'}

live_report_to_duplicate = {'livereport_name': '5 Fragments 4 Assays', 'livereport_id': '2248'}


@pytest.mark.usefixtures('customized_server_config')
def test_compound_live_report(selenium, duplicate_live_report, open_livereport):
    tab = dom.get_element(selenium, TAB_ACTIVE, text=duplicate_live_report)

    # Tab should have blue background
    verify_element_color(tab, (239, 239, 239))

    # Tab should have icon
    verify_is_visible(tab, '.compound-report-icon')

    # LR should have Compound Structure column
    verify_is_visible(selenium, GRID_HEADER_CELL + '[title="Compound Structure"]')

    # LR should not have "Device Recipe" column
    verify_is_not_visible(selenium, GRID_HEADER_CELL + '[title="Device Recipe"]')

    # Pane title should be "COMPOUNDS"
    open_add_compounds_panel(selenium)
    verify_is_not_visible(selenium, ACTION_PANE_HEADER_TITLE, selector_text='DEVICES')
    verify_is_visible(selenium, ACTION_PANE_HEADER_TITLE, selector_text='COMPOUNDS')

    # Analysis tools should be enabled for Compound LRs
    verify_is_visible(selenium, TOOLS_BUTTON)
    verify_is_not_visible(selenium, TOOLS_BUTTON + '[title="Disabled because the active Live Report is for devices."]')
    open_sar_panel(selenium)

    # Text is SPR not SAR
    verify_is_visible(selenium, ADD_SAR_BUTTON, selector_text='SPR Scaffold')
