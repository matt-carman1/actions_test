from helpers.api.actions.livereport import execute_live_report
from helpers.api.verification.live_report import verify_execute_live_report_response

test_type = 'api'


def test_execute_live_report(ld_client, new_live_report):
    """
    Test execute live report function with Existed Live report and non-existed Live report.

    :param ld_client: LDClient
    :param new_live_report: fixture for create live report
    """
    # Executing new live report
    response = execute_live_report(ld_client, new_live_report.id)
    verify_execute_live_report_response(response, new_live_report.id, expected_column_count=8, expected_row_count=0)

    # Executing live report with columns and rows
    response = execute_live_report(ld_client, '883')
    verify_execute_live_report_response(response, '883', expected_column_count=11, expected_row_count=3)

    # Executing non existed live report
    response = execute_live_report(ld_client, '-1')
    verify_execute_live_report_response(response, '-1')
