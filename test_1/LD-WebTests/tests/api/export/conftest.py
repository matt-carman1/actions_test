import pytest

from helpers.api.actions.column import add_columns_to_live_report
from helpers.api.actions.livereport import create_new_live_report, delete_live_report
from helpers.api.actions.row import add_rows_to_live_report

CORPORATE_ID_1 = "CRA-032662"
CORPORATE_ID_2 = "CRA-032664"
CORPORATE_ID_3 = "CRA-032703"
COLUMN_1_ID = 112
COLUMN_1_NAME = "STABILITY-PB-PH 7.4 (%Rem@2hr) [%]"
COLUMN_2_ID = 923
COLUMN_2_NAME = "CYP450 2C19-LCMS (%INH) [%]"


@pytest.fixture(scope="function")
def live_report_for_export(request, ld_client):
    live_report = create_new_live_report(ld_client, "Export")
    add_columns_to_live_report(ld_client, live_report.id, [COLUMN_1_ID, COLUMN_2_ID])
    add_rows_to_live_report(ld_client, live_report.id, [CORPORATE_ID_1, CORPORATE_ID_2, CORPORATE_ID_3])

    def finalizer():
        delete_live_report(ld_client, live_report.id)

    request.addfinalizer(finalizer)

    return live_report
