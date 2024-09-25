import pytest
from helpers.change.actions_pane import open_add_compounds_panel, close_add_compounds_panel
from helpers.flows.add_compound import add_compound_by_molv_to_active_lr
from helpers.verification.grid import verify_grid_contents


@pytest.mark.smoke
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures("use_module_isolated_project")
def test_sketch_compound(selenium):
    """
    Adds a compound idea to the LR using the Add Idea button & checks to see if it appears in the LR.

    :param selenium: Selenium Webdriver
    """

    molv3 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 9 9 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 Cl -1.400857 2.732571 0.000000 0\nM  V30 2 C -0.162286 2.020857 0.000000 0\nM  V30 3 C 1.073429 2.737714 0.000000 0\nM  V30 4 C -0.159429 0.592286 0.000000 0\nM  V30 5 C 1.079143 -0.119429 0.000000 0\nM  V30 6 C 1.082000 -1.548000 0.000000 0\nM  V30 7 C -0.153714 -2.264571 0.000000 0\nM  V30 8 C -1.392286 -1.552857 0.000000 0\nM  V30 9 C -1.395143 -0.124286 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 2 4\nM  V30 4 2 4 5\nM  V30 5 1 5 6\nM  V30 6 2 6 7\nM  V30 7 1 7 8\nM  V30 8 2 8 9\nM  V30 9 1 9 4\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'

    # ----- ADD FIRST COMPOUND ----- #
    # Opening the Compounds Panel & add a compound
    open_add_compounds_panel(selenium)
    add_compound_by_molv_to_active_lr(selenium, molv3)
    close_add_compounds_panel(selenium)

    # ----- VERIFY LR CONTENTS ----- #
    verify_grid_contents(selenium, {'Compound Structure': [molv3]})
