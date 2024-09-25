import pytest
from ldclient.models import User
from library.utils import is_k8s

from helpers.api.extraction.user import get_users_list

test_username = 'seurat'
test_password = 'seurat'


@pytest.mark.app_defect(reason='SS-33239')
def test_list_users(ld_api_client):
    """
    Test to list users
    1. List users with including permissions.
    2. list users without including permissions.

    :param ld_api_client: LDClient, ldclient object
    """
    # ------ list users with including permissions ----- #
    users = get_users_list(ld_api_client)
    # validating permission columns not present when include_permissions false
    assert not {'can_build_protocols', 'is_admin', 'is_project_admin', 'can_use_admin_panel'}.issubset(
        users[0].keys()), "Permission fields included with include_permissions false"

    expected_user_names = ['commaDecimalUser', 'demo', 'seurat', 'userA', 'userB', 'userC']

    # validating usernames
    actual_user_names = [user['username'] for user in users]
    actual_user_names.sort()
    assert expected_user_names == actual_user_names, \
        "Expected Usernames:{}, But got:{}".format(expected_user_names, actual_user_names)

    users_with_permissions = get_users_list(ld_api_client, include_permissions=True)
    # validating permission columns present when include_permissions true
    assert {'can_build_protocols', 'is_admin', 'is_project_admin', 'can_use_admin_panel'}.issubset(
        users_with_permissions[0].keys()), "Permission fields not included with include_permissions set to true"
    # validating user names
    actual_user_names = [user['username'] for user in users_with_permissions]
    actual_user_names.sort()
    assert expected_user_names == actual_user_names, \
        "Expected Usernames:{}, But got:{}".format(expected_user_names, actual_user_names)


@pytest.mark.xfail(not is_k8s(), reason="SS-43040: Old data dump in old jenkins causes test to fail")
@pytest.mark.k8s_defect(reason='SS-37881 AssertionError: id value not matched1')
def test_current_user(ld_api_client):
    """
    Test current user previliges

    :param ld_api_client: LDClient, ldclient object
    """
    user_privileges = ld_api_client.get_privileges()
    expected_user_privileges = User(id='76592',
                                    username='seurat',
                                    decimal_separator='.',
                                    can_build_protocols=True,
                                    is_admin=True,
                                    is_user_admin=True,
                                    license_type="DESIGN",
                                    is_project_admin=True,
                                    can_use_admin_panel=True,
                                    administered_project_ids=[]).as_dict()
    verify_user_details(expected_user_privileges, user_privileges)


def test_get_user(ld_api_client):
    """
    Test get_user method.

    :param ld_api_client: LDClient, ldclient object
    """
    user = ld_api_client.get_user("commaDecimalUser")
    expected_user = User(id='76492',
                         username='commaDecimalUser',
                         decimal_separator=',',
                         can_build_protocols=False,
                         is_admin=False,
                         is_user_admin=False,
                         license_type="DESIGN",
                         is_project_admin=False,
                         can_use_admin_panel=True,
                         administered_project_ids=[]).as_dict()
    verify_user_details(expected_user, user)


def test_list_memberships(ld_api_client):
    """
    Test list_memberships and validate whether memberships are proper

    :param ld_api_client: LDClient, ldclient object
    """
    memberships = ld_api_client.list_memberships()
    assert {'user_id',
            'group_id'}.issubset(memberships[0].keys()), "user_id or group_id is not there in the membership keys."

    # Mapping user ids with group
    group_user_dict = map_group_ids_with_project_or_users(memberships, 'user_id')

    # validating whether TestGroupBC group has 'commaDecimalUser', 'userC' and 'userB'
    testgroupbc_group_id = '76443'
    expected_user_list = ['76492', '76439', '76440']

    assert group_user_dict[testgroupbc_group_id] == expected_user_list, \
        "Users not mapped correctly for group. Actual users: {}, Expected users:{} for group:{}".format(
            group_user_dict[testgroupbc_group_id], expected_user_list, testgroupbc_group_id)

    # validating whether TestGroupAB group has 'userA' and 'userB'
    testgroupab_group_id = '76442'
    expected_user_list = ['76441', '76439']

    assert group_user_dict[testgroupab_group_id] == expected_user_list, \
        "Users not mapped correctly for group. Actual users: {}, Expected users:{} for group:{}".format(
            group_user_dict[testgroupab_group_id], expected_user_list, testgroupab_group_id)


def test_list_permissions(ld_api_client):
    """
    Test list_permissions and validate permissions are properly mapped.

    :param ld_api_client: LDClient, ldclient object
    """
    permissions = ld_api_client.list_permissions()
    group_project_mapping = map_group_ids_with_project_or_users(permissions, 'project_id')
    # validating whether group_id, project_id keys present in permission dictionary
    assert {'group_id',
            'project_id'}.issubset(permissions[0].keys()), "group_id or project_id is not there in the permission keys."

    # validating whether TestGroupBC group has 'JS Testing' and 'RestrictedBC' projects
    testgroupbc_group_id = '76443'
    expected_project_ids = ['4', '7']
    group_project_mapping[testgroupbc_group_id] = sorted(group_project_mapping[testgroupbc_group_id], key=int)
    expected_project_ids = sorted(expected_project_ids, key=int)
    assert group_project_mapping[testgroupbc_group_id] == expected_project_ids, \
        "Projects not mapped correctly for group. Actual projects: {}, Expected projects:{} for group:{}".format(
            group_project_mapping[testgroupbc_group_id], expected_project_ids, testgroupbc_group_id)

    # validating whether TestGroupAB group has 'RestrictedAB' project
    testgroupab_group_id = '76442'
    expected_project_ids = ['6']
    assert group_project_mapping[testgroupab_group_id] == expected_project_ids, \
        "Projects not mapped correctly for group. Actual projects: {}, Expected projects:{} for group:{}".format(
            group_project_mapping[testgroupab_group_id], expected_project_ids, testgroupab_group_id)


def verify_user_details(expected_user_details, actual_user_details):
    """
    Validates user details.

    :param expected_user_details: dict, Expected user details dictionary
    :param actual_user_details: dict, Actual user details dictionary
    """
    # validating user details
    for field in expected_user_details.keys():
        # not verifying last_login as this will change based on time of login
        # and plexus_visible since it is now deprecated
        if field == 'last_login' or field == 'plexus_visible':
            continue
        expected_value = expected_user_details[field]
        actual_value = actual_user_details[field]
        assert expected_value == actual_value, \
            "{} value not matched. Expected value:{}, but got:{}".format(field, expected_value, actual_value)


def map_group_ids_with_project_or_users(individual_mapping_list, key):
    """
    Creates the dictionary of group,user or group,project.

    :param individual_mapping_list: list, dictionaries list which contains individual group-user/group-project mapping
    :param key: str, project_id if you want to map group with project, user_id for mapping group with user.
    """
    mapped_dictionary = {}
    for member in individual_mapping_list:
        # getting group id
        group_id = member['group_id']
        if group_id in mapped_dictionary:
            # updating dictionary when key matches with group id
            li = mapped_dictionary.get(group_id)
            li.append(member[key])
            mapped_dictionary[group_id] = li
        else:
            # assigning user with group
            mapped_dictionary[group_id] = [member[key]]
    return mapped_dictionary
