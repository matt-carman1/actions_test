from library import dom
from helpers.change.actions_pane import open_notification_panel
from helpers.selection.audit_log import AUDIT_LOG_DATE, AUDIT_LOG_ITEM
from helpers.verification.element import verify_is_not_visible


def verify_audit_log_count(driver, count):
    """
    Checks the audit log count

    :param driver: Webdriver
    :param count: number, number of expected audit log items
    :return:
    """

    open_notification_panel(driver)
    if count == 0:
        verify_is_not_visible(driver, AUDIT_LOG_ITEM)
    else:
        audit_logs = dom.get_elements(driver, AUDIT_LOG_ITEM, dont_raise=True)
        num_audit_logs = len(audit_logs)
        message = 'There should only be {} audit log item(s) but there were {}.'.format(count, num_audit_logs)
        assert count == num_audit_logs, message


def verify_audit_log_dates(driver, *expected_dates):
    """
    Verifies dates shown in the audit log match expected_dates provided

    :param driver: webdriver
    :param expected_dates: str, audit log dates expected to be found.
                                Can specify multiple arguments if there is more than 1 expected date:

                                    verify_audit_log_dates(selenium, "TODAY", "01/03/2018")

    """
    # gets all audit log dates
    audit_log_dates = {date_elem.text for date_elem in dom.get_elements(driver, AUDIT_LOG_DATE)}
    # checks if expected dates have been found. Keeps track of unexpected dates found.
    unexpected_dates = []
    for actual_date in audit_log_dates:
        if actual_date not in expected_dates:
            unexpected_dates.append(actual_date)

    # if unexpected dates are found, prints the list of unexpected dates
    assert not unexpected_dates, \
        "Unexpected log dates found: `{}` \nExpecting only dates: `{}`".format(unexpected_dates, expected_dates)
