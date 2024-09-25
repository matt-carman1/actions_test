import pytest

from helpers.selection.actions_pane import HELP_LINK
from library import dom

LD_PROPERTIES = {'LIVEDESIGN_MODE': 'MATERIALS_SCIENCE', 'ENABLE_HELP_LINK_TO_TUTORIAL_ENDPOINT': 'false'}


@pytest.mark.usefixtures('customized_server_config')
@pytest.mark.usefixtures('open_project')
def test_compound_live_report(selenium):
    help_link = dom.get_element(selenium, HELP_LINK)
    assert help_link.get_attribute('href').endswith('documentation-matsci')
