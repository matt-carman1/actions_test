import time

import pytest

from selenium.webdriver import ActionChains
from helpers.change.live_report_picker import merge_live_reports, search_for_live_report, open_live_report
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.verification.element import verify_is_visible
from library import dom, base

control_key = dom.get_ctrl_key()


@pytest.mark.parametrize("first_lreport, second_lreport, lr_merge_type",
                         [["3D Pose Data", "Plots test LR", "Intersection"], ["RPE Test", "Plots test LR", "Union"]])
@pytest.mark.usefixtures("open_project")
def test_merged_live_report(driver, first_lreport, second_lreport, lr_merge_type):
    """
    Merging two live_reports, not auto-opening the merged LR
    and also verifying merged LR.
    :param driver: Selenium Webdriver
    :param first_lreport: first_live_report_name from parametrize data
    :param second_lreport: second_live_report_name from parametrize data
    """
    # passing open_merged_live_report as False means not auto-opening merged LR
    merged_name = merge_live_reports(driver,
                                     first_lreport,
                                     second_lreport,
                                     merge_type=lr_merge_type,
                                     reference_live_report=1,
                                     open_merged_live_report=False)
    open_live_report(driver, merged_name)
    verify_is_visible(driver, TAB_ACTIVE, selector_text=merged_name)
