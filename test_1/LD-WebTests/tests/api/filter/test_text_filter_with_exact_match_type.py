from ldclient.models import TextColumnFilter
from helpers.api.verification.live_report import verify_compound_ids

live_report_to_duplicate = {'livereport_name': 'RPE Selenium Test LR', 'livereport_id': '2302'}
test_type = 'api'


def test_text_filter_with_exact_match_type(ld_api_client, duplicate_live_report):
    """
    Test to add text filter with 'exactly' as match type

    :param ld_api_client: fixture which creates api client
    :param duplicate_live_report: fixture which duplicates the LR
    """
    livereport_id = duplicate_live_report.id
    # Match type: Exactly; Column Name: ID; Column id: 1226
    text_filter_with_exact_match = TextColumnFilter(addable_column_id='1226',
                                                    text_match_type='exactly',
                                                    value='V040929')
    ld_api_client.set_column_filter(livereport_id, text_filter_with_exact_match)
    verify_compound_ids(ld_api_client, livereport_id, expected_compound_ids=["V040929"])
