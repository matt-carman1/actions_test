"""
This test opens a live report, sorts it and then verifies the contents is as
expected.

NOTE: The LR that is opened has more rows and columns than will fit on the
screen, so this test really just testing that the page-scrolling code in
selenium_tests works as expected.
"""

import pytest

from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.live_report_picker import open_live_report
from helpers.verification.grid import verify_grid_contents


@pytest.mark.usefixtures("open_project")
def test_grid_scroll(selenium):
    open_live_report(selenium, alias=881)
    sort_grid_by(selenium, 'ID', sort_ascending=True)
    verify_grid_contents(
        selenium, {
            'ID': [
                'CRA-035507',
                'CRA-035508',
                'CRA-035509',
                'CRA-035510',
                'CRA-035511',
                'CRA-035512',
                'CRA-035513',
                'CRA-035514',
                'CRA-035516',
                'CRA-035517',
                'CRA-035518',
                'CRA-035519',
                'CRA-035520',
                'CRA-035521',
                'CRA-035522',
                'CRA-035524',
                'CRA-035525',
                'CRA-035526',
                'CRA-035527',
                'CRA-035528',
                'CRA-035529',
                'CRA-035530',
                'CRA-035531',
                'CRA-035532',
                'CRA-035533',
                'CRA-035534',
                'CRA-035535',
                'CRA-035536',
                'CRA-035537',
                'CRA-035538',
                'CRA-035539',
                'CRA-035541',
                'CRA-035542',
                'CRA-035544',
                'CRA-035545',
                'CRA-035546',
                'CRA-035547',
                'CRA-035548',
                'CRA-035549',
                'CRA-035550',
                'CRA-035551',
                'CRA-035552',
                'CRA-035553',
                'CRA-035554',
                'CRA-035555',
                'CRA-035557',
                'CRA-035558',
                'CRA-035560',
                'CRA-035561',
                'CRA-035563',
            ],
            'r_glide_XP_Sitemap (undefined)': [
                '-0.00246',
                '-0.528',
                '0.386',
                '-0.637',
                '-0.0396',
                '-0.131',
                '-0.278',
                '0.158',
                '-0.217',
                '0.659',
                '-0.367',
                '0.205',
                '-1.35',
                '0.397',
                '0.176',
                '-0.127',
                '-0.255',
                '0.27',
                '-0.216',
                '0.261',
                '0.00295',
                '-0.16',
                '-0.408',
                '-0.0476',
                '0.0491',
                '-1.28',
                '0.495',
                '-0.727',
                '0.252',
                '0.168',
                '-0.202',
                '-0.495',
                '0.166',
                '-0.574',
                '-0.476',
                '-0.464',
                '0.68',
                '-0.419',
                '0.659',
                '0.501',
                '0.419',
                '-0.832',
                '0.292',
                '-0.431',
                '-0.367',
                '-0.849',
                '-0.124',
                '0.653',
                '-0.851',
                '-0.122',
            ],
            'Rationale': ['demo:\nA large Live Report based on the 100 Ideas SDF.'] * 50
        })
