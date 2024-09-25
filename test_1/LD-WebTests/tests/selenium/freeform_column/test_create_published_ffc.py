import pytest

from helpers.change.freeform_column_action import create_ffc
from helpers.verification.data_and_columns_tree import verify_column_exists_in_column_tree
from library.utils import make_unique_name

live_report_to_duplicate = {'livereport_name': 'FFC Selenium Test LR', 'livereport_id': '2304'}
test_report_name = 'FFC Selenium Test LR'
test_type = 'selenium'


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
@pytest.mark.parametrize("ffc_type", ["Text", "Number", "True/false", "Date", "File / Image"])
def test_create_published_ffc(driver, ffc_type):
    """
    Checking Published FFCs with different data types.
    1.Open live_report
    2.Duplicate a live_report
    3.Create a published FFC with different types
    4.Verify the different types of published FFC's
    :param ffc_type: Livereport column types(Text, True/false, Number, Date, File / Image)
    """
    ffc_name = make_unique_name("ffc")
    create_ffc(driver, ffc_name, column_type=ffc_type, publish=True)
    verify_column_exists_in_column_tree(driver, ffc_name, search_retries=3)
