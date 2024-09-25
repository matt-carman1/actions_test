"""

Test to confirm R-Group images show as expected.

"""

import pytest

from helpers.change.actions_pane import close_add_compounds_panel
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.change.grid_columns import select_multiple_contiguous_columns
from helpers.change.sar_action import create_sar_scaffold
from helpers.extraction.grid import get_image_status
from helpers.flows.add_compound import search_by_id
from helpers.verification.grid import verify_column_contents


@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_sar_scaffold_images(selenium):
    """
    Create two SAR scaffolds and verify R-Group images show as expected for structures in the LR.
    """

    # ----- LR Setup ----- #
    # Add compounds to LR via Search by ID
    structure_id_1, structure_id_2, structure_id_3, structure_id_4 = "CRA-032664", "CRA-032703", "CRA-032913", "V035752"
    search_by_id(selenium, ", ".join([structure_id_1, structure_id_2, structure_id_3, structure_id_4]))
    close_add_compounds_panel(selenium)

    # Hide irrelevant columns
    select_multiple_contiguous_columns(selenium, "ID", "Lot Scientist")
    click_column_menu_item(selenium, "Lot Scientist", "Hide")
    # Apply sorting to prevent unexpected structure row ordering
    click_column_menu_item(selenium, "Compound Structure", 'Sort', "Ascending", exact_text_match=True)

    # ----- Create 2 Scaffolds ----- #
    # Add first scaffold
    sar_scaffold_01 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 15 16 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -2.282571 -1.757143 0.000000 0\nM  V30 2 O -2.281429 -0.328571 0.000000 0\nM  V30 3 C -1.043714 0.384571 0.000000 0\nM  V30 4 C -1.042571 1.813143 0.000000 0\nM  V30 5 O -2.279143 2.528571 0.000000 0\nM  V30 6 R# -2.278000 3.957143 0.000000 102 VAL=1 RGROUPS=(1 2)\nM  V30 7 C 0.195143 2.526571 0.000000 0\nM  V30 8 C 1.431714 1.811143 0.000000 0\nM  V30 9 N 2.669429 2.524571 0.000000 0\nM  V30 10 C 3.906000 1.809429 0.000000 0\nM  V30 11 C 3.904857 0.380857 0.000000 0\nM  V30 12 C 2.667143 -0.332571 0.000000 0\nM  V30 13 R# 2.666000 -1.761143 0.000000 101 VAL=1 RGROUPS=(1 1)\nM  V30 14 C 1.430571 0.382571 0.000000 0\nM  V30 15 C 0.192857 -0.330571 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 1 5 6\nM  V30 6 1 4 7\nM  V30 7 2 7 8\nM  V30 8 1 8 9\nM  V30 9 2 9 10\nM  V30 10 1 10 11\nM  V30 11 2 11 12\nM  V30 12 1 12 13\nM  V30 13 1 12 14\nM  V30 14 2 14 15\nM  V30 15 1 15 3\nM  V30 16 1 14 8\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    create_sar_scaffold(selenium, sar_scaffold_01)

    # Add second scaffold
    sar_scaffold_02 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 9 9 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 F 1.864571 2.451714 0.000000 0\nM  V30 2 C 0.622857 1.745143 0.000000 0\nM  V30 3 C 0.613714 0.316857 0.000000 0\nM  V30 4 C -0.628000 -0.389714 0.000000 0\nM  V30 5 C -1.860572 0.332571 0.000000 0\nM  V30 6 N -3.102286 -0.373714 0.000000 0\nM  V30 7 R# -4.334857 0.348571 0.000000 101 VAL=1 RGROUPS=(1 1)\nM  V30 8 C -1.851429 1.761143 0.000000 0\nM  V30 9 C -0.609714 2.467429 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 2 4 5\nM  V30 5 1 5 6\nM  V30 6 1 6 7\nM  V30 7 1 5 8\nM  V30 8 2 8 9\nM  V30 9 1 9 2\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    create_sar_scaffold(selenium, sar_scaffold_02)

    # ----- TEST PASSING CRITERIA ----- #
    # Verify R1/R2 SAR images show for compounds
    verify_column_contents(selenium, 'R1 (SAR)', [True, True, False, True], get_image_status)
    verify_column_contents(selenium, 'R2 (SAR)', [True, True, False, False], get_image_status)
