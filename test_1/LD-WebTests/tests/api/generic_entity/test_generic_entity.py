# NOTE(badlato): These tests will most likely have to be updated as the experimental functions evolve
import pytest
import json

from helpers.extraction import paths
from tests.api.generic_entity.util import build_unique_id
from ldclient.enums import GenericEntityImportDataType
from ldclient.requests import ImportEntityAlias
from ldclient.responses import GenericEntityParseResponse, EntityAliasSearchResponse, ParsedGenericEntityData

LD_PROPERTIES = {'ENABLE_GENERIC_ENTITY': 'true'}
import_entities = True
import_properties = True
skipped_columns = []
observations_to_delete = []


@pytest.mark.usefixtures('customized_server_config')
def test_generic_entity_entity_alias_search(ld_api_client):
    """
    Tests searching for available entity aliases.
    Searches for 1 unused alias & 1 used alias and verifies that the response reflects this state.

    :param ld_api_client: fixture for the ldclient object
    :type ld_api_client: LDClient
    """
    # NOTE(badlato): CRA-031137 exists in the starter data
    aliases = ['an-unused-alias', 'CRA-031137']
    actual = ld_api_client.entity_alias_search(aliases=aliases)
    expected = EntityAliasSearchResponse(results=[{
        'alias': 'an-unused-alias',
        'availability': 'unclaimed'
    }, {
        'alias': 'CRA-031137',
        'availability': 'unavailable'
    }])
    assert actual.as_dict() == expected.as_dict()


test_type = 'api'


@pytest.mark.usefixtures('customized_server_config')
def test_generic_entity_import_single_entity(ld_api_client, new_live_report):
    """
    Tests importing a single file as a generic entity.
    Imports a single entity and verifies the async task results.
    # TODO(badlato): Test that entity was added to the LiveReport
    # TODO(badlato): Test downloading the entity file

    :param ld_api_client: fixture for the ldclient object
    :type ld_api_client: LDClient

    :param new_live_report: fixture that creates an isolated LiveReport for this test
    :type new_live_report: ldclient.models.LiveReport
    """
    unique_id = build_unique_id()
    file_path = paths.get_resource_path("generic_file.txt")
    live_report_id = new_live_report.id
    import_entity_alias_obj = ImportEntityAlias(index=0, id=unique_id)
    entities_spec = [import_entity_alias_obj]
    import_type = GenericEntityImportDataType.SINGLE_ENTITY
    result = ld_api_client.import_generic_entity(filename=file_path,
                                                 live_report_id=live_report_id,
                                                 entities=entities_spec,
                                                 import_type=import_type,
                                                 import_entities=import_entities,
                                                 import_properties=import_properties,
                                                 skipped_columns=skipped_columns,
                                                 observation_ids_to_delete=observations_to_delete)
    responses = getattr(result, "import_responses")
    assert len(responses) == 1
    assert responses[0].entity_id == unique_id
    assert responses[0].success == True


@pytest.mark.usefixtures('customized_server_config')
def test_generic_entity_import_csv(ld_api_client, new_live_report):
    """
    Tests importing a CSV of IDs + properties.
    Imports a CSV of generic entity IDs and properties and verifies the async task results.
    TODO(badlato): Test import just IDs or just properties

    :param ld_api_client: fixture for the ldclient object
    :type ld_api_client: LDClient

    :param new_live_report: fixture that creates an isolated LiveReport for this test
    :type new_live_report: ldclient.models.LiveReport
    """
    num_ids = 5  # NOTE(badlato): Equal to number of IDs in generic_ids.csv
    ids = [build_unique_id() for _ in range(num_ids)]
    file_path = paths.get_resource_path("generic_ids.csv")
    live_report_id = new_live_report.id
    entities_spec = [ImportEntityAlias(index=i, id=ids[i]) for i in range(num_ids)]
    import_type = GenericEntityImportDataType.CSV_ROW_PER_ENTITY
    identifier = 's_m_entry_id (undefined)'
    result = ld_api_client.import_generic_entity(filename=file_path,
                                                 live_report_id=live_report_id,
                                                 entities=entities_spec,
                                                 import_type=import_type,
                                                 import_entities=import_entities,
                                                 import_properties=import_properties,
                                                 skipped_columns=skipped_columns,
                                                 observation_ids_to_delete=observations_to_delete,
                                                 identifier=identifier)
    responses = getattr(result, "import_responses")
    assert len(responses) == num_ids
    for i in range(num_ids):
        response = responses[i]
        assert response.entity_id == ids[i]
        assert response.success == True
        assert response.observations_imported == 2


