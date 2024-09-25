"""
Testing adding of Row per Experiment (RPE) columns, expanding of RPE columns,
verifying of RPE elements while the LR is in RPE mode, switch to compound mode,
verify LR contents in Compound mode.
"""
import pytest
from helpers.change.actions_pane import open_add_compounds_panel, open_add_data_panel, close_add_data_panel,\
    toggle_lr_mode, click_expand_row
from helpers.change.columns_action import add_column_by_name
from helpers.change.grid_column_menu import sort_grid_by
from helpers.flows.add_compound import search_by_id
from helpers.verification.grid import verify_grid_contents


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rpe_basic(selenium):
    """
    Populate a new LR with 3 structures and RPE columns from 2 different experiments. The first
    structure will have values in both experiments. The second and third structure added will not
    have values for the same experiment.

    Verify:
    - Switching to RPE mode is possible and verify grid content.
    - that columns from different experiments do not expand together.
    - LiveReport is able to return to Row per Compound mode (from Row per Experiment) & LR
      contents are correct.
    """

    # Add compounds to the LR with search by ID
    open_add_compounds_panel(selenium)
    search_by_id(selenium, 'CRA-031137, CRA-033619, V055685')

    # Add RPE columns to the LR
    pk_po_rat_rpe = 'PK_PO_RAT (AUC)'
    pk_iv_rat_rpe = 'PK_IV_RAT (AnalysisComment)'
    open_add_data_panel(selenium)
    add_column_by_name(selenium, pk_po_rat_rpe)
    add_column_by_name(selenium, pk_iv_rat_rpe)
    close_add_data_panel(selenium)

    # Sort compounds by ID
    sort_grid_by(selenium, 'ID')

    # ----- Expand PK_PO_RAT (AUC) and check grid content ----- #
    click_expand_row(selenium, pk_po_rat_rpe)

    # verify grid values
    verify_grid_contents(
        selenium, {
            'ID': [
                'CRA-031137-1', 'CRA-031137-Alpha Numeric', 'CRA-033619-1', 'CRA-033619-V-22173', 'V055685-V',
                'V055685-V-0', 'V055685-V-1', 'V055685-V-2'
            ],
            pk_po_rat_rpe: ['', '', '', '6.1', '', '0.1', '0.2', '0.3'],
            pk_iv_rat_rpe: [
                'PK analysis (WinNonlin Pro) two-compartment model with 1/y^ weighting',
                'PK analysis (WinNonlin Pro) two-compartment model with 1/y^ weighting',
                'WinNonlin Pro two-compartment model with 1/y^ and 1/y^2 weighting',
                'WinNonlin Pro two-compartment model with 1/y^ and 1/y^2 weighting', '', '', '', ''
            ]
        })

    # ----- Expand PK_IV_RAT (AnalysisComment) and check grid content ----- #
    click_expand_row(selenium, pk_iv_rat_rpe)

    # verify grid values
    verify_grid_contents(
        selenium, {
            'ID': [
                'CRA-031137-1', 'CRA-031137-Alpha Numeric', 'CRA-031137-V-17656', 'CRA-033619-1', 'CRA-033619-V-22165',
                'V055685-V'
            ],
            pk_po_rat_rpe: ['', '', '', '6.1', '6.1', '0.3\n0.2\n0.1'],
            pk_iv_rat_rpe: [
                '', '', 'PK analysis (WinNonlin Pro) two-compartment model with 1/y^ weighting', '',
                'WinNonlin Pro two-compartment model with 1/y^ and 1/y^2 weighting', ''
            ]
        })

    # Toggle LiveReport back to Row per Compound
    toggle_lr_mode(selenium)

    # Verify LR contents are correct in Row per Compound mode
    verify_grid_contents(
        selenium, {
            'ID': ['CRA-031137', 'CRA-033619', 'V055685'],
            pk_po_rat_rpe: ['', '6.1', '0.3\n0.2\n0.1'],
            pk_iv_rat_rpe: [
                'PK analysis (WinNonlin Pro) two-compartment model with 1/y^ weighting',
                'WinNonlin Pro two-compartment model with 1/y^ and 1/y^2 weighting', ''
            ]
        })
