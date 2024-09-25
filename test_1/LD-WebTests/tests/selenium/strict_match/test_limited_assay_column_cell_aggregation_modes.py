import pytest

from helpers.change.strict_match_actions import open_create_limited_assay_column_dialog, add_remove_limiting_conditions, set_limited_column_title
from helpers.flows.grid import toggle_cell_aggregation_and_verify_column_content
from helpers.selection.assay import ASSAY_HEADER_AGGREGATION_LABEL
from helpers.selection.strict_match import LIMITING_CONDITION_TITLE_IN_DIALOG
from helpers.verification.assay import verify_assay_aggregation_column_label
from helpers.verification.element import verify_is_not_visible
from library import base, wait

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


@pytest.mark.usefixtures('open_livereport')
@pytest.mark.usefixtures('duplicate_live_report')
def test_limited_assay_column_cell_aggregation_modes(selenium):
    """
    Tests cell aggregation modes for a Limited Assay Column.
    Validates column contents are as expected by toggling the the following cell aggregation modes:
    1. Unaggregated
    2. Latest Result
    3. Median
    4. Mean(Arithmetic)
    5. Mean(Geometric)
    6. Min
    7. Max
    8. Std Dev
    9. Count
    """
    # Test Data
    pk_po_rat_auc = "PK_PO_RAT (AUC) [uM]"
    pk_po_rat_auc_column_title = "PK_PO_RAT (AUC)"
    limited_assay_pk_po_rat_auc = "[LIM] {}".format(pk_po_rat_auc)
    limiting_condition = "AUC"

    # Create a limited assay column with a limiting condition
    create_limiting_assay_dialog = open_create_limited_assay_column_dialog(selenium, pk_po_rat_auc)
    set_limited_column_title(selenium, pk_po_rat_auc_column_title)
    add_remove_limiting_conditions(create_limiting_assay_dialog, condition=limiting_condition, exact_text_match=True)
    base.click_ok(selenium)
    wait.until_not_visible(selenium, LIMITING_CONDITION_TITLE_IN_DIALOG, limiting_condition)

    # ----- Validation of cell contents ----- #
    # Cell Aggregation = "Unaggregated"
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Unaggregated",
                                                      ['20\n10', '', '0.3\n0.2\n0.1', '100'])
    verify_assay_aggregation_column_label(selenium, limited_assay_pk_po_rat_auc, "UNAGGREGATED")

    # Cell Aggregation = "Latest Result"
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Latest Result",
                                                      ['20', '', '0.3', '100'])
    verify_assay_aggregation_column_label(selenium, limited_assay_pk_po_rat_auc, "LATEST")

    # Cell Aggregation = "Median"
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Median",
                                                      ['15', '', '0.2', '100'])
    verify_assay_aggregation_column_label(selenium, limited_assay_pk_po_rat_auc, "MEDIAN")

    # Cell Aggregation = "Mean(Arithmetic)", the default (so no label in the header)
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Mean(Arithmetic)",
                                                      ['15', '', '0.2', '100'])
    verify_is_not_visible(selenium, ASSAY_HEADER_AGGREGATION_LABEL)

    # Cell Aggregation = "Mean(Geometric)"
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Mean(Geometric)",
                                                      ['14.14', '', '0.182', '100'])
    verify_assay_aggregation_column_label(selenium, limited_assay_pk_po_rat_auc, "GEO")

    # Cell Aggregation = "Min"
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Min",
                                                      ['10', '', '0.1', '100'])
    verify_assay_aggregation_column_label(selenium, limited_assay_pk_po_rat_auc, "MIN")

    # Cell Aggregation = "Max"
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Max",
                                                      ['20', '', '0.3', '100'])
    verify_assay_aggregation_column_label(selenium, limited_assay_pk_po_rat_auc, "MAX")

    # Cell Aggregation = "Std Dev"
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Std Dev",
                                                      ['5', '', '0.0816', '0'])
    verify_assay_aggregation_column_label(selenium, limited_assay_pk_po_rat_auc, "STDDEV")

    # Cell Aggregation = "Count"
    toggle_cell_aggregation_and_verify_column_content(selenium, limited_assay_pk_po_rat_auc, "Count",
                                                      ['2', '', '3', '1'])
    verify_assay_aggregation_column_label(selenium, limited_assay_pk_po_rat_auc, "COUNT")
