"""
Selenium test for grid performance (gauged via cell rerenders) during selection, hover, and scroll. 
"""

import pytest

from helpers.change.grid_row_actions import select_row, hover_row
from helpers.change.live_report_picker import open_live_report
from helpers.extraction.grid import get_grid_render_count_map, get_row_entity_id
from helpers.selection.grid import GRID_ROWS_CONTAINER
from helpers.verification.grid import verify_reasonable_initial_render_count, verify_row_selected, verify_render_count, \
    verify_row_hovered
from helpers.verification.live_report import verify_live_report_open
from library import dom
from library.scroll import user_scroll


@pytest.mark.app_defect(reason="SS-35552: Flaky test - got 'KeyError' while attempting to call verify_render_count")
@pytest.mark.usefixtures("open_project")
def test_grid_performance(selenium):
    """
     By counting renders from GridCell's RENDER_COUNT_MAP
     this test ensures cells don't render an excessive
     number of times during selection, hover, & scroll.

     TODO make this stricter. For now the test fails if we
     try to hold it to "higher standards". In [brackets]
     throughout are the values we should be able to achieve.
     :param selenium: Selenium WebDriver
     """

    open_live_report(selenium, '50 Compounds 10 Assays')
    verify_live_report_open(selenium, '50 Compounds 10 Assays')

    # ------- Setup ------- #
    baseline_counts = get_grid_render_count_map(selenium)
    first_row_id = get_row_entity_id(selenium, 0)
    second_row_id = get_row_entity_id(selenium, 1)
    third_row_id = get_row_entity_id(selenium, 2)

    # ------- Initial Render Count ------- #
    verify_reasonable_initial_render_count(selenium)

    # ------- Selection Render Count ------- #
    select_row(selenium, first_row_id)
    verify_row_selected(selenium, first_row_id)

    # selected row's cells should render no more than twice from the selection
    # [5 should be 2]
    verify_render_count(selenium, first_row_id, 5, baseline_counts[first_row_id])
    # another row's cells shouldn't re-render from the selection
    # [4 should be 0]
    verify_render_count(selenium, third_row_id, 4, baseline_counts[third_row_id])

    # ------- Hover Render Count ------- #
    hover_row(selenium, second_row_id)
    verify_row_hovered(selenium, second_row_id)

    # hovered row's cells should render no more than twice from the hover
    # [5 should be 2]
    verify_render_count(selenium, second_row_id, 5, baseline_counts[second_row_id])
    # another row's cells shouldn't re-render from the hover
    # [4 should be 0]
    verify_render_count(selenium, third_row_id, 4, baseline_counts[third_row_id])

    # ------- Scroll Render Count ------- #
    row_container = dom.get_element(selenium, GRID_ROWS_CONTAINER)
    user_scroll(selenium, row_container, 300)
    # a row should not re-render as a result of scrolling
    # [4 should be 0]
    verify_render_count(selenium, third_row_id, 4, baseline_counts[third_row_id])
