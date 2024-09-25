from helpers.api.actions.livereport import update_live_report
from helpers.api.verification.general import verify_error_response
import pytest

test_type = 'api'
# Creating an LR under folder 'MPO'
test_report_folder = ['124781']


def test_move_lr_between_folders(ld_api_client, new_live_report):
    """
    Test moving an new LR in between folders.
    1. Create a new LR under a folder (preferably not the default folder)
    2. Use the LR tag and update the LR, which moves the LR to the new folder.
    3. Verify the same.
    4. Move an LR to multiple folders and verify the same
    4. Check it returns an error with an incorrect folder tag

    :param ld_api_client: LDClient
    :param new_live_report: Fixture for creating a new Livereport
    """
    adv_search_folder_id = ["124731"]
    materials_science_test_sorting_folder_id = ["124931", "124881"]

    # Moving the LR to a different folder (Adv Search - id 124731) using the update_live_report method.
    new_live_report.tags = adv_search_folder_id
    moved_lr_obj = update_live_report(ld_api_client, new_live_report.id, new_live_report)

    assert moved_lr_obj.tags == adv_search_folder_id, \
        "The LR with id {} has not been moved".format(new_live_report.id)

    # Moving an LR to multiple folder (Materials Science - id 124931, Test Sorting, id = 124881)
    new_live_report.tags = sorted(materials_science_test_sorting_folder_id)
    multiple_tags_lr_obj = update_live_report(ld_api_client, new_live_report.id, new_live_report)

    assert multiple_tags_lr_obj.tags == sorted(materials_science_test_sorting_folder_id), \
        "The LR with id {} has not been moved".format(new_live_report.id)

    with pytest.raises(Exception) as error_response:
        new_live_report.tags = ["1"]
        update_live_report(ld_api_client, new_live_report.id, new_live_report)

    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message='The specified tag '
                          'does not exist.')

    with pytest.raises(Exception) as error_response:
        new_live_report.tags = ["fake_tag"]
        update_live_report(ld_api_client, new_live_report.id, new_live_report)

    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message='The input was valid '
                          'JSON but there was a missing field or incorrect value')
