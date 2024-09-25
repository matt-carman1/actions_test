from ldclient.models import ModelCommand

test_protocol_name = 'Test Schrodinger Python Template'
is_unique_name_required = False
test_protocol_commands = [ModelCommand(command='${Hello:NUMERIC-INPUT}', driver_id='1')]


def test_multiple_protocols_object_and_id_by_name(ld_api_client, new_protocol_via_api):
    """
    Test to get protocol objects and ids by name for multiple protocols with same name
    using two ldclient methods and verify them.
    i) list_protocols_by_name()
    ii) list_protocol_ids_by_name()

    NOTE: Since there are no two protocols in starter data with same name.
          This test creates one and delete it at the end.

    :param ld_api_client: LDClient, ldclient object
    """
    # list_protocols_by_name()
    actual_protocol_count = len(ld_api_client.list_protocols_by_name(test_protocol_name))
    assert actual_protocol_count == 2, 'Expected protocol count {}, but got {}'.format(2, actual_protocol_count)

    # list_protocol_ids_by_name()
    expected_protocol_ids = ['3554', new_protocol_via_api.id]
    actual_protocol_ids = ld_api_client.list_protocol_ids_by_name(test_protocol_name)
    assert expected_protocol_ids == actual_protocol_ids, \
        'Expected protocol IDs {} but got {}'.format(expected_protocol_ids, actual_protocol_ids)
