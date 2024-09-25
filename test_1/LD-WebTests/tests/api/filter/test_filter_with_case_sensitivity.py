from ldclient import models
import pytest
from helpers.api.verification.live_report import verify_visible_row_count, verify_compound_ids

live_report_to_duplicate = {'livereport_name': 'Read Only Selenium Test LR', 'livereport_id': '2303'}
test_type = 'api'


def test_filter_with_case_sensitivity(ld_api_client, duplicate_live_report):
    """
    Test filter with case sensitivity.

    :param ld_api_client: LDClient, ldclient object
    :param duplicate_live_report: fixture which duplicates livereport
    """
    live_report_id = duplicate_live_report.id

    # Case sensitive filter - column_id:1250, column_name: Published Freeform Text Column
    text_filter_with_case_sensitivity_on = models.TextColumnFilter(addable_column_id='1250',
                                                                   text_match_type='anywhere',
                                                                   case_sensitive=True,
                                                                   value='sample')
    ld_api_client.set_column_filter(live_report_id, text_filter_with_case_sensitivity_on)
    verify_compound_ids(ld_api_client, live_report_id, expected_compound_ids=[])
    verify_visible_row_count(ld_api_client, live_report_id, expected_visible_row_count=0)

    # Case in-sensitive filter - column_id-1250, column_name: Published Freeform Text Column
    text_filter_with_case_sensitivity_off = models.TextColumnFilter(addable_column_id='1250',
                                                                    text_match_type='anywhere',
                                                                    case_sensitive=False,
                                                                    value='sample')
    ld_api_client.set_column_filter(live_report_id, text_filter_with_case_sensitivity_off)
    verify_compound_ids(ld_api_client, live_report_id, expected_compound_ids=['V035624', 'V035625'])
    verify_visible_row_count(ld_api_client, live_report_id, expected_visible_row_count=2)

    # Removing added filter for column: 1250 - Published Freeform Text Column
    ld_api_client.remove_column_filter(live_report_id, '1250')
    verify_compound_ids(ld_api_client, live_report_id, expected_compound_ids=['V035624', 'V035625', 'V055682'])
    verify_visible_row_count(ld_api_client, live_report_id, expected_visible_row_count=3)
