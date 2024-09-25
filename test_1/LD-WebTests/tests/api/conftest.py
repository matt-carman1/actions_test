import requests

import pytest

from helpers.extraction import paths
from ldclient.__experimental.experimental_client import ExperimentalLDClient
from ldclient.enums import GenericEntityEntityType, GenericEntityImportDataType
from ldclient.requests import ImportEntityAlias
from library.api.exceptions import LiveDesignAPIException
from library.api.ldclient import get_api_client
from library.api.urls import LDCLIENT_HOST


@pytest.fixture(scope="function")
def ld_api_client(request):
    try:
        # This is because request.param is not available if we are doing indirect parametrization else it would
        # generate attribute error.
        test_username = request.param[0]
        test_password = request.param[1]
    except AttributeError:
        test_username = getattr(request.module, 'test_username', 'demo')
        test_password = getattr(request.module, 'test_password', 'demo')

    return get_api_client(username=test_username, password=test_password)


@pytest.fixture(scope="function")
def experimental_ldclient(request):
    test_username = getattr(request.module, 'test_username', 'demo')
    test_password = getattr(request.module, 'test_password', 'demo')

    try:
        # Note: Any wrong input for either LDCLIENT_HOST or username or password throws HTTPError.
        client = ExperimentalLDClient(host=LDCLIENT_HOST,
                                      username=test_username,
                                      password=test_password,
                                      compatibility_mode=(8, 10))
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    try:
        ping_return = client.ping()
        if ping_return:
            return client
        else:
            print("Experimental ldclient ping returned False. It may not be able to hit the about path. Please "
                  "check...")
            exit(1)
    except RuntimeError as e:
        raise SystemExit(e)


@pytest.fixture(scope="function")
def customized_server_config(request, ld_client):
    """
    Logs in a user using custom LD_PROPERTIES (w/o restart required)

    Example Usage:
        import pytest


        LD_PROPERTIES = {'ENABLE_INTERNAL_ENUMERATION': 'true'}


        @pytest.mark.usefixtures('customized_server_config')
        def test_new_enumeration(ld_client):
            print('breakpoint')
    :param ld_client: LDClient fixture
    :param request: request object with test metadata (from pytest fixture)
    :return: updated properties
    """

    try:
        properties = request.param
    except AttributeError:
        properties = getattr(request.module, 'LD_PROPERTIES', {})

    if len(properties) == 0:
        raise LiveDesignAPIException("At least one property in LD_PROPERTIES should be set.")

    config = ld_client.config()
    original_properties = {
        config_item.get('key'): config_item.get('value')
        for config_item in config
        if config_item.get('key') in properties.keys()
    }

    def fin():
        ld_client.update_properties(original_properties)

    request.addfinalizer(fin)
    properties = ld_client.update_properties(properties)
    return properties


@pytest.fixture(scope="function")
def import_biologic_entities(ld_api_client, new_live_report):
    """
    Imports biologic entities for testing
    """
    file_path = paths.get_resource_path("helm_sample.zip")
    live_report_id = new_live_report.id
    entities_spec = [ImportEntityAlias(index=idx, id='') for idx in range(0, 10)]
    import_type = GenericEntityImportDataType.ZIP_FILE_ENTRY_PER_ENTITY
    result = ld_api_client.import_generic_entity(filename=file_path,
                                                 live_report_id=live_report_id,
                                                 entities=entities_spec,
                                                 import_type=import_type,
                                                 entity_type=GenericEntityEntityType.BIOLOGIC,
                                                 import_entities=True,
                                                 import_properties=True,
                                                 skipped_columns=[],
                                                 observation_ids_to_delete=[])
    responses = getattr(result, "import_responses")
    assert len(responses) == 10
    # TODO(jordan): re-enable this assertion once we fix SS-42632
    # for response in responses:
    #     assert response.success == True, f"Failed to import entity at index {response.index}.  Failure messages: {response.messages}"

    return responses
