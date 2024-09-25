import pytest
import time

from helpers.change.actions_pane import open_add_compounds_panel, open_compound_search_panel
from library import dom
from library.scroll import scroll_element_by


@pytest.mark.skip(reason="This was added only to test the helper 'scroll_element_by'. Leaving it here but marking it "
                  "skip to avoid unnecessary test being run on jenkins.")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_scroll_compounds_panel(selenium):
    """

    :param selenium:  Selenium Webdriver
    """

    open_add_compounds_panel(selenium)
    open_compound_search_panel(selenium)
    time.sleep(10)
    scroll_ele = dom.get_element(selenium, '#compounds-pane-container .active-tab-content', timeout=10)
    distance_from_top = scroll_element_by(selenium, scroll_ele, 0, 150)
    assert distance_from_top == 150
    distance_from_top = scroll_element_by(selenium, scroll_ele, 0, -50)
    assert distance_from_top == 100
    distance_from_top = scroll_element_by(selenium, scroll_ele, 0, 150)
    assert distance_from_top == 250
