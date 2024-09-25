import pytest

from helpers.flows.grid import set_custom_alignment
from helpers.verification.grid import verify_header_has_aligned, verify_svg

live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}


@pytest.mark.flaky(reason="SS-29520: test_custom_alignment fails when checking reference structure image CRA-035002")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_custom_alignment(selenium):
    """
    SS-28093: Smoke test custom alignment

    From the Compound Structure column's context menu, Set Alignment to pyridine.
    1. Verify that the "Compound Structure" column changes to Compound Structure (Aligned)"
    2. Two of the compounds will be aligned and one will not due to lack of pyridine core in the structure.

    :param selenium: Selenium WebDriver
    """
    # From the Compound Structure column's context menu, Set Alignment to pyridine.
    set_custom_alignment(selenium, 'pyridine.mrv')

    # Verify that the "Compound Structure" column header changes to "Compound Structure (Aligned)"
    verify_header_has_aligned(selenium)

    # This compound will not be aligned due to lack of pyridine core in the structure.
    verify_svg(selenium, 'CRA-035000', 'CustomAlignment1.svg')
    # These two compounds will be aligned due to pyridine core in the structures.
    verify_svg(selenium, 'CRA-035001', 'CustomAlignment2.svg')
    verify_svg(selenium, 'CRA-035002', 'CustomAlignment3.svg')
