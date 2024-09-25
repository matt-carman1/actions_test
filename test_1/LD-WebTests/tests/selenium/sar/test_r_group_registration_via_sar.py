"""
Test registration of R-groups from SAR scaffold
"""

import pytest
from helpers.change.sar_action import create_sar_scaffold
from helpers.change.actions_pane import open_add_compounds_panel
from helpers.change.sar_action import save_all_r_groups
from helpers.change.grid_column_menu import sort_grid_by
from helpers.flows.add_compound import search_by_id
from helpers.verification.grid import check_for_butterbar
from helpers.selection.grid import GRID_NOTIFICATION_LINK, Footer
from helpers.verification.grid import verify_footer_values, verify_grid_contents
from library import dom, wait


@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures("use_module_isolated_project")
def test_r_group_registration_via_sar(selenium):
    """
    This test performs the following steps:

    a. Creates an initial SAR scaffold on a duplicated LR.
    b. Select a compound and Save as R-group from the R1 dropdown.
    c. Selects two compound and Save as R-group from the R2 dropdown.
    d. Selects three compounds and Save as R-groups from the R3 dropdown.
    e. Verifies if all the R-groups are added and de-duplicated.
    :param selenium: Webdriver
    """

    r_group_smiles = [
        "CN1CCN(CC1)C1=C(NC2=CC=C(O)C(F)=C2)C(=O)C1=O", "CO", "O", "OC1=CC=C(NC(=O)C2(CC2)C(=O)NC2=CC=C(F)C=C2)C=C1F",
        "OC1=CC=C(NC2=C(NC3=CC=C(F)C=C3)C(=O)C2=O)C=C1F"
    ]

    # ----- Create a Scaffold ----- #
    sar_scaffold = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 13 14 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 R# -2.302857 -1.170000 0.000000 101 VAL=1 RGROUPS=(1 1)\nM  V30 2 C -1.065143 -0.456571 0.000000 0\nM  V30 3 C -1.064000 0.972000 0.000000 0\nM  V30 4 R# -2.300571 1.687143 0.000000 102 VAL=1 RGROUPS=(1 2)\nM  V30 5 C 0.173714 1.685143 0.000000 0\nM  V30 6 C 1.410286 0.970000 0.000000 0\nM  V30 7 C 2.648000 1.683143 0.000000 0\nM  V30 8 R# 2.649143 3.111714 0.000000 103 VAL=1 RGROUPS=(1 3)\nM  V30 9 C 3.884572 0.968000 0.000000 0\nM  V30 10 C 3.883429 -0.460571 0.000000 0\nM  V30 11 N 2.645714 -1.174000 0.000000 0\nM  V30 12 C 1.409143 -0.458571 0.000000 0\nM  V30 13 C 0.171429 -1.172000 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 1 3 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 1 7 8\nM  V30 8 2 7 9\nM  V30 9 1 9 10\nM  V30 10 2 10 11\nM  V30 11 1 11 12\nM  V30 12 2 12 13\nM  V30 13 1 13 2\nM  V30 14 1 12 6\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'

    # Open the Compounds Panel and add compound to LR via search by ID
    open_add_compounds_panel(selenium)
    search_by_id(selenium, 'CRA-032662, CRA-032664, CRA-032703, CRA-032913')

    create_sar_scaffold(selenium, sar_scaffold)

    # Verify number of columns in the LR
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(10),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    butterbar_notification_text = 'R-Groups have been saved.\nGo to the new LiveReport.'

    # Saving R-groups from R1 scaffold into a new LiveReport and checking for the butterbar message.
    new_r_group_lr = save_all_r_groups(selenium,
                                       "R1 (SAR)",
                                       lr_name="R_group_registration",
                                       new_lr=True,
                                       list_of_entity_ids=["CRA-032703"])
    check_for_butterbar(selenium, notification_text=butterbar_notification_text, visible=True)
    check_for_butterbar(selenium, notification_text=butterbar_notification_text, visible=False)

    # Saving R-groups from R2 scaffold and into the old LiveReport and checking for the butterbar message.
    save_all_r_groups(selenium, "R2 (SAR)", new_r_group_lr, list_of_entity_ids=["CRA-032662"])
    check_for_butterbar(selenium, notification_text=butterbar_notification_text, visible=True)
    check_for_butterbar(selenium, notification_text=butterbar_notification_text, visible=False)

    # Saving R-groups from the R3 scaffold into the old LiveReport and checking for the butterbar message.
    save_all_r_groups(selenium, "R3 (SAR)", new_r_group_lr, list_of_entity_ids=["CRA-032913"])
    check_for_butterbar(selenium, notification_text=butterbar_notification_text, visible=True)

    # From SS-30284 onwards, there is a new link to open Livereport from the notification bar.
    dom.click_element(selenium, GRID_NOTIFICATION_LINK, text="Go to the new LiveReport.")
    wait.until_loading_mask_not_visible(selenium)

    # Verify number of columns in the LR
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5)
        })
    sort_grid_by(selenium, column_name="Compound Structure")
    verify_grid_contents(selenium, {'Compound Structure': r_group_smiles})
