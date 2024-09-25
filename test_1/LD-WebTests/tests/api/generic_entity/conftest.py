import pytest
from ldclient.requests import ImportEntityAlias
from helpers.extraction import paths
from tests.api.generic_entity.util import build_unique_id


@pytest.fixture(scope="function")
def empty_generic_entity(experimental_ldclient, new_live_report):
    file_path = paths.get_resource_path("generic_single_id.csv")
    live_report_id = new_live_report.id
    entities_spec = [ImportEntityAlias(index=0, id=build_unique_id())]
    import_type = 'csv_row_per_entity'
    identifier = 'ID'
    result = experimental_ldclient.import_generic_entity(filename=file_path,
                                                         live_report_id=live_report_id,
                                                         entities=entities_spec,
                                                         import_entities=True,
                                                         import_properties=True,
                                                         import_type=import_type,
                                                         identifier=identifier)
    return result.import_responses[0].entity_id
