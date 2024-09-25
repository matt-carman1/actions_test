from ldclient.models import ModelCommand

# Protocol data
test_protocol_name = 'Protocol'
test_protocol_commands = [ModelCommand(command='${Hello:NUMERIC-INPUT}', driver_id='1')]


def test_create_protocol(ld_api_client, new_protocol_via_api):
    """
    Test create simple protocol

    :param ld_api_client: fixture which creates api client
    :param new_protocol_via_api: fixture which creates protocol
    """
    # validate protocol created in project
    protocols = ld_api_client.get_protocols_by_project_id(project_ids=['4'])
    # getting protocol ids from protocols
    protocol_ids = [protocol.id for protocol in protocols]
    assert new_protocol_via_api.id in protocol_ids, \
        "Protocol with ID:{} is not created in JS Testing(project id=4) Project".format(new_protocol_via_api.id)

    # validating protocol id
    expected_id = ld_api_client.get_protocol_id_by_name(new_protocol_via_api.name)
    assert str(expected_id) == new_protocol_via_api.id

    expected_protocol_object = ld_api_client.get_protocol_by_id(expected_id)
    # validating protocol object fields
    except_fields = ['created_at', 'updated_at', 'as_merged']
    for field in expected_protocol_object._fields:
        if field in except_fields:
            continue
        expected = getattr(expected_protocol_object, field)
        actual = getattr(new_protocol_via_api, field)
        assert str(expected) == str(actual), \
            "{} value is not matching with expected. Expected: {}, but got: {}".format(field, expected, actual)
