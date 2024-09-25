import pytest

from helpers.change.enumeration import open_enumeration_wizard, add_structures_from_live_report, \
    close_enumeration_wizard
from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report, \
    verify_column_contents
from helpers.verification.element import verify_is_visible
from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_STATUS, \
    ENUMERATION_STRUCTURE_COUNT, ENUMERATION_SCAFFOLD_SKETCHER
from library import dom, wait

LD_PROPERTIES = {'SPECIFY_COMPOUND_MATCHING_TYPE_SS_34107': 'true'}


@pytest.mark.usefixtures('customized_server_config')
@pytest.mark.require_webgl
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rgroup_enum_via_livereports(selenium):
    """
    Basic R-group enumeration test via livereports:
    1. Enumerate R-groups from LiveReports for a generic scaffold.
    2. Validated the number of products and columns in the LiveReport.

    :param selenium: Selenium Webdriver
    """

    scaffold = '\n  Mrv1908 01112218092D          \n\n  0  0  0     0  0            999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 7 7 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 R# 0 2.31 0 0 RGROUPS=(1 1)\nM  V30 2 C -0 0.77 0 0\nM  V30 3 C 1.3337 -0 0 0\nM  V30 4 C 1.3337 -1.54 0 0\nM  V30 5 C -0 -2.31 0 0\nM  V30 6 C -1.3337 -1.54 0 0\nM  V30 7 C -1.3337 0 0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 3 4\nM  V30 4 1 4 5\nM  V30 5 1 5 6\nM  V30 6 1 6 7\nM  V30 7 1 2 7\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    smiles_list = [
        'c1nc(CN2NCC(=C3CC3)CC2C2CCCCC2)no1', 'c1ccc(C2CCCCC2)nc1', 'C=C1CC(C2CCCCC2)CN(Cc2nnc3n2CCN3)C1',
        'NCC1(CC(=O)O)CCCC(C2CCCCC2)N1', 'O=C(O)C1Nc2ccccc2C(C2CCCCC2)N1'
    ]
    open_enumeration_wizard(selenium, enumeration_type='R-Group')

    # Sketching a scaffold in the sketcher
    import_structure_into_sketcher(selenium,
                                   molv3_or_smiles=scaffold,
                                   sketcher_iframe_selector=ENUMERATION_SCAFFOLD_SKETCHER)
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON)

    # Add reactants from LiveReports and verify that number of reactants
    add_structures_from_live_report(selenium, live_report_name='5 Fragments 4 Assays', structure_name='R1')

    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(5 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Verify the number of expected products
    # NOTE(Nitin) : Increased the timeout to 15 seconds from 10 seconds to avoid flakiness. It has been observed that
    # the test sometimes fails because the structures are not populated quickly sometimes. Another alternative is to
    # wait for .preview-pending-spinner
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(5 structures",
                      exact_selector_text_match=True,
                      custom_timeout=15)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    close_enumeration_wizard(selenium)

    # Validate the number of products and columns in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Highlighted Substructure'
    ]

    verify_visible_columns_in_live_report(selenium, expected_column_list)

    # Verify compound SMILES
    sort_grid_by(selenium, 'Compound Structure')
    verify_column_contents(selenium, 'Compound Structure', smiles_list, exact_match=False)
