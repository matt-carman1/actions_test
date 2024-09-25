import pytest

from helpers.change.actions_pane import open_add_compounds_panel
from helpers.extraction.grid import wait_until_cells_are_loaded
from helpers.flows.add_compound import add_compound_by_molv_to_active_lr
from helpers.selection.add_compound_panel import SIMILARITY_TAB, COMPOUNDS_FOUND
from helpers.selection.grid import GRID_HEADER_TOP, GRID_PENDING_CELLS
from helpers.verification.grid import verify_footer_values, verify_grid_contents, \
    check_for_butterbar
from library import dom, utils
from library.wait import until_not_visible


def get_similarity_score_column_name(driver):
    """
    Gets the similarity score column name. We don't want to hardcode this because it
    contains a SMILES string.
    :param driver: Selenium Webdriver
    """

    lr_column_names = dom.get_element(driver, GRID_HEADER_TOP).text
    observed_lr_column_names = lr_column_names.split("\n")

    for column_name in observed_lr_column_names:
        if column_name.startswith('Similarity Score'):
            return column_name
    raise dom.LiveDesignWebException("Missing similarity score column. Got following "
                                     "{} columns".format(observed_lr_column_names))


@pytest.mark.smoke
@pytest.mark.require_webgl
@pytest.mark.xfail(utils.is_k8s(), reason="SS-42730: Unknown failure reason on New Jenkins")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_structure_search_similarity(selenium):
    """
    Adds a compound to the LR using Similarity Compound Search and verifies Similarity Score column is added.

    :param selenium: Selenium Webdriver
    """
    molv3 = "Test\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 32 36 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -3.585412 4.037258 0.000000 0\nM  V30 2 C -2.719812 3.536457 0.000000 0\nM  V30 3 C -1.853212 4.035656 0.000000 0\nM  V30 4 N -2.720614 2.536457 0.000000 0\nM  V30 5 C -1.855414 2.036856 0.000000 0\nM  V30 6 C -0.988414 2.533855 0.000000 0\nM  V30 7 C -0.122414 2.035454 0.000000 0\nM  V30 8 C -0.123216 1.032854 0.000000 0\nM  V30 9 C 0.741984 0.533253 0.000000 0\nM  V30 10 O 1.608384 1.032452 0.000000 0\nM  V30 11 C -0.990216 0.535855 0.000000 0\nM  V30 12 N -1.856216 1.034456 0.000000 0\nM  V30 13 C -0.992018 -0.465345 0.000000 0\nM  V30 14 C -1.857018 -0.966344 0.000000 0\nM  V30 15 C -1.859019 -1.966144 0.000000 0\nM  V30 16 C -0.990820 -2.465145 0.000000 0\nM  V30 17 C -0.126619 -1.966546 0.000000 0\nM  V30 18 C 0.825380 -2.275547 0.000000 0\nM  V30 19 C 1.412981 -1.467548 0.000000 0\nM  V30 20 C 0.826182 -0.657547 0.000000 0\nM  V30 21 C -0.124818 -0.966946 0.000000 0\nM  V30 22 C 1.132579 -3.226747 0.000000 0\nM  V30 23 C 0.544578 -4.035347 0.000000 0\nM  V30 24 C 1.130977 -4.844748 0.000000 0\nM  V30 25 C 2.082377 -4.535748 0.000000 0\nM  V30 26 C 2.083379 -3.537348 0.000000 0\nM  V30 27 C 2.893379 -2.949150 0.000000 0\nM  V30 28 C 2.788581 -1.954949 0.000000 0\nM  V30 29 C 3.598981 -1.368750 0.000000 0\nM  V30 30 C 4.512981 -1.774752 0.000000 0\nM  V30 31 C 4.615580 -2.769152 0.000000 0\nM  V30 32 C 3.806379 -3.357351 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 2 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 8 9\nM  V30 9 2 9 10\nM  V30 10 1 8 11\nM  V30 11 2 11 12\nM  V30 12 1 11 13\nM  V30 13 2 13 14\nM  V30 14 1 14 15\nM  V30 15 2 15 16\nM  V30 16 1 16 17\nM  V30 17 1 17 18\nM  V30 18 1 18 19\nM  V30 19 1 19 20\nM  V30 20 1 20 21\nM  V30 21 1 18 22\nM  V30 22 1 22 23\nM  V30 23 1 23 24\nM  V30 24 1 24 25\nM  V30 25 1 25 26\nM  V30 26 1 26 27\nM  V30 27 1 27 28\nM  V30 28 1 28 29\nM  V30 29 1 29 30\nM  V30 30 1 30 31\nM  V30 31 1 31 32\nM  V30 32 1 12 5\nM  V30 33 1 21 13\nM  V30 34 1 26 22\nM  V30 35 1 32 27\nM  V30 36 2 21 17\nM  V30 END BOND\nM  V30 END CTAB\nM  END"

    # ----- ADD COMPOUNDS ----- #
    # Opening the Compounds Panel and add compound to LR via Similarity Search
    open_add_compounds_panel(selenium)

    add_compound_by_molv_to_active_lr(selenium, molv3, SIMILARITY_TAB)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)
    assert \
        dom.get_element(selenium, COMPOUNDS_FOUND, text='3 compounds found', timeout=3,
                        dont_raise=True, must_be_visible=False), \
        'Can not verify 3 compounds found.'

    # ----- VERIFY LR CONTENT ----- #
    verify_footer_values(selenium, {'row_all_count': '3 Total Compounds'})
    # breakpoint()
    similarity_score_column_name = get_similarity_score_column_name(selenium)
    wait_until_cells_are_loaded(selenium, similarity_score_column_name, custom_timeout=10)
    verify_grid_contents(selenium, {
        'ID': ['CMPD-1', 'CMPD-2', 'V055846'],
        similarity_score_column_name: ['1', '0.839', '0.77']
    },
                         inexact_match_columns=['ID', similarity_score_column_name])
