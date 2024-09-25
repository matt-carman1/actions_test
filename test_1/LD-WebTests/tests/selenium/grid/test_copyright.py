from datetime import datetime

import pytest

from helpers.change.live_report_picker import open_live_report
from helpers.change.tile_view import switch_to_tile_view
from helpers.selection.grid import GRID_FOOTER_COPYRIGHT
from helpers.selection.login import DISCLAIMER
from helpers.selection.modal import MODAL_DIALOG
from helpers.selection.project import CHANGE_PROJECT_ICON, PROJECT_COPYRIGHT_NOTICE
from library import dom, url
from library.url_endpoints import LOGIN_URL, COPYRIGHT_URL

COPYRIGHT = 'Copyright notices'
SCHRODINGER_END_USER_AGREEMENT = 'Schrödinger End-User License Agreement'
SCHRODINGER_EULA_URL = 'http://www.schrodinger.com/Legal/eula.html'


@pytest.mark.usefixtures('open_project')
def test_copyright_project(selenium):
    """
    Test Copyright for LiveDesign Project picker window

    :param selenium: selenium webdriver
    """
    dom.click_element(selenium, CHANGE_PROJECT_ICON)
    project_modal = dom.get_element(selenium, MODAL_DIALOG)
    project_copyright_notice = dom.get_element(project_modal, PROJECT_COPYRIGHT_NOTICE)
    assert project_copyright_notice.text == 'By clicking OK, you agree to use LiveDesign in accordance ' \
                                            'with theSchrödinger End-User License Agreement.Copyright notices'
    links = dom.get_elements(project_copyright_notice, 'a')
    assert len(links) == 2
    assert links[0].text == SCHRODINGER_END_USER_AGREEMENT
    assert links[0].get_attribute('href') == SCHRODINGER_EULA_URL
    assert links[1].text == COPYRIGHT
    assert links[1].get_attribute('href') == COPYRIGHT_URL


@pytest.mark.usefixtures('open_project')
def test_copyright_grid_footer(selenium):
    """
    Test copyright for grid footer in spreadsheet view and tile view.

    :param selenium: selenium webdriver
    """
    open_live_report(selenium, '5 Compounds 4 Assays')
    verify_footer_copyright(selenium)
    switch_to_tile_view(selenium)
    verify_footer_copyright(selenium)


def test_login_copyright(selenium):
    """
    Test copyright for login page

    :param selenium: selenium webdriver
    """
    url.go_to_url(selenium, LOGIN_URL)
    login_copyright_notice = dom.get_element(selenium, DISCLAIMER)
    assert login_copyright_notice.text == 'By clicking Log in, you agree to use LiveDesign in accordance with the\n' \
                                          'Schrödinger End-User License Agreement. Copyright notices'
    links = dom.get_elements(login_copyright_notice, 'a')
    assert len(links) == 2
    assert links[0].text == SCHRODINGER_END_USER_AGREEMENT
    assert links[0].get_attribute('href').startswith(SCHRODINGER_EULA_URL)
    assert links[1].text == COPYRIGHT
    assert links[1].get_attribute('href') == COPYRIGHT_URL


def verify_footer_copyright(driver):
    """
    Verifies footer copyright for spreadsheet view and tile view.

    :param driver: selenium webdriver
    """
    footer_copyright_notice = dom.get_element(driver, GRID_FOOTER_COPYRIGHT)
    current_year = datetime.now().year

    assert footer_copyright_notice.text == '© {} Schrödinger, Inc.Copyright noticesEULA'.format(current_year)

    links = dom.get_elements(footer_copyright_notice, 'a')
    assert len(links) == 2
    assert links[0].text == COPYRIGHT
    assert links[0].get_attribute('href') == COPYRIGHT_URL
    assert links[1].text == 'EULA'
    assert links[1].get_attribute('href') == SCHRODINGER_EULA_URL
