import pytest

from helpers.extraction import paths
from library.utils import is_k8s

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': 2048}
test_type = 'api'


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
def test_run_maestro_export(ld_api_client, duplicate_live_report):
    """
    Test Maestro Export doesn't fail for numeric IDs
    :param ld_api_client: fixture that returns ldclient object.
    """
    live_report_id = duplicate_live_report.id
    data_path = paths.get_resource_path("api/")
    ld_api_client.load_sdf(live_report_id=live_report_id,
                           filename='{0}/test_run_maestro_export.sdf'.format(data_path),
                           compounds_only=True,
                           compound_source='non_pri',
                           published=True)

    maestro_file_contents = ld_api_client.export_to_maestro(live_report_id=live_report_id)
    assert len(maestro_file_contents) != 0
