def test_non_existent_protocol_object_and_id_by_name(ld_api_client):
    """
    Test to get protocol objects and ids by name for a non-existent/Invalid protocol
    using two ldclient methods and verify them.
    i) list_protocols_by_name()
    ii) list_protocol_ids_by_name()

    :param ld_api_client: LDClient, ldclient object
    """
    # list_protocols_by_name()
    protocol_name = 'Unnamed Protocol'
    actual_protocol_count = len(ld_api_client.list_protocols_by_name(protocol_name))
    assert actual_protocol_count == 0, 'Expected protocol count {} but got {}'.format(0, actual_protocol_count)

    # list_protocol_ids_by_name()
    actual_protocol_ids_count = len(ld_api_client.list_protocol_ids_by_name(protocol_name))
    assert actual_protocol_ids_count == 0, 'Expected protocol ids count {} but got {}'\
        .format(0, actual_protocol_ids_count)
