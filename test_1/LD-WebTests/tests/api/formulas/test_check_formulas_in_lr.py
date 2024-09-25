import pytest
from requests import RequestException

from helpers.api.extraction.formula import get_formula_names
from helpers.api.verification.general import verify_error_response

from library.api.ldclient import get_api_client


# TODO: Change to single user(B) after SS-33687
def test_check_formulas_in_lr(ld_api_client):
    """
    Test list formulas in LiveReports using LR ID.
    1. List of formulas from a LR are correct
    2. Valid error for invalid LR
    3. Empty return for LR without formulas
    4. Valid error for non-accessible LR

    :param ld_api_client:  Fixture that returns ldclient object (for demo user)
    """

    # Checking formulas returned from a LR are correct
    lr_id = "890"  # LR: 4 Compounds 3 Formulas (Project: JS Testing)
    expected_formula_names = ['A1 + A2', 'substructureSearch', 'Max A1-A4']
    formula_object = get_formula_names(ld_api_client, lr_id)
    actual_formula_names = [formula.name for formula in formula_object]
    assert expected_formula_names == actual_formula_names

    # Checking for invalid LR
    lr_id = "-1"  # Invalid LR; ID doesn't exist
    with pytest.raises(RequestException) as error_response:
        get_formula_names(ld_api_client, lr_id)
    verify_error_response(error_response.value,
                          expected_status_code='400',
                          expected_error_message='One or more of the specified LiveReports do not exist')

    # Checking LR with no formulas returns empty list
    lr_id = "877"  # LR: Scatterplot Data (Project: JS Testing) (doesn't have any formula columns)
    formula_object = get_formula_names(ld_api_client, lr_id)
    actual_formula_names = [formula.name for formula in formula_object]
    assert len(actual_formula_names) == 0

    # Checking for inaccessible LR
    non_admin_client = get_api_client(username='userA', password='userA')
    lr_id = "890"  # Inaccessible LR (LR not accessible to the user 'userA', in project JS Testing)
    with pytest.raises(RequestException) as error_response:
        get_formula_names(non_admin_client, lr_id)
    verify_error_response(error_response.value, expected_status_code='403', expected_error_message='Permission denied')
