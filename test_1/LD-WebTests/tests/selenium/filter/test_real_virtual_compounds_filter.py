import pytest

from helpers.change import actions_pane, filter_actions, grid_column_menu
from helpers.flows import add_compound
from helpers.selection.filter_actions import COMPOUND_TYPE_CHECKBOX
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_column_contents, verify_footer_values
from library import dom, wait


@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures("use_module_isolated_project")
def test_real_virtual_compounds_filter(selenium):
    """
    Test REAL and VIRTUAL compound filters

    :param selenium: Webdriver
    :return:
    """

    # ----- Create and setup the LR ----- #
    search_keyword = "CHEMBL103, CHEMBL1030, CHEMBL105, CHEMBL1055, CRA-035507"
    actions_pane.open_add_compounds_panel(selenium)
    molv3 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 20 22 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C 2.810857 3.675143 0.000000 0\nM  V30 2 C 2.323143 2.332571 0.000000 0\nM  V30 3 C 3.730286 2.085714 0.000000 0\nM  V30 4 O 1.085429 3.045714 0.000000 0\nM  V30 5 C -0.151143 2.330571 0.000000 0\nM  V30 6 C -1.388857 3.044000 0.000000 0\nM  V30 7 C -2.625429 2.328571 0.000000 0\nM  V30 8 C -2.624286 0.900000 0.000000 0\nM  V30 9 C -1.386571 0.186857 0.000000 0\nM  V30 10 C -0.150000 0.902000 0.000000 0\nM  V30 11 C 1.087714 0.188571 0.000000 0\nM  V30 12 C 2.324286 0.904000 0.000000 0\nM  V30 13 O 3.562000 0.190571 0.000000 0\nM  V30 14 N 1.088857 -1.240000 0.000000 0\nM  V30 15 C 0.079429 -2.250857 0.000000 0\nM  V30 16 C 1.090571 -3.260286 0.000000 0\nM  V30 17 C 2.100000 -2.249429 0.000000 0\nM  V30 18 O 3.528571 -2.248286 0.000000 0\nM  V30 19 C -3.860857 0.184857 0.000000 0\nM  V30 20 N -5.097429 -0.530571 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 2 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 8 9\nM  V30 9 2 9 10\nM  V30 10 1 10 11\nM  V30 11 1 11 12\nM  V30 12 1 12 13\nM  V30 13 1 11 14\nM  V30 14 1 14 15\nM  V30 15 1 15 16\nM  V30 16 1 16 17\nM  V30 17 2 17 18\nM  V30 18 1 8 19\nM  V30 19 3 19 20\nM  V30 20 1 12 2\nM  V30 21 1 17 14\nM  V30 22 1 10 5\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    # Search Compounds by ID and add to LR
    add_compound.search_by_id(selenium, search_keyword)
    # Add compounds by MOLV
    add_compound.add_compound_by_molv_to_active_lr(selenium, molv3)

    # ----- Test the Filters ----- #
    # Open the Filter Panel and Clear filters if there were some leftover ones
    actions_pane.open_filter_panel(selenium)
    filter_actions.remove_all_filters(selenium)

    # ----- Filter ONLY REAL ----- #
    # Clicking on "VIRTUAL" to deselect it as it initially both "REAL" AND "VIRTUAL" are auto-selected.
    dom.click_element(selenium, COMPOUND_TYPE_CHECKBOX, text="VIRTUAL")
    wait.until_loading_mask_not_visible(selenium)
    grid_column_menu.sort_grid_by(selenium, 'ID')
    # Verify grid contents
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(6),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(4)
        })
    expected_real_id_content = ['CHEMBL103', 'CHEMBL105', 'CHEMBL1030', 'CHEMBL1055']
    verify_column_contents(selenium, 'ID', expected_real_id_content)

    # ----- Filter ONLY VIRTUAL ----- #
    dom.click_element(selenium, COMPOUND_TYPE_CHECKBOX, text="REAL")
    # Verify grid contents
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(6),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(2)
        })
    # Only verify the virtual that is part of starter data. One can't be certain about the ID generated for the
    # newly added compound, especially when running the whole test suite.
    verify_column_contents(selenium, 'ID', ['CRA-035507'], match_length_to_expected=True)
