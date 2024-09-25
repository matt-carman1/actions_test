from helpers.selection.freeform_columns import FreeformColumnDialog
from library import dom


def verify_users_on_read_only_ffc_allowlist(driver, expected_checked_users):
    """
    Function to verify if the users on expected_checked_users list are checked/selected on the read-only FFC allowlist
    :param driver: Webdriver
    :param expected_checked_users: list, list of users expected to be checked on the allowlist
    :return:
    """
    # Verify expected users are checked on the allowlist
    allowlist_checked_elems = dom.get_elements(driver, FreeformColumnDialog.FFC_READ_ONLY_ALLOWLIST_CHECKED_VALUE)
    allowlist_checked_users = [dom.get_parent_element(elem).text for elem in allowlist_checked_elems]
    assert set(allowlist_checked_users) == set(expected_checked_users), \
        'Expected users {} to be checked on the allowlist, actual users {} checked'.format(expected_checked_users,
                                                                                           allowlist_checked_users)


def verify_disabled_creator_user_on_read_only_ffc_allowlist(driver, ffc_creator):
    """
    Function to verify if the ffc_creator is checked and disabled by default on the read-only FFC allowlist
    :param driver: Webdriver
    :param ffc_creator: str, FFC creator user whose name should be disabled by default
    :return:
    """
    # Verify FFC creator username is checked and disabled on the allowlist
    allowlist_disabled_elem = dom.get_element(driver, FreeformColumnDialog.FFC_READ_ONLY_ALLOWLIST_DISABLED_VALUE)
    actual_disabled_user = dom.get_parent_element(allowlist_disabled_elem).text
    assert actual_disabled_user == ffc_creator, \
        'Expected FFC creator user "{}" to be disabled on the allowlist,' \
        ' actual disabled user "{}"'.format(ffc_creator, actual_disabled_user)
