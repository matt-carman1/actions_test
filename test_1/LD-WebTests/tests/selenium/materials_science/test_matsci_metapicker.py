import pytest

from helpers.change.live_report_picker import open_metapicker
from helpers.selection.live_report_picker import REPORT_PICKER, REPORT_LIST_TITLE, REPORT_LIST_BODY
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from library import dom

LD_PROPERTIES = {'LIVEDESIGN_MODE': 'MATERIALS_SCIENCE', 'ENABLE_DEVICE_LIVE_REPORTS': 'true'}


@pytest.mark.usefixtures("open_project")
@pytest.mark.usefixtures('customized_server_config')
def test_matsci_metapicker(selenium):
    open_metapicker(selenium)
    picker = dom.get_element(selenium, REPORT_PICKER)
    live_report_list = dom.get_element(selenium, REPORT_LIST_BODY)
    dom.click_element(picker, 'a', 'All LiveReports')

    # every LR should have an icon.
    verify_is_not_visible(
        live_report_list,
        REPORT_LIST_TITLE + ':not(.device-report-icon):not(.reaction-report-icon):not(.compound-report-icon)')

    # device LR should have device icon
    dom.click_element(picker, 'a', 'Materials Science')
    verify_is_visible(live_report_list, REPORT_LIST_TITLE + '.device-report-icon', selector_text='Device Test')

    # other LRs must have compound icon
    # (the actual check is: there are LRs visible and no LRs must be visible without the compound report icon)
    dom.click_element(picker, 'a', 'Selenium Testing')
    verify_is_visible(live_report_list, REPORT_LIST_TITLE, error_if_selector_matches_many_elements=False)
    verify_is_not_visible(live_report_list, REPORT_LIST_TITLE + ':not(.compound-report-icon)')
