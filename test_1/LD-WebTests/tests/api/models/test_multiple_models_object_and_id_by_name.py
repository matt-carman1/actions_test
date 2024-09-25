import pytest


def test_get_multiple_model_objects_with_same_name(ld_api_client):
    """
    Test to check multiple model objects with same name using get_model_by_name.

    :param ld_api_client: LDClient, ldclient object
    """
    # Using get_model_by_name() method
    model_name = 'Rotatable Bonds'
    expected_error_response = "Multiple models found with name: {}".format(model_name)
    with pytest.raises(RuntimeError) as error_response:
        ld_api_client.get_model_by_name(model_name)
    actual_object_error = str(error_response.value)
    assert expected_error_response == actual_object_error, \
        'Expected error message {} but got {}'.format(expected_error_response, actual_object_error)


def test_get_multiple_model_ids_with_same_name(ld_api_client):
    """
    Test check multiple model ids with same name using get_model_id_by_name.

    :param ld_api_client: LDClient, ldclient object
    """
    model_name = 'Rotatable Bonds'
    expected_error_response = "Multiple models found with name: {}".format(model_name)
    # Using get_model_id_by_name() method
    with pytest.raises(RuntimeError) as error_response:
        ld_api_client.get_model_id_by_name(model_name)
    actual_id_error = str(error_response.value)
    assert expected_error_response == actual_id_error, \
        'Expected error message {} but got {}'.format(expected_error_response, actual_id_error)
