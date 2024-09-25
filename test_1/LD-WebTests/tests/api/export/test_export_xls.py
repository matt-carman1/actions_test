from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import pytest

from helpers.api.actions.livereport import export_live_report
from tests.conftest import get_api_client

from .testing_data import highlighted_substructure_image_detail_list, scaffold_image_detail_list, \
    rgroup_image_detail_list

live_report_id = '886'
visible_columns_in_lr = [
    'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'PK_PO_RAT (AUC) [uM]',
    'PK_PO_RAT (Absorption) [uM]', 'DRC TEST ASSAY (IC50%) [uM]', 'Test RPE Formula', 'Test RPE MPO',
    'CorpID String (CorpID String)'
]


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_compound_image(username, password):
    """
    test batch compound image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    entity_ids = ['V055682', 'V055683', 'V055685', 'V055691']
    user_client = get_api_client(username=username, password=password)
    zipped_compound_images = user_client.get_batch_compound_images(entity_ids, 200, 100, "PNG", "FFFFFF00", [])
    file_names = [file.filename for file in ZipFile(BytesIO(zipped_compound_images)).filelist]
    assert len(file_names) == 4
    assert file_names == entity_ids


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_compound_image_for_incorrect_id(username, password):
    """
    test batch compound image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    entity_ids = ['V055682', 'V055683', 'V055685', 'RandomID']
    user_client = get_api_client(username=username, password=password)
    zipped_compound_images = user_client.get_batch_compound_images(entity_ids, 200, 100, "PNG", "FFFFFF00", [])
    file_names = [file.filename for file in ZipFile(BytesIO(zipped_compound_images)).filelist]
    assert len(file_names) == 3
    for file_name in file_names:
        assert file_name in entity_ids


# Note: Modified the rgroup_image_detail_list as the CRA-035513
#       doesn't generate rgroup image on New Jenkins builds
#       Until that is fixed, this test will only validate for CRA-035517
@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_rgroup_image(username, password):
    """
    test batch rgroup image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    user_client.execute_live_report(live_report_id)
    zipped_rgroup_images = user_client.get_batch_rgroup_image(rgroup_image_detail_list=rgroup_image_detail_list,
                                                              width=200,
                                                              height=100,
                                                              format="PNG",
                                                              bgcolor="FFFFFF00")

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_rgroup_images)).filelist]
    assert len(file_names) == 3
    for i in range(3):
        assert file_names[
            i] == rgroup_image_detail_list[i]['entity_id'] + "$$#$$" + rgroup_image_detail_list[i]['column_id']


# Note: Modified the rgroup_image_detail_list as the CRA-035513
#       doesn't generate rgroup images on New Jenkins builds
#       Until that is fixed, this test will only validate for CRA-035517
@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_rgroup_image_for_incorrect_entity_id(username, password):
    """
    test batch rgroup image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    user_client.execute_live_report(live_report_id)

    rgroup_image_detail_list_with_incorrect_entity_id = [image_detail for image_detail in rgroup_image_detail_list]
    rgroup_image_detail_list_with_incorrect_entity_id[0]["entity_id"] = "random value"
    zipped_rgroup_images = user_client.get_batch_rgroup_image(
        rgroup_image_detail_list=rgroup_image_detail_list_with_incorrect_entity_id,
        width=200,
        height=100,
        format="PNG",
        bgcolor="FFFFFF")

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_rgroup_images)).filelist]
    assert len(file_names) == 2
    for i in range(1, 3):
        file_name = rgroup_image_detail_list[i]['entity_id'] + "$$#$$" + rgroup_image_detail_list[i]['column_id']
        assert file_name in file_names


