def verify_lr_in_project(ldclient, project_id, live_report_id):
    """
    Function to verify if a specific LR is present in the project

    :param ldclient: LDClient
    :param project_id: str, Project ID
    :param live_report_id: str, LiveReport ID
    """
    livereports = ldclient.live_reports(project_ids=[project_id])
    lr_ids = [lr.id for lr in livereports]
    assert live_report_id in lr_ids, \
        "Expected LiveReport ID '{}' to be present in project ID '{}'".format(live_report_id, project_id)


def verify_lr_not_in_project(ldclient, project_id, live_report_id):
    """
    Function to verify if a specific LR is not present in the project

    :param ldclient: LDClient
    :param project_id: str, Project ID
    :param live_report_id: str, LiveReport ID
    """
    livereports = ldclient.live_reports(project_ids=[project_id])
    lr_ids = [lr.id for lr in livereports]
    assert live_report_id not in lr_ids, \
        "Expected LiveReport ID '{}' to be not present in project ID '{}'".format(live_report_id, project_id)
