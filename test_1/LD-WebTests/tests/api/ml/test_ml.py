import pytest
import json
import time

from ldclient.api import paths


def _get_page(ldclient,
              column_ids,
              project_id,
              from_date,
              page_details=None,
              live_report_id=None,
              include_unpublished=None,
              search_type='unaggregated_data'):
    query_name = '{}_query'.format(search_type)
    payload = {
        'search_type': search_type,
        query_name: {
            'project_id': str(project_id),
            'addable_column_ids': column_ids,
            'from_date': from_date,
            'live_report_id': live_report_id,
            'include_unpublished': include_unpublished,
        }
    }
    if page_details:
        payload[query_name]['page_details'] = page_details

    return ldclient.client.post(service_path=paths.DATA_PATH, path='/search', data=json.dumps(payload))


def get_all_data_for_columns(ldclient,
                             column_ids,
                             project_id,
                             from_date=0,
                             page_size=500,
                             search_type='unaggregated_data',
                             live_report_id=None,
                             include_unpublished=None):
    next_page_details = {'page_size': page_size}
    results = []
    while next_page_details is not None:
        response = _get_page(ldclient,
                             column_ids,
                             project_id,
                             from_date,
                             next_page_details,
                             search_type=search_type,
                             live_report_id=live_report_id,
                             include_unpublished=include_unpublished)
        next_page_details = response.get('next_page_details')
        results += response['results']
    return results


def test_basic(ld_client):
    expected_results = {
        'CHEMBL1044': '-4.0',
        'CHEMBL1024': '-3.369',
        'CHEMBL107': '-7.513',
        'CHEMBL1088': '-4.0',
        'CHEMBL105': '-6.146',
        'CHEMBL1081': '-6.851',
        'CHEMBL1015': '-4.0',
        'CHEMBL1064': '-6.045',
        'CHEMBL1006': '-4.125',
        'CHEMBL103': '-4.611',
        'CHEMBL104': '-4.686',
        'CHEMBL1071': '-4.0',
        'CHEMBL109': '-3.274'
    }

    assay_results = get_all_data_for_columns(ld_client, ['2873'], 2, page_size=500)

    assert len(assay_results) == 13
    for entry in assay_results:
        assert '2873' == entry['column_id']
        assert (expected_results.get(entry['entity_id'], 'entity not found') == entry['data']['value'])


@pytest.mark.parametrize("page_size", [500, 50, 1])
def test_pagination_multiple_column_types(ld_client, page_size):
    # fetch the expected results. Use a page size large enough that only one
    # request is necessary and use two separate requests to eliminate any
    # issues with requesting both assay and model data at the same time.
    expected_assay_results = get_all_data_for_columns(ld_client, ['2873'], 2, page_size=500)
    expected_results = (expected_assay_results + get_all_data_for_columns(ld_client, ['14'], 2, page_size=500))
    results = get_all_data_for_columns(ld_client, ['2873', '14'], 2, page_size=page_size)

    # The second call should always have more results
    assert len(results) >= len(expected_results)

    def key(res):
        return (res['entity_id'], res['column_id'], res['data']['value'])

    # loop until it looks like they've reached a steady state.
    for i in range(10):
        if sorted(results, key=key) == sorted(expected_results, key=key):
            return
        # If the results are not what we expect, then it should be because
        # there have been new entries added since the expected results were
        # fetched.
        assert len(results) > len(expected_results)
        time.sleep(1)
        expected_results = (expected_assay_results + get_all_data_for_columns(ld_client, ['14'], 2, page_size=500))

        # should still be getting longer
        assert len(expected_results) >= len(results)

        results = get_all_data_for_columns(ld_client, ['2873', '14'], 2, page_size=page_size)

        # yet again, should be getting longer.
        assert len(results) >= len(expected_results)
    assert sorted(results, key=key) == sorted(expected_results, key=key)


def test_mpo_new(ld_client):
    EXPECTED_COUNT = 270
    for i in range(10):
        mpo_results = get_all_data_for_columns(ld_client, ['3588'],
                                               4,
                                               page_size=500,
                                               live_report_id='1298',
                                               search_type='mpo_or_unaggregated_data',
                                               include_unpublished=True)
        if len(mpo_results) == EXPECTED_COUNT:
            return
        assert len(mpo_results) < EXPECTED_COUNT
        time.sleep(1)
    assert len(mpo_results) == EXPECTED_COUNT


def test_mpo_old(ld_client):
    EXPECTED_COUNT = 0
    for i in range(10):
        mpo_results = get_all_data_for_columns(ld_client, ['3588'], 4, page_size=500, live_report_id='1298')
        assert len(mpo_results) <= EXPECTED_COUNT
        time.sleep(1)

    assert len(mpo_results) == EXPECTED_COUNT
