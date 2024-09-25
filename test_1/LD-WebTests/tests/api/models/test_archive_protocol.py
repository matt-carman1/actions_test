from ldclient.models import ModelCommand, ModelTemplateVar
from ldclient.enums import RecursiveTag, ModelReturnType
from helpers.api.actions.model import create_model_via_api, archive_models
from library.utils import make_unique_name
from helpers.api.verification.general import verify_error_response

import pytest

# Protocol data
test_protocol_name = 'Protocol'
test_protocol_commands = [ModelCommand(command='${Length:TEXT-INPUT}', driver_id='1')]
test_protocol_template_vars = [
    ModelTemplateVar(tag=RecursiveTag.DEFAULT,
                     type='STRING',
                     name='Length',
                     is_optional=False,
                     data="template var data")
]
archive_after_test = False


def test_archive_protocol(ld_api_client, new_protocol_via_api):
    """
    Test archiving protocols. Steps followed are:

    a. Create a protocol which will not archive automatically.
    b. Create dependent models of the protocol.
    c. Update the protocol to archive and ensure protocol is not archived. (since it has dependent models)
    d. Validate that the protocol is still present in the project
    e. Now archive the model and subsequently delete the protocol.
    f. Ensure that the  protocol is now deleted and is no longer present in the project.


    :param ld_api_client: fixture which creates api client
    :param new_protocol_via_api: fixture which creates protocol
    """

    # Creating a dependent model of the protocol
    normal_model = create_model_via_api(ld_api_client,
                                        make_unique_name('Model1'),
                                        'description',
                                        folder=new_protocol_via_api.folder,
                                        parent=new_protocol_via_api.id,
                                        project_ids=new_protocol_via_api.project_ids)

    # Updating the protocol to archived and ensuring the protocol will not be archived by handling the exception.
    with pytest.raises(Exception) as error_response:
        new_protocol_via_api.archived = True
        ld_api_client.create_or_update_protocol(new_protocol_via_api)
    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message='Cannot archive '
                          'protocol with dependent un-archived models')

    # Validating protocol still present in project
    protocols = ld_api_client.get_protocols_by_project_id(project_ids=['4'])

    # getting protocol ids from protocols
    protocol_ids = [protocol.id for protocol in protocols]
    assert str(new_protocol_via_api.id) in protocol_ids, \
        "Protocol with ID:{} is not created in JS Testing(project id=4) Project".format(new_protocol_via_api.id)

    # Archiving dependent models
    archive_models(ld_api_client, [normal_model])

    # Finally deleting the protocol
    new_protocol_via_api.archived = True
    archived_protocol_object = ld_api_client.create_or_update_protocol(new_protocol_via_api)

    protocol_object = ld_api_client.get_protocol_by_id(new_protocol_via_api.id)

    # Validation that updated protocol id and archived protocol id are similar
    assert archived_protocol_object.id == str(protocol_object.id), \
        "Updated protocol id: {} is different from original protocol id: {}".format(archived_protocol_object.id,
                                                                                    protocol_object.id)

    # Validation that the protocol is archived - boolean comparison
    assert protocol_object.archived == archived_protocol_object.archived, \
        "Either original protocol with ID:{} or updated protocol with id: {} is not archived". format(
            protocol_object.id, archived_protocol_object.id)
