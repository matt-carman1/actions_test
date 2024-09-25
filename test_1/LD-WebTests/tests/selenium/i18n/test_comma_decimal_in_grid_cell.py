import pytest

from helpers.change.grid_columns import get_cell
from helpers.change.live_report_picker import open_live_report

# This user is configured to use a comma for decimal point. This is a smoke test verifying that the feature works
test_username = 'commaDecimalUser'
test_password = 'commaDecimalUser'


@pytest.mark.smoke
@pytest.mark.usefixtures('open_project')
def test_comma_decimal_in_grid_cell(selenium):
    open_live_report(selenium, '50 Compounds 10 Assays')
    decimal_cell = get_cell(selenium, 'CRA-035534', 'r_epik_Ionization_Penalty (undefined)')
    assert decimal_cell.text == '0,00010'
