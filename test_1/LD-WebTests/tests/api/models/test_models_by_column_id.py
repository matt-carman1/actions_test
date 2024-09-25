import pytest
from requests import RequestException

from helpers.api.verification.general import verify_error_response


def test_models_by_column_id(ld_api_client):
    """
    Test to get the list of models by column id.
    Three test cases are being tested here,
    1. one column id passed and subsequently tested that the model object returned is similar to the model definition.
    2. Two column ids passed and subsequently tested that the model object returned for each are similar to the each of
    the original model definition.
    3. A fake column id passed and subsequently tested that an appropriate error response is recorded.

    :param ld_api_client: LDClient, ldclient object
    """
    # One column id passed and subsequently tested that the model ids and the addable column ids are as defined.
    addable_column_id = ["1254"]
    random_int_model_id = '2301'
    model_with_column_id = ld_api_client.get_models_by_column_id(addable_column_id)

    # Verification by asserting for length and model ids and model addable columns ids.
    assert len(model_with_column_id) == 1
    assert model_with_column_id[0].id == random_int_model_id, \
        "Model id from the model object returned via column_id does not match original model ids"
    assert model_with_column_id[0].returns[0].addable_column_id == addable_column_id[0], \
        "Addable column id from the model object returned via column_id does not match original addable column id"

    # Two column ids passed and subsequently tested that the model ids and the addable column ids are as defined.
    addable_column_id_list = ["14", "1254"]
    fake_3d_model_id = '1201'
    models_with_column_id = ld_api_client.get_models_by_column_id(addable_column_id_list)

    # Verification by asserting for length and model ids and model addable column ids.
    assert len(models_with_column_id) == 2
    actual_model_ids = [model.id for model in models_with_column_id]
    assert actual_model_ids == [fake_3d_model_id, random_int_model_id], \
        "Model ids from the model object returned via column_ids does not match original model ids"

    actual_addable_column_ids = [model.returns[0].addable_column_id for model in models_with_column_id]
    assert actual_addable_column_ids == addable_column_id_list, \
        "Addable column ids from the model object returned via column_ids does not match original addable column ids"

    # A fake column id passed and subsequently tested that a appropriate error response is recorded.
    fake_addable_id = ["789145"]
    expected_error_response = "Columns: [789145] do not exist"
    with pytest.raises(RequestException) as error_response:
        ld_api_client.get_models_by_column_id(fake_addable_id)
    verify_error_response(error_response.value, '400', expected_error_response)
