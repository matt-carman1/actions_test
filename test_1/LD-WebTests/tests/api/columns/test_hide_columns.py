from helpers.api.extraction.livereport import get_column_descriptor

live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}
test_type = 'api'


def test_hide_columns(ld_api_client, duplicate_live_report):
    """
    Test hide column in livereport

    :param ld_api_client: LDClient, ldclient object
    :param duplicate_live_report: fixture which duplicates livereport
    """
    # addable column id for 'Fake 3D model with 2 Poses (3D)' column
    addable_column_id = '11'

    live_report_id = duplicate_live_report.id
    column_descriptor = get_column_descriptor(ld_api_client, live_report_id, addable_column_id)
    # Hiding the column
    column_descriptor.hidden = True
    ld_api_client.add_column_descriptor(live_report_id, column_descriptor)

    # verify whether column hidden
    column_descriptor = get_column_descriptor(ld_api_client, live_report_id, addable_column_id)
    assert column_descriptor.hidden, "Hidden column: {} is having hidden=False".format(addable_column_id)
