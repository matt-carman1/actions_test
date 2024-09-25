# TODO rename file to test_generic_structure_match_filter.py after CR
import pytest

from helpers.api.verification.live_report import verify_compound_ids
from ldclient.models import GenericStructureMatchColumnFilter

test_type = 'api'
LD_PROPERTIES = {'ENABLE_BIOLOGICS': 'true', 'ENABLE_GENERIC_ENTITY': 'true'}
COMPOUND_STRUCTURE_ADDABLE_COLUMN_ID = '1228'


@pytest.mark.serial
@pytest.mark.parametrize("structure, matching_entity_indices", [
    ('PEPTIDE1{A}$$$$', [1, 2, 6, 7, 8]),
    ('PEPTIDE1{P.Q.R}$$$$', [0]),
])
@pytest.mark.usefixtures('customized_server_config')
def test_generic_structure_match_filter(ld_api_client, new_live_report, import_biologic_entities, structure,
                                        matching_entity_indices):
    """
    Test to add a generic structure match filter

    :param ld_api_client: fixture which creates api client
    :param new_live_report: fixture which creates a new LR
    :param import_biologic_entities: fixture which imports biologics into the LR
    :param structure: structure to filter on
    :param expected_structure: structure expected to be saved in the filter
    :param matching_entity_indices: indices from the import file of the entities expected to match the filter
    """
    livereport_id = new_live_report.id
    generic_structure_match_filter = GenericStructureMatchColumnFilter(
        addable_column_id=COMPOUND_STRUCTURE_ADDABLE_COLUMN_ID, value=structure)
    ld_api_client.set_column_filter(livereport_id, generic_structure_match_filter)

    assert _get_generic_structure_match_filter(ld_api_client, livereport_id).value == structure
    expected_entity_ids = _get_expected_entity_ids_from_indices(matching_entity_indices, import_biologic_entities)
    verify_compound_ids(ld_api_client, livereport_id, expected_compound_ids=expected_entity_ids)

    # Set filter to None and verify that all entities are returned
    # This tests that empty filters don't don't filter anything as well as that filters can be updated
    col_descriptor = ld_api_client.column_descriptor(livereport_id, COMPOUND_STRUCTURE_ADDABLE_COLUMN_ID)
    col_descriptor.filters[0]['value'] = None
    ld_api_client.update_column_descriptor(livereport_id, col_descriptor)

    # Confirm that None is converted to an empty string on the server
    assert _get_generic_structure_match_filter(ld_api_client, livereport_id).value == ''
    all_expected_entity_ids = _get_expected_entity_ids_from_indices([0, 1, 2, 3, 6, 7, 8, 9], import_biologic_entities)
    verify_compound_ids(ld_api_client, livereport_id, expected_compound_ids=all_expected_entity_ids)


def _get_generic_structure_match_filter(ld_api_client, livereport_id):
    filters = [
        filter for filter in ld_api_client.column_filters(livereport_id)
        if str(filter.addable_column_id) == COMPOUND_STRUCTURE_ADDABLE_COLUMN_ID and
        filter.filter_type == 'generic_structure_match'
    ]
    assert len(filters) == 1
    return filters[0]


def _get_expected_entity_ids_from_indices(expected_entity_indices, import_biologic_entities):
    return [
        gen_id for idx in expected_entity_indices for gen_id in import_biologic_entities[idx].all_ids
        if gen_id.startswith('GEN')
    ]
