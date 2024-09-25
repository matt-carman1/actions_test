"""
Verifications for maestro sketcher.
"""

from helpers.extraction.maestro import get_molv
from helpers.selection.sketcher import SKETCHER_IFRAME


def verify_molv_from_maestro_equals(driver, expected_atoms_bonds_count, sketcher_iframe_selector=SKETCHER_IFRAME):
    """
    Verify that the molv3 representation of the current structure in the maestro
    sketcher is as expected.

    :param driver: webdriver
    :param expected_atoms_bonds_count: list, verification that the list containing the num of atoms and bonds are as expected.
    :param sketcher_iframe_selector: str, optional, the selector for the sketcher iframe.
                                     Defaults to '#design-pane-sketcher'
    
    """
    actual_molv3 = ''

    def get_actual_molv(driver):
        nonlocal actual_molv3
        actual_molv3 = get_molv(driver, sketcher_iframe_selector)
        return actual_molv3

    molv3_from_sketcher = get_actual_molv(driver)

    # Finding the number of atoms and bonds present in the sketcher.
    actual_num_atoms_and_bonds = molv3_from_sketcher.split('\n')[5].split()[3:5]

    # Verification that the number of atoms and bonds of the original molv3 matches that generated from the sketcher
    assert expected_atoms_bonds_count == actual_num_atoms_and_bonds, \
        "The number of atoms and bonds of the molv3 does not match from the one returned by the sketcher, i.e expected {} actual {}".format(expected_atoms_bonds_count, actual_num_atoms_and_bonds)
