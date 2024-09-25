"""
Selenium test for testing basic R-group enumeration workflow
"""

import pytest

from helpers.flows.sketcher import use_compound_in_sketcher_and_verify
from helpers.verification.sketcher import verify_if_enumeration_is_populated
from resources.structures.structures_test_rgroup_enum_import_scaffolds import \
    RGROUP_SCAFFOLD_FOR_V035624, RGROUP_SCAFFOLD_FOR_V035626
from helpers.change.enumeration import open_enumeration_wizard, close_enumeration_wizard
from helpers.selection.enumeration import NEW_ENUMERATION_WIZARD_WINDOW, ENUMERATION_HEADER, RGROUP_ENUM_ACTIVE_LR_RADIO, \
    RGROUP_ENUM_ACTIVE_LR_DROPDOWN, RGROUP_ENUM_ACTIVE_LR_COMPOUND_ID
from helpers.verification.element import verify_is_visible
from helpers.verification.maestro import verify_molv_from_maestro_equals
from helpers.selection.sketcher import RGROUP_SCAFFOLD_IFRAME
from library.wait import until_condition_met
from library import dom

# Set name of LiveReport that will be duplicated
live_report_to_duplicate = {'livereport_name': '4 Compounds 3 Formulas', 'livereport_id': '890'}


@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_rgroup_enum_import_scaffolds(selenium):
    """
    Basic R-group enumeration test for importing Scaffolds to the sketcher via LiveReport:
    1. Use the Active LiveReport option and select a compound from the dropdown.
    2. Verify that the Compound Image is imported.
    3. Close the Enumeration wizard.
    4. Right-click on the row, and select 'Use in' >> 'Enumeration'.
    5. Verify that the R-group Enumeration wizard opens up.

    :param selenium: Selenium Webdriver
    """

    # Opening the R-group Enumeration panel
    open_enumeration_wizard(selenium, enumeration_type='R-Group')

    # Use the Active LiveReport option and select a compound from the dropdown.
    dom.click_element(selenium, RGROUP_ENUM_ACTIVE_LR_RADIO)
    dom.click_element(selenium, RGROUP_ENUM_ACTIVE_LR_DROPDOWN)
    dom.get_element(selenium, RGROUP_ENUM_ACTIVE_LR_COMPOUND_ID.format('V035624')).click()

    # wait for structure to import in sketcher
    until_condition_met(verify_if_enumeration_is_populated, retries=3, interval=1000, driver=selenium)

    # verify compound structure imported in sketcher is correct
    verify_molv_from_maestro_equals(selenium,
                                    RGROUP_SCAFFOLD_FOR_V035624.split('\n')[5].split()[3:5], RGROUP_SCAFFOLD_IFRAME)
    # Close the enumeration wizard
    close_enumeration_wizard(selenium)

    # Right-click on a row and 'Use in' >> 'Enumeration'
    use_compound_in_sketcher_and_verify(selenium, 'V035626', enumeration_sketcher=True, interval=1000)

    # verify compound structure imported in sketcher is correct
    verify_molv_from_maestro_equals(selenium,
                                    RGROUP_SCAFFOLD_FOR_V035626.split('\n')[5].split()[3:5], RGROUP_SCAFFOLD_IFRAME)

    verify_is_visible(selenium, NEW_ENUMERATION_WIZARD_WINDOW, message='Could not locate Enumeration Wizard window')
    verify_is_visible(selenium, ENUMERATION_HEADER, selector_text="R-GROUP ENUMERATION WIZARD")
