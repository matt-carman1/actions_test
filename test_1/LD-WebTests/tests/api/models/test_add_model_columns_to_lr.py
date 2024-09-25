# LiveReport details to duplicate
from helpers.api.actions.column import add_columns_to_live_report
from helpers.api.extraction.livereport import get_live_report_column_ids

live_report_to_duplicate = {'livereport_name': 'Import Data', 'livereport_id': '878'}
test_type = 'api'


def test_add_model_columns_to_lr(ld_api_client, duplicate_live_report):
    """
    Test add model columns to the livereport.
    1. Add model column and Parametrized model column to the LR.
    2. Verify columns added to LR

    :param ld_api_client: LDClient, fixture that returns ldclient object
    :param duplicate_live_report: LiveReport, fixture that duplicates lr and returns duplicated lr object
    """
    # columns ids for Model and Parametrized Model columns
    model_column_id = ld_api_client.get_model_by_name('[Img-Attachment-Value] Sample - 1').returns[0].addable_column_id
    param_model_column_id = ld_api_client.get_model_by_name('Parameterizable Example').returns[0].addable_column_id

    # adding columns to the LR
    add_columns_to_live_report(ld_api_client,
                               duplicate_live_report.id,
                               column_ids=[model_column_id, param_model_column_id])

    # Verify whether columns added to the LR
    column_ids_in_lr = get_live_report_column_ids(ld_api_client, duplicate_live_report.id)
    assert model_column_id in column_ids_in_lr, "Model column with id:{} is not added to the LR, Columns present in" \
                                                "LR:{}".format(model_column_id, column_ids_in_lr)
    assert param_model_column_id in column_ids_in_lr, "Param Model column with id:{} is not added to the LR, Columns " \
                                                      "present in LR:{}".format(param_model_column_id, column_ids_in_lr)
