def verify_error_response(response, expected_status_code, expected_error_message):
    """
    verify error code and message for response.

    :param response: RequestException, error response from any ldclient method
    :param expected_status_code: str, status code to verify
    :param expected_error_message: str, error message to verify
    """
    assert '<Response [{}]>'.format(expected_status_code) == str(response.response), \
        "Expected status code: {}, But got: {}".format(expected_status_code, str(response.response))
    assert expected_error_message in response.args[0], \
        "Expected message: {}, is not present in Actual Message:{}".format(expected_error_message, response.args[0])


def assert_dicts_equal_except(dict1: dict, dict2: dict, except_keys: list):
    """
    Asserts that two dicts are equal, except for the keys specified.
    :param dict1: first dictionary
    :param dict2: second dictionary
    :param except_keys: The keys of the fields of the dicts that are allowed to be different
    """

    for key in (dict1.keys() | dict2.keys()) - set(except_keys):
        assert key in dict1, "Key: {} not present in dictionary:{}.".format(key, dict1)
        assert key in dict2, "Key: {} not present in dictionary:{}.".format(key, dict2)
        dict1_value = dict1.get(key)
        dict2_value = dict2.get(key)
        assert dict1_value == dict2_value, "{} value mismatched. value in dict1:{} and value in dict2:{}".format(
            key, dict1_value, dict2_value)
