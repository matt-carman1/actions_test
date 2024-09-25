import pytest

from helpers.change.actions_pane import open_sar_panel
from helpers.change.sar_action import create_sar_scaffold
from helpers.extraction.grid import get_image_status
from helpers.flows.grid import hide_columns_contiguously
from helpers.selection.general import STRUCTURE_IMAGE
from helpers.verification.grid import verify_column_contents
from library import dom

live_report_to_duplicate = {'livereport_name': '2 Compounds 2 Freeform Column', 'livereport_id': '891'}


@pytest.mark.app_defect(reason='SS-37305: flaky test')
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_sar_scaffold_editing(selenium):
    """
    1. Create a SAR scaffold and validate
    2. Edit the added scaffold, and validate
    :param selenium: Webdriver
    :return:
    """
    # ----- Scaffold addition and validation ----- #
    # Hiding irrelevant columns
    hide_columns_contiguously(selenium, 'ID', 'Published Freeform Text Column')

    # Adding a scaffold
    sar_scaffold_edited = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 18 20 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -1.529143 1.518571 0.000000 0\nM  V30 2 C -1.530286 0.090000 0.000000 0\nM  V30 3 C -2.768000 -0.623429 0.000000 0\nM  V30 4 C -2.769143 -2.052000 0.000000 0\nM  V30 5 C -1.532571 -2.767143 0.000000 0\nM  V30 6 C -0.294857 -2.054000 0.000000 0\nM  V30 7 C -0.293714 -0.625429 0.000000 0\nM  V30 8 C 1.065143 -0.185143 0.000000 0\nM  V30 9 O 1.904000 -1.341429 0.000000 0\nM  V30 10 C 1.063143 -2.496571 0.000000 0\nM  V30 11 C 1.507714 1.173143 0.000000 0\nM  V30 12 C 0.668857 2.329714 0.000000 0\nM  V30 13 C 1.509429 3.484571 0.000000 0\nM  V30 14 O 1.069143 4.843429 0.000000 0\nM  V30 15 O 2.867714 3.042000 0.000000 0\nM  V30 16 C 2.866571 1.613429 0.000000 0\nM  V30 17 C 4.287143 1.761714 0.000000 0\nM  V30 18 R# 3.571429 0.371429 0.000000 101 VAL=1 RGROUPS=(1 1)\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 2 4 5\nM  V30 5 1 5 6\nM  V30 6 2 6 7\nM  V30 7 1 2 7\nM  V30 8 1 8 7\nM  V30 9 1 8 9 CFG=1\nM  V30 10 1 9 10\nM  V30 11 1 6 10\nM  V30 12 1 11 8\nM  V30 13 1 11 12 CFG=1\nM  V30 14 1 12 13\nM  V30 15 2 13 14\nM  V30 16 1 13 15\nM  V30 17 1 15 16\nM  V30 18 1 11 16\nM  V30 19 1 16 17\nM  V30 20 1 16 18\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    create_sar_scaffold(selenium, sar_scaffold_edited)

    # Verifying SAR scaffold image exists for the respective compound
    verify_column_contents(selenium, 'R1 (SAR)', [True, False], get_image_status)

    # ----- Editing scaffold and validation ----- #
    open_sar_panel(selenium)
    dom.click_element(selenium, STRUCTURE_IMAGE)
    sar_scaffold = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 19 20 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -3.173714 -2.021143 0.000000 0\nM  V30 2 C -3.891714 -0.786000 0.000000 0\nM  V30 3 O -4.850286 0.273143 0.000000 0\nM  V30 4 C -4.139429 1.512286 0.000000 0\nM  V30 5 O -4.724000 2.815714 0.000000 0\nM  V30 6 C -2.741428 1.218857 0.000000 0\nM  V30 7 C -2.588000 -0.201429 0.000000 0\nM  V30 8 C -1.349143 -0.912286 0.000000 0\nM  V30 9 C -0.114000 -0.194571 0.000000 0\nM  V30 10 C 1.125143 -0.905429 0.000000 0\nM  V30 11 C 1.129143 -2.333714 0.000000 0\nM  V30 12 O 2.368286 -3.044571 0.000000 0\nM  V30 13 C 2.360572 -0.187714 0.000000 0\nM  V30 14 C 2.356286 1.240857 0.000000 0\nM  V30 15 C 1.117143 1.951714 0.000000 0\nM  V30 16 C -0.118000 1.234000 0.000000 0\nM  V30 17 C -1.357143 1.944571 0.000000 0\nM  V30 18 O -1.361143 3.373143 0.000000 0\nM  V30 19 R# -5.142857 -1.514286 0.000000 101 VAL=1 RGROUPS=(1 1)\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 3 4\nM  V30 4 2 4 5\nM  V30 5 1 4 6\nM  V30 6 1 7 6\nM  V30 7 1 7 2\nM  V30 8 1 7 8 CFG=1\nM  V30 9 1 8 9\nM  V30 10 2 9 10\nM  V30 11 1 10 11\nM  V30 12 1 11 12\nM  V30 13 1 10 13\nM  V30 14 2 13 14\nM  V30 15 1 14 15\nM  V30 16 2 15 16\nM  V30 17 1 9 16\nM  V30 18 1 16 17\nM  V30 19 2 17 18\nM  V30 20 1 2 19\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    create_sar_scaffold(selenium, sar_scaffold)
    verify_column_contents(selenium, 'R1 (SAR)', [False, True], get_image_status)
