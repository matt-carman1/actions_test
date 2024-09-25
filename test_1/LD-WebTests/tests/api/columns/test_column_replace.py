from library.api.wait import wait_until_condition_met
from helpers.api.actions.column import remove_columns_from_live_report, replace_column_async, add_columns
from helpers.api.actions.livereport import export_live_report
from helpers.api.verification.file_contents import verify_csv_column_names_and_compound_ids

test_type = 'api'


def test_replace_column_successful(ld_api_client, new_live_report):
    """
    :param ld_api_client: LDClient, ldclient object
    :param new_live_report: fixture that creates a new LiveReport.

    Verifies columns are being created and then replaced successfully
    """
    columns = add_columns(ld_api_client, new_live_report, ["column1", "column2"])
    remove_columns_from_live_report(ld_api_client, new_live_report.id, [columns[0].id])
    exported_live_report = export_live_report(ld_api_client, new_live_report.id)

    verify_csv_column_names_and_compound_ids(exported_live_report,
                                             expected_column_names=[columns[1].name],
                                             unexpected_column_names=[columns[0].name])

    # Replacing the column using api
    replace_column_async(ld_api_client, columns[1].id, columns[0].id, [new_live_report.project_id])

    def assert_column_replaced():
        exported_live_report2 = export_live_report(ld_api_client, new_live_report.id)
        verify_csv_column_names_and_compound_ids(exported_live_report2,
                                                 expected_column_names=[columns[0].name],
                                                 unexpected_column_names=[columns[1].name])

    wait_until_condition_met(assert_column_replaced)