# Note: Modified the rgroup_image_detail_list as the CRA-035513
#       doesn't generate rgroup images on New Jenkins builds
#       Until that is fixed, this test will only validate for CRA-035517
@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_rgroup_image_for_invalid_image_detail(username, password):
    """
    test batch rgroup image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    user_client.execute_live_report(live_report_id)
    rgroup_image_detail_list_with_image_detail = [
        {key: value for key, value in rgroup_image.items()} for rgroup_image in rgroup_image_detail_list
    ]
    del rgroup_image_detail_list_with_image_detail[0]["entity_id"]
    zipped_rgroup_images = user_client.get_batch_rgroup_image(
        rgroup_image_detail_list=rgroup_image_detail_list_with_image_detail,
        width=200,
        height=100,
        format="PNG",
        bgcolor="FFFFFF")

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_rgroup_images)).filelist]
    assert len(file_names) == 2
    for i in range(1, 3):
        file_name = rgroup_image_detail_list[i]['entity_id'] + "$$#$$" + rgroup_image_detail_list[i]['column_id']
        assert file_name in file_names


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_scaffold_image(username, password):
    """
    test batch scaffold image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)

    zipped_scaffold_images = user_client.get_batch_scaffold_image(scaffold_image_detail_list=scaffold_image_detail_list,
                                                                  width=200,
                                                                  height=100,
                                                                  fmt="PNG",
                                                                  bgcolor="FFFFFF00",
                                                                  scaffold_batch_request_type='SCAFFOLD_ID')

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_scaffold_images)).filelist]
    assert len(file_names) == 4
    for i in range(4):
        assert file_names[i] == scaffold_image_detail_list[i]['row_key'] + "$$#$$" + scaffold_image_detail_list[i][
            'scaffold_column_name']


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_scaffold_image_for_incorrect_scaffold_id(username, password):
    """
    test batch scaffold image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)

    partially_scaffold_image_detail_list = [image_detail for image_detail in scaffold_image_detail_list]
    partially_scaffold_image_detail_list[0]["scaffold_id"] = 9000
    zipped_scaffold_images = user_client.get_batch_scaffold_image(scaffold_image_detail_list=scaffold_image_detail_list,
                                                                  width=200,
                                                                  height=100,
                                                                  fmt="PNG",
                                                                  bgcolor="FFFFFF00",
                                                                  scaffold_batch_request_type='SCAFFOLD_ID')

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_scaffold_images)).filelist]
    assert len(file_names) == 3
    for i in range(1, 4):
        file_name = scaffold_image_detail_list[i]['row_key'] + "$$#$$" + scaffold_image_detail_list[i][
            'scaffold_column_name']
        assert file_name in file_names


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_misc_image(username, password):
    """
    test batch image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    image_id_list = ["0068a21f-6e10-4dea-a6a9-6450b3754cc4"]

    zipped_images = user_client.get_batch_misc_images(image_id_list)

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_images)).filelist]
    assert len(file_names) == 1
    assert file_names[0] == image_id_list[0]


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_misc_image_with_incorrect_id(username, password):
    """
    test batch image api

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    image_id_list = ["0068a21f-6e10-4dea-a6a9-6450b3754cc4", "lkjmnhbgvf"]

    zipped_images = user_client.get_batch_misc_images(image_id_list)

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_images)).filelist]
    assert len(file_names) == 1
    assert file_names[0] == image_id_list[0]


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_highlighted_substructure_image(username, password):
    """
    test batch highlighted substructure image api
    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    zipped_highlighted_substructure_images = user_client.get_batch_highlighted_substructure_compound_images(
        highlighted_substructure_image_detail_list=highlighted_substructure_image_detail_list,
        width=200,
        height=100,
        format="PNG",
        bgcolor="FFFFFF00")

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_highlighted_substructure_images)).filelist]
    assert len(file_names) == 4
    for i in range(4):
        assert file_names[i] == highlighted_substructure_image_detail_list[i][
            'entity_id'] + "$$#$$" + highlighted_substructure_image_detail_list[i]['column_id']


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_highlighted_substructure_image_with_one_incorrect_param(username, password):
    """
    test batch highlighted substructure image api for the case where we are not getting all the images
    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    partially_incorrect_list = [image_detail for image_detail in highlighted_substructure_image_detail_list]
    partially_incorrect_list[3]["entity_id"] = "Incorrect id"
    zipped_highlighted_substructure_images = user_client.get_batch_highlighted_substructure_compound_images(
        highlighted_substructure_image_detail_list=partially_incorrect_list,
        width=200,
        height=100,
        format="PNG",
        bgcolor="FFFFFF00")

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_highlighted_substructure_images)).filelist]
    assert len(file_names) == 3
    for i in range(3):
        assert file_names[i] == highlighted_substructure_image_detail_list[i][
            'entity_id'] + "$$#$$" + highlighted_substructure_image_detail_list[i]['column_id']


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_get_batch_highlighted_substructure_image_with_empty_data_list(username, password):
    """
    test batch highlighted substructure image api in case image detail list is empty

    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)

    zipped_highlighted_substructure_images = user_client.get_batch_highlighted_substructure_compound_images(
        highlighted_substructure_image_detail_list=[], width=200, height=100, format="PNG", bgcolor="FFFFFF00")

    file_names = [file.filename for file in ZipFile(BytesIO(zipped_highlighted_substructure_images)).filelist]
    assert len(file_names) == 0


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_exported_rows_complete_live_report(username, password):
    """
    Export an entire LiveReport to xls as admin and non-admin user and verify exported xls contents.
    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    user_client.execute_live_report(live_report_id)
    enable_xls_image_generations()
    exported_live_report = export_live_report(user_client, live_report_id, export_type="xls")
    df = pd.read_excel(exported_live_report)
    assert df.shape[0] == 101


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_exported_rows_partial_live_report(username, password):
    """
    Export an entire LiveReport to xls as admin and non-admin user and verify exported xls contents.
    :param username: str, Username to get the ldclient
    :param password: str, Password to get the ldclient
    """
    user_client = get_api_client(username=username, password=password)
    user_client.execute_live_report(live_report_id)
    enable_xls_image_generations()
    entity_ids = ["CRA-035517", "CRA-035526", "CRA-035531", "CRA-035574", "CRA-035509", "CRA-035511"]
    exported_live_report = export_live_report(user_client, live_report_id, export_type="xls", entity_ids=entity_ids)
    df = pd.read_excel(exported_live_report)
    assert df.shape[0] == len(entity_ids)


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_export_of_smiles_string_image_generation_enabled(username, password):
    user_client = get_api_client(username=username, password=password)
    user_client.execute_live_report(live_report_id)
    enable_xls_image_generations()
    exported_live_report = export_live_report(user_client, live_report_id, export_type="xls")
    df = pd.read_excel(exported_live_report)
    for i in range(df.shape[0]):
        assert df.iloc[i]['SMILES'] != None
    disable_xls_image_generations()


@pytest.mark.parametrize("username, password", [('demo', 'demo'), ('userB', 'userB')])
def test_export_of_smiles_string_image_generation_disabled(username, password):
    user_client = get_api_client(username=username, password=password)
    user_client.execute_live_report(live_report_id)
    disable_xls_image_generations()
    exported_live_report = export_live_report(user_client, live_report_id, export_type="xls")
    df = pd.read_excel(exported_live_report)
    for i in range(df.shape[0]):
        assert df.iloc[i]['SMILES'] != None


def enable_xls_image_generations():
    user_client = get_api_client(username="demo", password="demo")
    properties = {"ENABLE_XLS_IMAGE_GENERATION": True}
    user_client.update_properties(properties)


def disable_xls_image_generations():
    user_client = get_api_client(username="demo", password="demo")
    properties = {"ENABLE_XLS_IMAGE_GENERATION": False}
    user_client.update_properties(properties)
