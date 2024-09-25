def verify_template_vars(actual_model_temp_vars, expected_model_temp_vars):
    """
    Verify model template vars fields i,e Model data fields (name, type, data, is_optional, optional_parameter)

    :param actual_model_temp_vars: ModelTemplateVar, actual template vars object
    :param expected_model_temp_vars: ModelTemplateVar, expected template vars object
    """
    for field in ['name', 'type', 'data', 'is_optional', 'optional_parameter_name']:
        actual_value = getattr(actual_model_temp_vars, field)
        expected_value = getattr(expected_model_temp_vars, field)
        assert actual_value == expected_value, \
            "{} value mismatched. Expected value: {}, but got:{}".format(field, expected_value,
                                                                         actual_value)


def verify_expected_protocols_names_exists_in_protocols_found(protocols, expected_names):
    """
    Verifies that the list of expected names exists within the list of protocols passed in

    :param protocols: list, List of protocol objects retrieved.
    :param expected_names: list, List of expected protocol names
    """
    actual_protocol_names = set([protocol.name for protocol in protocols])
    expected_names_set = set(expected_names)
    assert expected_names_set.issubset(actual_protocol_names)


def verify_expected_driver_names_exists_in_drivers_found(drivers, expected_names):
    """
    Verifies that the list of expected names exists within the list of drivers passed in

    :param drivers: list, List of driver objects retrieved.
    :param expected_names: list, List of expected driver names
    """
    actual_driver_names = set([driver.name for driver in drivers])
    expected_names_set = set(expected_names)
    assert expected_names_set.issubset(actual_driver_names)


def verify_expected_driver_name_exists_in_driver_found(driver, expected_name):
    """
    Verifies that the expected name is same as driver name

    :param driver: driver object
    :param expected_name: expected driver name
    """
    actual_name = driver.name
    assert actual_name == expected_name, \
            "Expected value: {}, but got:{}".format(expected_name, actual_name)


def verify_protocols_names_is_equal_to_expected(protocols, expected_names):
    """
    Compares expected and actual protocol names.

    :param protocols: list, List of protocol objects retrieved.
    :param expected_names: list, List of expected protocol names
    """
    actual_protocol_names = [protocol.name for protocol in protocols]
    assert actual_protocol_names == expected_names


def verify_protocol_model_predictions(actual_model_returns_obj, expected_model_returns_obj):
    """
    Verification of protocol and model predictions

    :param actual_model_returns_obj: list of objects, the actual returns object
    :param expected_model_returns_obj: list of objects, the expected returns object
    :return:
    """
    for index, return_of_actual in enumerate(actual_model_returns_obj):
        actual_return_display_name = return_of_actual.display_name
        actual_return_key = return_of_actual.key
        actual_return_type = return_of_actual.type
        actual_return_units = return_of_actual.units
        actual_return_precision = return_of_actual.precision

        expected_return_display_name = expected_model_returns_obj[index].display_name
        expected_return_key = expected_model_returns_obj[index].key
        expected_returns_type = expected_model_returns_obj[index].type
        expected_returns_units = expected_model_returns_obj[index].units
        expected_returns_precision = expected_model_returns_obj[index].precision

        # Verification of all the parameters of the predictions
        assert actual_return_display_name == expected_return_display_name
        assert actual_return_key == expected_return_key
        assert actual_return_type == expected_returns_type
        assert actual_return_units == expected_returns_units
        assert actual_return_precision == expected_returns_precision
