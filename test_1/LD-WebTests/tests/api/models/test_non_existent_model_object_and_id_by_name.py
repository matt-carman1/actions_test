import pytest


def test_non_existent_model_object_and_id_by_name(ld_api_client):
    """
    Test to get model objects and ids by name for a non-existent model
    using two ldclient methods and verify them.
    i) get_model_by_name()
    ii) get_model_id_by_name()

    :param ld_api_client: LDClient, ldclient object
    """
    # Using get_model_by_name() method
    model_name = 'Unnamed Model'
    expected_error_response = "No models found with name: {}".format(model_name)
    with pytest.raises(RuntimeError) as error_response:
        ld_api_client.get_model_by_name(model_name)
    actual_object_error = str(error_response.value)
    assert expected_error_response == actual_object_error, \
        'Expected error message {} but got {}'.format(expected_error_response, actual_object_error)

    # Using get_model_id_by_name() method
    with pytest.raises(RuntimeError) as error_response:
        ld_api_client.get_model_id_by_name(model_name)
    actual_id_error = str(error_response.value)
    assert expected_error_response == actual_id_error, \
        'Expected error message {} but got {}'.format(expected_error_response, actual_id_error)
