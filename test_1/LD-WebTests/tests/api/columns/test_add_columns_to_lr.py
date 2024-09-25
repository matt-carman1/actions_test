from helpers.api.actions.column import add_columns_to_live_report
from helpers.api.extraction.livereport import get_live_report_column_ids

live_report_to_duplicate = {'livereport_name': 'Import Data', 'livereport_id': '878'}
test_type = 'api'


def test_add_columns(ld_api_client, duplicate_live_report):
    """
    API test for adding columns to LR
    1. Add a single column and verify
    2. Add multiple columns and verify
    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    """
    # Adding model column '[Img-Attachment-Value] Sample - 1'
    model_column_id = '16'
    add_columns_to_live_report(ld_api_client, duplicate_live_report.id, column_ids=[model_column_id])
    column_ids_in_lr = get_live_report_column_ids(ld_api_client, duplicate_live_report.id)
    assert model_column_id in column_ids_in_lr, "Column with id:{} is not added to the LR, Columns present in" \
                                                "LR:{}".format(model_column_id, column_ids_in_lr)

    # Add multiple columns to the lr and verify
    # comp_prop_col_id = '1254' model_column_id_2 = '36' assay_col_id = '827' other_col_id = '1281'
    # mpo_col_ids = '1221' ffc_col_id = '3595'
    list_of_addable_col_ids = ['1254', '36', '827', '1281', '1221', '3595', '84550', '83700']

    # last two col ids are MPO dependent cols, so adding cols upto 6
    add_columns_to_live_report(ld_api_client, duplicate_live_report.id, column_ids=list_of_addable_col_ids[:6])
    column_ids_in_lr = get_live_report_column_ids(ld_api_client, duplicate_live_report.id)
    for col_ids in list_of_addable_col_ids:
        assert col_ids in column_ids_in_lr, "Column with id:{} is not added to the LR, Columns present in" \
                                                "LR:{}".format(col_ids, column_ids_in_lr)
