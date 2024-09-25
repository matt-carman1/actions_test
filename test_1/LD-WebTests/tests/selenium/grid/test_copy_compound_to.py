"""
Test to ensure the grid submenu options in "Use in" work as expected.
"""
import pytest
from helpers.change.actions_pane import open_add_compounds_panel
from helpers.change.enumeration import close_enumeration_wizard
from helpers.change.grid_columns import click_compound_row
from helpers.change.grid_row_menu import copy_compound_to_live_report
from helpers.change.live_report_menu import switch_to_live_report, delete_open_live_report
from helpers.flows.grid import edit_rationale_in_grid_view
from helpers.flows.sketcher import use_compound_in_sketcher_and_verify
from helpers.selection.sketcher import RGROUP_SCAFFOLD_IFRAME
from helpers.verification.grid import verify_grid_contents
from helpers.verification.maestro import verify_molv_from_maestro_equals

# LD_PROPERTIES = {'ENABLE_INTERNAL_SCAFFOLD_ENUMERATION': 'true'}
live_report_to_duplicate = {'livereport_name': "Test Reactants - Nitriles", 'livereport_id': '2553'}


@pytest.mark.require_webgl
# @pytest.mark.usefixtures("customized_server_config")
def test_copy_compound_to(selenium, duplicate_live_report, open_livereport):
    """
    Duplicates an LR and sends compounds via the grid submenu option "Use in" to:
    1. Design Sketcher, #sketcher-js
    2. a new LiveReport
    3. an existing LiveReport
    4. the R-Group enumeration Sketcher, #enumeration-scaffold-sketcher

    :param selenium: Webdriver
    :param duplicate_live_report: fixture to duplicate Live Report
    """
    # ----- STRUCTURE TO COPY TO ----- #
    structure_existing_lr = {
        "ID":
            "V047518",
        "smiles":
            "CCC#N",
        "molv":
            "\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 4 3 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C 2.325429 1.539429 0.000000 0\nM  V30 2 C 1.605714 0.305429 0.000000 0\nM  V30 3 C 0.177143 0.311714 0.000000 0\nM  V30 4 N -1.251429 0.318000 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 3 3 4\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n"
    }
    structure_new_lr = {
        "ID":
            "V047755",
        "smiles":
            "N#CC1=CC=CC=C1",
        "molv":
            "\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 8 8 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 N -2.681143 -1.213714 0.000000 0\nM  V30 2 C -1.439429 -0.507143 0.000000 0\nM  V30 3 C -0.197714 0.199143 0.000000 0\nM  V30 4 C 1.034857 -0.523143 0.000000 0\nM  V30 5 C 2.276571 0.183143 0.000000 0\nM  V30 6 C 2.285714 1.611714 0.000000 0\nM  V30 7 C 1.053143 2.334000 0.000000 0\nM  V30 8 C -0.188571 1.627429 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 3 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 3 8\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n"
    }

    # ----- STRUCTURE COPIED TO SKETCHER ----- #
    # Added this to reduce time it takes for the compound to appear in the sketcher (prevent flakiness)
    open_add_compounds_panel(selenium)
    # Right click structure, hover over "Copy Compound to", and select "Sketcher" option
    use_compound_in_sketcher_and_verify(selenium, structure_new_lr['ID'], interval=1000)
    # Validate expected compound appears in the sketcher
    verify_molv_from_maestro_equals(selenium, structure_new_lr["molv"].split('\n')[5].split()[3:5])

    # ----- STRUCTURE COPIED TO A NEW LR ----- #
    edit_rationale_in_grid_view(selenium, 'This is a million dollar compound', structure_new_lr['ID'])
    new_lr_name = copy_compound_to_live_report(selenium,
                                               structure_new_lr["ID"],
                                               report_name=duplicate_live_report,
                                               new_report=True)
    # Confirm compound was copied over, but not the rationale
    verify_grid_contents(selenium, {
        "Compound Structure": [structure_new_lr["smiles"]],
        "ID": [structure_new_lr["ID"]],
        "Rationale": [""]
    })

    # ----- STRUCTURE COPIED TO AN EXISTING LR -----#
    # switch to initial LR & un-check the previous structure row
    switch_to_live_report(selenium, duplicate_live_report)
    click_compound_row(selenium)
    copy_compound_to_live_report(selenium, structure_existing_lr["ID"], report_name=new_lr_name)
    verify_grid_contents(
        selenium, {
            "Compound Structure": [structure_existing_lr["smiles"], structure_new_lr["smiles"]],
            "ID": [structure_existing_lr["ID"], structure_new_lr["ID"]],
            "Rationale": ["", ""]
        })

    # ----- STRUCTURE APPEARS IN R-GROUP ENUMERATION SKETCHER -----#
    # Right click structure, hover over "Use in", and select "Enumeration" option
    use_compound_in_sketcher_and_verify(selenium, structure_existing_lr['ID'], enumeration_sketcher=True)
    # Validate expected compound appears in the sketcher
    verify_molv_from_maestro_equals(selenium, structure_existing_lr["molv"].split('\n')[5].split()[3:5],
                                    RGROUP_SCAFFOLD_IFRAME)
    close_enumeration_wizard(selenium)

    # lr teardown fails if not on duplicated lr created by the fixture, so deleting the extra lr created
    delete_open_live_report(selenium, new_lr_name)
