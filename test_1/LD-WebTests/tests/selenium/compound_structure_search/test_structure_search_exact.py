import pytest
from helpers.change.actions_pane import open_add_compounds_panel
from helpers.flows.add_compound import add_compound_by_molv_to_active_lr
from helpers.selection.add_compound_panel import EXACT_TAB, COMPOUNDS_FOUND
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_column_contents
from library import dom


@pytest.mark.k8s_defect(reason="SS-42730: lingering failure when re-enabling require_webgl tests on new jenkins")
@pytest.mark.smoke
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_structure_search_exact(selenium):
    """
    Adds 2 compounds (one that exists and one that is chemically invalid) to the LR using Exact Compound Search.

    :param selenium: Selenium Webdriver
    """
    structure_1 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 35 39 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 F 4.173714 -2.022000 0.000000 0\nM  V30 2 C 5.410000 -2.737429 0.000000 0\nM  V30 3 C 6.648000 -2.024286 0.000000 0\nM  V30 4 C 7.884571 -2.739428 0.000000 0\nM  V30 5 N 9.122286 -2.026000 0.000000 0\nM  V30 6 C 9.123429 -0.597429 0.000000 0\nM  V30 7 O 7.886857 0.117714 0.000000 0\nM  V30 8 C 10.361143 0.115714 0.000000 0\nM  V30 9 S 10.362286 1.544286 0.000000 0\nM  V30 10 O 11.790857 1.543143 0.000000 0\nM  V30 11 O 8.933714 1.545429 0.000000 0\nM  V30 12 C 10.363429 2.972857 0.000000 0\nM  V30 13 C 9.126857 3.688286 0.000000 0\nM  V30 14 C 7.889143 2.975143 0.000000 0\nM  V30 15 C 6.652286 3.690286 0.000000 0\nM  V30 16 C 6.653428 5.118857 0.000000 0\nM  V30 17 C 7.891143 5.832000 0.000000 0\nM  V30 18 C 9.128000 5.116857 0.000000 0\nM  V30 19 C 7.883429 -4.168000 0.000000 0\nM  V30 20 C 6.645714 -4.881143 0.000000 0\nM  V30 21 C 5.408857 -4.166000 0.000000 0\nM  V30 22 O 4.171429 -4.879143 0.000000 0\nM  V30 23 C 4.170286 -6.308000 0.000000 0\nM  V30 24 C 2.932571 -7.021143 0.000000 0\nM  V30 25 C 1.696000 -6.306000 0.000000 0\nM  V30 26 C 0.458286 -7.019143 0.000000 0\nM  V30 27 O -0.900286 -6.576571 0.000000 0\nM  V30 28 C -1.740286 -7.731714 0.000000 0\nM  V30 29 O -0.902000 -8.888286 0.000000 0\nM  V30 30 C 0.457143 -8.447715 0.000000 0\nM  V30 31 C 1.693714 -9.162857 0.000000 0\nM  V30 32 C 2.931429 -8.449714 0.000000 0\nM  V30 33 N 4.168000 -9.164857 0.000000 0\nM  V30 34 C 5.405714 -8.451714 0.000000 0\nM  V30 35 C 5.406857 -7.023143 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 1 4 5\nM  V30 5 1 5 6\nM  V30 6 2 6 7\nM  V30 7 1 6 8\nM  V30 8 1 8 9\nM  V30 9 2 9 10\nM  V30 10 2 9 11\nM  V30 11 1 9 12\nM  V30 12 1 12 13\nM  V30 13 2 13 14\nM  V30 14 1 14 15\nM  V30 15 2 15 16\nM  V30 16 1 16 17\nM  V30 17 2 17 18\nM  V30 18 2 4 19\nM  V30 19 1 19 20\nM  V30 20 2 20 21\nM  V30 21 1 21 22\nM  V30 22 1 22 23\nM  V30 23 1 23 24\nM  V30 24 2 24 25\nM  V30 25 1 25 26\nM  V30 26 1 26 27\nM  V30 27 1 27 28\nM  V30 28 1 28 29\nM  V30 29 1 29 30\nM  V30 30 1 30 31\nM  V30 31 2 31 32\nM  V30 32 1 32 33\nM  V30 33 2 33 34\nM  V30 34 1 34 35\nM  V30 35 1 21 2\nM  V30 36 2 35 23\nM  V30 37 1 18 13\nM  V30 38 1 32 24\nM  V30 39 2 30 26\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    structure_2 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 24 25 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -0.900286 -1.107143 0.000000 0\nM  V30 2 O 0.336286 -0.392000 0.000000 0\nM  V30 3 C 1.574000 -1.105143 0.000000 0\nM  V30 4 C 2.810572 -0.390000 0.000000 0\nM  V30 5 C 4.048571 -1.103143 0.000000 0\nM  V30 6 C 5.284857 -0.388000 0.000000 0\nM  V30 7 O 6.522571 -1.101143 0.000000 0\nM  V30 8 O 5.283714 1.040571 0.000000 0\nM  V30 9 C 4.049714 -2.531714 0.000000 0\nM  V30 10 C 2.812857 -3.246857 0.000000 0\nM  V30 11 C 1.575143 -2.533714 0.000000 0\nM  V30 12 C 0.338571 -3.248857 0.000000 0\nM  V30 13 O 0.339714 -4.677429 0.000000 0\nM  V30 14 N -0.899143 -2.535714 0.000000 0\nM  V30 15 C -2.135429 -3.250857 0.000000 0\nM  V30 16 C -3.373429 -2.537714 0.000000 0\nM  V30 17 C -4.610000 -3.252857 0.000000 0\nM  V30 18 C -4.608857 -4.681429 0.000000 0\nM  V30 19 C -3.371143 -5.394571 0.000000 0\nM  V30 20 C -2.134571 -4.679714 0.000000 0\nM  V30 21 O 5.287143 -3.245143 0.000000 0\nM  V30 22 C 4.574000 -4.482857 0.000000 0\nM  V30 23 C 6.002571 -4.481714 0.000000 0\nM  V30 24 C 6.523714 -2.529714 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 1 5 6\nM  V30 6 1 6 7\nM  V30 7 2 6 8\nM  V30 8 2 5 9\nM  V30 9 1 9 10\nM  V30 10 2 10 11\nM  V30 11 1 11 12\nM  V30 12 2 12 13\nM  V30 13 1 12 14\nM  V30 14 1 14 15\nM  V30 15 2 15 16\nM  V30 16 1 16 17\nM  V30 17 2 17 18\nM  V30 18 1 18 19\nM  V30 19 2 19 20\nM  V30 20 1 9 21\nM  V30 21 1 21 22\nM  V30 22 1 21 23\nM  V30 23 1 21 24\nM  V30 24 1 11 3\nM  V30 25 1 20 15\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'

    # ----- ADD COMPOUNDS ----- #
    # Opening the Compounds Panel
    open_add_compounds_panel(selenium)
    # Exact searching for a compound that already exists
    add_compound_by_molv_to_active_lr(selenium, structure_1, EXACT_TAB)
    # Verify that 1 compound was found
    assert dom.get_element(selenium, COMPOUNDS_FOUND, text='1 compounds found', timeout=3, dont_raise=True), \
        'Can not verify 1 compound found.'
    # Exact searching for a chemically invalid compound
    add_compound_by_molv_to_active_lr(selenium, structure_2, EXACT_TAB)
    # Verify that 0 compounds were found
    assert dom.get_element(selenium, COMPOUNDS_FOUND, text='0 compounds found', timeout=3, dont_raise=True), \
        'Can not verify 0 compounds found.'

    # ----- VERIFY LR CONTENT ----- #
    # Verifying a compound is added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(1)})
    verify_column_contents(selenium, column_name='ID', expected_content=['CRA-033369'])
