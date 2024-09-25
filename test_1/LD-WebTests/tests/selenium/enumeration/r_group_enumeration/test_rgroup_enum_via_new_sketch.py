"""
Selenium test for testing basic R-group enumeration workflow
"""

import pytest

from helpers.change.enumeration import open_enumeration_wizard, close_enumeration_wizard, add_structures_via_sketcher
from helpers.change.grid_column_menu import sort_grid_by
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report, \
    verify_column_contents
from helpers.verification.element import verify_is_visible
from helpers.selection.enumeration import ENUMERATION_SCAFFOLD_SKETCHER, ENUMERATION_PROCEED_BUTTON, \
    ENUMERATION_STRUCTURE_COUNT, ENUMERATION_STATUS
from helpers.change.sketcher import import_structure_into_sketcher
from library import dom, wait
from library.utils import is_k8s


@pytest.mark.k8s_defect(reason="SS-42730: lingering failure when re-enabling require_webgl tests on new jenkins")
@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rgroup_enum_via_new_sketch(selenium):
    """
    Basic R-group enumeration test:
    1. Enumerate products for a basic Scaffold with R1, R2 groups and two R-group structures each.
    2. Validated the number of products and columns in the LiveReport.

    :param selenium: Selenium Webdriver
    """
    scaffold = '\n  Mrv1908 01112222592D          \n\n  0  0  0     0  0            999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 7 7 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 R# 0.2147 2.5779 0 0 RGROUPS=(1 1)\nM  V30 2 C 0.2147 1.0379 0 0\nM  V30 3 C 1.4605 0.1327 0 0\nM  V30 4 C 0.9847 -1.332 0 0\nM  V30 5 C -0.5553 -1.332 0 0\nM  V30 6 R# -1.4605 -2.5779 0 0 RGROUPS=(1 2)\nM  V30 7 C -1.0312 0.1327 0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 3 4\nM  V30 4 1 4 5\nM  V30 5 1 5 6\nM  V30 6 1 5 7\nM  V30 7 1 2 7\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    list_of_rgroups = [
        '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 2 1 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 C -0.500000 0.000000 0.000000 0\nM  V30 2 C 0.500000 0.000000 0.000000 0 ATTCHPT=1\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n>  <_CXSMILES_Data>  \n|$;;_AP1$|\n\n$$$$\n',
        '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 1 0 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 Cl 0.000000 0.000000 0.000000 0 ATTCHPT=1\nM  V30 END ATOM\nM  V30 END CTAB\nM  END\n>  <_CXSMILES_Data>  \n|$;_AP1$,lp:0:3|\n\n$$$$\n'
    ]
    smiles_list = ['CCC1CCC(CC)C1', 'CCC1CCC(Cl)C1', 'ClC1CCC(Cl)C1']

    # Opening the R-group Enumeration panel
    open_enumeration_wizard(selenium, enumeration_type='R-Group')

    # Sketching a scaffold in the sketcher
    import_structure_into_sketcher(selenium,
                                   molv3_or_smiles=scaffold,
                                   sketcher_iframe_selector=ENUMERATION_SCAFFOLD_SKETCHER)
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON)

    # Bringing the R-groups via New Sketch
    add_structures_via_sketcher(selenium, list_of_rgroups, structure_tag='R1')
    add_structures_via_sketcher(selenium, list_of_rgroups, structure_tag='R2', explicitly_open_sketcher=True)

    # Verification that all three R-groups are being brought
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Verify the expected products
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(3 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    close_enumeration_wizard(selenium)

    # Validate the number of products and columns in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Highlighted Substructure'
    ]

    verify_visible_columns_in_live_report(selenium, expected_column_list)

    # Verify Compound SMILES
    sort_grid_by(selenium, 'Compound Structure')
    verify_column_contents(selenium, 'Compound Structure', smiles_list)
