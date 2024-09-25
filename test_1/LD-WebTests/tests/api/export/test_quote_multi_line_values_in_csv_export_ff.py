import pytest

from helpers.api.actions.livereport import export_live_report
from helpers.api.verification.file_contents import verify_csv_column_contents

LD_PROPERTIES = {'QUOTE_MULTI_LINE_VALUES_IN_CSV_EXPORT': 'true'}


@pytest.mark.app_defect(reason='LDIDEAS-4705')
@pytest.mark.usefixtures('customized_server_config')
def test_quote_multi_line_values_in_csv_export_ff(ld_api_client):
    """
    API test for check QUOTE_MULTI_LINE_VALUES_IN_CSV_EXPORT feature flag.

    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    """
    # export_live_report returns bytes of mentioned export type, here export_lr is csv file contents in bytes
    exported_lr = export_live_report(ld_api_client, live_report_id='877')
    # verify multivalued column values have quotes
    verify_csv_column_contents(exported_lr,
                               column_name='Lot Amount Prepared',
                               expected_column_values=['"400 mg;50 mg;100 mg;50 mg"', '"3 g;3 g"', ''])
    verify_csv_column_contents(
        exported_lr,
        column_name='Lot Scientist',
        expected_column_values=['"demo;J.PALMER;J.PALMER;J.PALMER;J.PALMER"', '"demo;J.PALMER;J.PALMER"', 'demo'])

    # verify multi line(not multivalued) column values don't have quotes
    verify_csv_column_contents(exported_lr,
                               column_name='Rationale',
                               expected_column_values=[
                                   'demo: A small Live Report for testing the scatterplot feature.',
                                   'demo: A small Live Report for testing the scatterplot feature.',
                                   'demo: A small Live Report for testing the scatterplot feature.'
                               ])
