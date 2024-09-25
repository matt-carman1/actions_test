import pytest

from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.grid_columns import get_cell
from helpers.change.live_report_picker import open_live_report
from helpers.flows.live_report_management import copy_active_live_report
from helpers.selection.grid import GRID_ROWS_CONTAINER, GRID_PENDING_CELLS, Footer
from helpers.verification.grid import verify_footer_values, check_for_butterbar
from helpers.verification.live_report import verify_live_report_open
from library import dom, scroll, wait


@pytest.mark.app_defect(reason="SS-32648: Flaky Test on master")
@pytest.mark.serial
@pytest.mark.usefixtures("open_project")
def test_duplicate_large_lr(selenium):
    """
    Test duplication of a large live report (10k compounds), ensuring butter bar appears
    and that cell values load (are no longer pending) in a reasonable amount of time.

    :param selenium: Webdriver
    :return:
    """

    open_live_report(selenium, name='10k Selenium Test LR')
    copied_lr_name = copy_active_live_report(selenium, '10k Selenium Test LR', '10k Selenium Test LR Copy', False)

    # butter bar should display, and then should disappear
    check_for_butterbar(selenium, notification_text='Duplicating Live Report', visible=True)
    check_for_butterbar(selenium, notification_text='Duplicating Live Report', visible=False)

    # verify the duplicate opens and visible cells at the top of the LR are not pending after 20 seconds
    verify_live_report_open(selenium, copied_lr_name, pending_timeout=20)

    # make sure footer indicates correct number of compounds
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(10001)})

    # TODO: Remove the commented lines of code below after this is fixed SS-31927
    # sort_grid_by(selenium, 'ID')

    # Remove the commented lines of code below after this is fixed SS-31927
    # verify a cell's content in first row
    # first_cell_mw = get_cell(selenium, 'CHEMBL103', 'Molecular Weight (Molecular Weight')
    # assert first_cell_mw.text == '314', "Expected the first cell's MW value to be 314 but got " + first_cell_mw.text

    # scroll to bottom
    # grid = dom.get_element(selenium, GRID_ROWS_CONTAINER)
    # scroll.wheel_to_bottom(selenium, grid)
    # wait.until_visible(selenium, '.row-index', '10000')
    #
    # # TODO (maas) remove this after SS-24726, when results will be requested onScrollEnd and this will no longer be necessary
    # scroll.wheel_element(selenium, grid, -1)
    #
    # # verify the visible cells at the bottom of the LR are not pending after 20 seconds
    # wait.until_not_visible(selenium, GRID_PENDING_CELLS, timeout=20)
    #
    # # verify a cell's content in last row
    # last_cell_mw = get_cell(selenium, 'V055814', 'Molecular Weight (Molecular Weight')
    # assert last_cell_mw.text == '265', "Expected the last cell's MW value to be 265 but got " + last_cell_mw.text
