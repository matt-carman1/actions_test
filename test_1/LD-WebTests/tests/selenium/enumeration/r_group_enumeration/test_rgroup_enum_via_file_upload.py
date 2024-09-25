"""
Selenium test for R-group Enumeration via file upload
"""

import pytest

from helpers.change.enumeration import open_enumeration_wizard, close_enumeration_wizard, add_structures_via_file_upload
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report
from helpers.verification.element import verify_is_visible
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_STRUCTURE_COUNT,\
    ENUMERATION_STATUS, ENUMERATION_SCAFFOLD_SKETCHER

from library import dom, wait


@pytest.mark.flaky(reason="SS-31957")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rgroup_enum_via_file_upload(selenium):
    """
    R-group enumeration test via file upload:
    1. Enumerate a R-group reaction with R1 and R2 groups via file upload.
    2. Validated the number of products and columns in the LiveReport.

    :param selenium: Selenium Webdriver
    """
    scaffold = '[*]C1CCCC([*])C1 |$_R1;;;;;;_R2;$|'
    open_enumeration_wizard(selenium, enumeration_type='R-Group')

    # Sketching a scaffold in the sketcher
    import_structure_into_sketcher(selenium,
                                   smiles_or_mrv=scaffold,
                                   sketcher_iframe_selector=ENUMERATION_SCAFFOLD_SKETCHER)
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON)

    # Adding r-groups via file upload
    add_structures_via_file_upload(selenium, "aliphatic_monocyclic_rings.sdf", structure='R1')
    add_structures_via_file_upload(selenium, "aromatic_monocyclic_rings.sdf", structure='R2')

    # Verifying that the r-groups are populated
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(4 structures",
                      exact_selector_text_match=True,
                      custom_timeout=2)
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(5 structures",
                      exact_selector_text_match=True,
                      custom_timeout=2)

    # Verify the number of expected products
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(20 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    close_enumeration_wizard(selenium)

    # Validate the number of products and columns in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(20),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Highlighted Substructure'
    ]

    # Verifies that all the expected columns are visible in the LR
    verify_visible_columns_in_live_report(selenium, expected_column_list)
