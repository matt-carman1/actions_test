from library.utils import make_unique_name

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': 2048}
test_type = 'api'


def test_rename_live_report(ld_client, duplicate_live_report):
    """
    Test rename a live report.
    1. Duplicate any livereport using duplicate_live_report fixture
    2. Update name of the Livereport object using: duplicate_live_report.title = 'new name'
    3. Use this method to rename the lr : update_live_report(duplicate_live_report.id, duplicate_live_report)
    4. Verify whether the livereport name changed properly from the live_report() method

    :param ld_client: LDClient
    :param duplicate_live_report: fixture which duplicates livereport
    """
    # Update name of the Livereport object using: duplicate_live_report.title = 'new name'
    new_lr_name = make_unique_name('new_lr_name')
    duplicate_live_report.title = new_lr_name

    # Use this method to rename the lr : update_live_report(duplicate_live_report.id, duplicate_live_report)
    ld_client.update_live_report(duplicate_live_report.id, duplicate_live_report)

    # Verify whether the livereport name changed properly from the live_report() method.
    name = ld_client.live_report(duplicate_live_report.id).title
    assert name == new_lr_name
