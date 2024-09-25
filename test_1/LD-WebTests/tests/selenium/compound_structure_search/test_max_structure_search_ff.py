import pytest
from helpers.change.actions_pane import open_add_compounds_panel
from helpers.flows.add_compound import add_compound_by_molv_to_active_lr, max_results_on_search
from helpers.selection.add_compound_panel import COMPOUNDS_FOUND, SUBSTRUCTURE_TAB, COMPOUND_SEARCH_SUB_TAB, \
    SEARCH_AND_ADD_COMPOUNDS_BUTTON, MAX_RESULTS_DIALOG, MAX_RESULTS_INPUT, GEAR_BUTTON_DOWN, GEAR_BUTTON_UP
from helpers.selection.grid import Footer
from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_DIALOG_BODY
from helpers.verification.grid import verify_footer_values, verify_is_visible, check_for_butterbar

from library import dom, base

LD_PROPERTIES = {'STRUCTURE_SEARCH_MAX_COMPOUNDS': 3}


@pytest.mark.k8s_defect(reason="SS-42730: lingering failure when re-enabling require_webgl tests on new jenkins")
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures("customized_server_config")
def test_max_structure_search_ff(selenium):
    """
    Test the STRUCTURE_SEARCH_MAX_COMPOUNDS Feature flag.
    a. Set the default value of the FF to 3.
    b. Run a substructure search which returns more than 3 comps, and ensure only 3 are returned.
    c. Run a exact search which returns 1 comp, and ensure only 1 is returned.
    d. Run a similarity search which returns more than 3 comps, and ensure only 3 are returned.
    e. Negative validation of a search greater than 3.
    """
    molv3 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 19 20 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -1.229143 0.470000 0.000000 0\nM  V30 2 N -1.003143 -0.942000 0.000000 0\nM  V30 3 C -2.012000 -1.952286 0.000000 0\nM  V30 4 C -3.422571 -1.732571 0.000000 0\nM  V30 5 C -4.320000 -2.843714 0.000000 0\nM  V30 6 O -5.731429 -2.622000 0.000000 0\nM  V30 7 O -3.806286 -4.176571 0.000000 0\nM  V30 8 C -1.360857 -3.225143 0.000000 0\nM  V30 9 C 0.048857 -2.998000 0.000000 0\nM  V30 10 C 0.271429 -1.586857 0.000000 0\nM  V30 11 C 1.542286 -0.936857 0.000000 0\nM  V30 12 O 1.614857 0.490000 0.000000 0\nM  V30 13 C 2.741428 -1.711429 0.000000 0\nM  V30 14 C 2.668857 -3.141714 0.000000 0\nM  V30 15 C 3.868857 -3.914857 0.000000 0\nM  V30 16 C 5.141143 -3.267429 0.000000 0\nM  V30 17 C 6.340000 -4.042286 0.000000 0\nM  V30 18 C 5.214000 -1.837143 0.000000 0\nM  V30 19 C 4.013714 -1.064000 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 3 4\nM  V30 4 1 4 5\nM  V30 5 1 5 6\nM  V30 6 2 5 7\nM  V30 7 2 3 8\nM  V30 8 1 8 9\nM  V30 9 2 9 10\nM  V30 10 1 10 11\nM  V30 11 2 11 12\nM  V30 12 1 11 13\nM  V30 13 2 13 14\nM  V30 14 1 14 15\nM  V30 15 2 15 16\nM  V30 16 1 16 17\nM  V30 17 1 16 18\nM  V30 18 2 18 19\nM  V30 19 1 10 2\nM  V30 20 1 19 13\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'

    # Opening the Compounds Panel
    open_add_compounds_panel(selenium)

    # ---------- Adding compounds by Substructure Search --------- #
    add_compound_by_molv_to_active_lr(selenium, molv3, mode=SUBSTRUCTURE_TAB)

    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)

    # Verify that 3 compounds were found
    verify_is_visible(selenium, COMPOUNDS_FOUND, selector_text='3 compounds found')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5)
        })

    # --------- Adding compounds by Exact Search --------- #
    dom.click_element(selenium, COMPOUND_SEARCH_SUB_TAB, text='Exact Match', exact_text_match=True)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)

    verify_is_visible(selenium, COMPOUNDS_FOUND, selector_text='1 compounds found')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5)
        })

    # -------- Adding compounds by Similarity Search ------- #
    dom.click_element(selenium, COMPOUND_SEARCH_SUB_TAB, text='Similarity', exact_text_match=True)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)

    verify_is_visible(selenium, COMPOUNDS_FOUND, selector_text='3 compounds found')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(7),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })

    # Negative validation checking that with Max Results set to 10, an error is thrown
    max_results_on_search(selenium, max_result=10, scroll_required=True)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    verify_is_visible(selenium, MODAL_DIALOG_HEADER, selector_text='Error')
    verify_is_visible(selenium,
                      MODAL_DIALOG_BODY,
                      selector_text='There was an error adding the compound: '
                      'Please specify a valid "Max Results" value between 1 and 3')
    base.click_ok(selenium)
