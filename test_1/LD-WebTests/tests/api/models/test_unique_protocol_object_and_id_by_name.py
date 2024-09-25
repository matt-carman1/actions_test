def test_unique_protocol_object_and_id_by_name(ld_api_client):
    """
    Test to get protocol objects and ids by name for an unique protocol
    using two ldclient methods and verify them.
    i) list_protocols_by_name()
    ii) list_protocol_ids_by_name()

    :param ld_api_client: LDClient, ldclient object
    """
    # list_protocols_by_name()
    protocol_name = 'Test Async Template'
    actual_protocol_count = len(ld_api_client.list_protocols_by_name(protocol_name))
    assert actual_protocol_count == 1, 'Expected protocol count {} but got {}'.format(1, actual_protocol_count)

    # list_protocol_ids_by_name()
    expected_protocol_id = ['3552']
    actual_protocol_id = ld_api_client.list_protocol_ids_by_name(protocol_name)
    assert expected_protocol_id == actual_protocol_id, \
        'Expected protocol IDs {} but got {}'.format(expected_protocol_id, actual_protocol_id)