@pytest.mark.usefixtures('customized_server_config')
@pytest.mark.app_defect(reason="LDIDEAS-7486")
def test_generic_entity_import_update_empty_entity(ld_api_client, new_live_report, empty_generic_entity):
    """
    Tests updating an empty generic entity with a file.
    Imports a file onto an existing (& empty) generic entity and verifies the async task results.

    :param ld_api_client: fixture for the ldclient object
    :type ld_api_client: LDClient

    :param new_live_report: fixture that creates an isolated LiveReport for this test
    :type new_live_report: ldclient.models.LiveReport

    :param empty_generic_entity: A fixture that creates an empty generic entity and returns the ID
    :type empty_generic_entity: str
    """
    file_path = paths.get_resource_path("generic_file.txt")
    live_report_id = new_live_report.id
    import_entity_alias_obj = ImportEntityAlias(index=0, id=empty_generic_entity, update_if_empty=True)
    entities_spec = [import_entity_alias_obj]
    import_type = GenericEntityImportDataType.SINGLE_ENTITY
    result = ld_api_client.import_generic_entity(filename=file_path,
                                                 live_report_id=live_report_id,
                                                 entities=entities_spec,
                                                 import_type=import_type,
                                                 import_entities=import_entities,
                                                 import_properties=import_properties,
                                                 skipped_columns=skipped_columns,
                                                 observation_ids_to_delete=observations_to_delete)
    responses = getattr(result, "import_responses")
    assert len(responses) == 1
    assert responses[0].entity_id == empty_generic_entity
    assert responses[0].success == True


@pytest.mark.usefixtures('customized_server_config')
def test_generic_entity_parse_csv(ld_api_client, new_live_report):
    """
    Tests parsing a CSV of IDs + properties.
    Uploads a CSV file of generic entity IDs & properties and verfies the response from the server.

    :param ld_api_client: fixture for the ldclient object
    :type ld_api_client: LDClient

    :param new_live_report: fixture that creates an isolated LiveReport for this test
    :type new_live_report: ldclient.models.LiveReport
    """
    file_path = paths.get_resource_path("generic_ids.csv")
    identifier = 's_m_entry_id (undefined)'
    live_report_id = new_live_report.id
    import_type = GenericEntityImportDataType.SINGLE_ENTITY
    actual = ld_api_client.parse_csv_for_generic_entity_import(filename=file_path,
                                                               identifier=identifier,
                                                               live_report_id=live_report_id,
                                                               type=import_type)
    expected = GenericEntityParseResponse(parsed_entity_data=[
        ParsedGenericEntityData(index=0,
                                alias='id1',
                                success=True,
                                messages=[],
                                availability='unclaimed',
                                properties=[{
                                    'PSA (PSA)': 'val2'
                                }, {
                                    'Plasma (Vd)': 'val1'
                                }]),
        ParsedGenericEntityData(index=1,
                                alias='id2',
                                success=True,
                                messages=[],
                                availability='unclaimed',
                                properties=[{
                                    'PSA (PSA)': 'val4'
                                }, {
                                    'Plasma (Vd)': 'val3'
                                }]),
        ParsedGenericEntityData(index=2,
                                alias='id3',
                                success=True,
                                messages=[],
                                availability='unclaimed',
                                properties=[{
                                    'PSA (PSA)': 'val6'
                                }, {
                                    'Plasma (Vd)': 'val5'
                                }]),
        ParsedGenericEntityData(index=3,
                                alias='id4',
                                success=True,
                                messages=[],
                                availability='unclaimed',
                                properties=[{
                                    'PSA (PSA)': 'val8'
                                }, {
                                    'Plasma (Vd)': 'val7'
                                }]),
        ParsedGenericEntityData(index=4,
                                alias='id5',
                                success=True,
                                messages=[],
                                availability='unclaimed',
                                properties=[{
                                    'PSA (PSA)': 'val10'
                                }, {
                                    'Plasma (Vd)': 'val9'
                                }]),
    ],
                                          column_metadata={
                                              's_m_entry_id (undefined)': '864',
                                              'PSA (PSA)': '3387',
                                              'Plasma (Vd)': '2744'
                                          })
    assert actual.as_dict() == expected.as_dict()
