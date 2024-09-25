from ldclient import LDClient

from helpers.api.actions.livereport import execute_live_report


def get_live_report_column_ids(ld_client: LDClient, live_report_id):
    """
    Get the column ids present in livereport

    :param ld_client: LDClient, ldclient object
    :param live_report_id:str, id of the live report

    :return: list, list of column ids
    """
    columns = ld_client.live_report_results_metadata(live_report_id).get('columns')
    return list(columns.keys())


def get_column_ids_by_name(ldclient, lr_id, column_names):
    """
    Function to get the addable column ids by passing column names
    Note: Useful while retrieving the unpublished columns id in duplicated LR using column name.

    :param ldclient: LDClient object
    :param lr_id: str, LiveReport ID
    :param column_names: list of str, List of column names

    :return: list, List of column ids for the column names passed in the same order.
    """
    lr_column_desc = ldclient.column_descriptors(live_report_id=lr_id)
    column_ids = []
    for col_desc in lr_column_desc:
        if col_desc.display_name in column_names:
            column_ids.append(col_desc.addable_column_id)
    return column_ids


def get_column_descriptor(ld_client, lr_id, column_id):
    """
    Get column descriptor for the column in the livereport.

    :param ld_client: LDClient, ldclient object
    :param lr_id: str, live report id
    :param column_id: id of the addable column

    :rtype: :class:`models.ColumnDescriptor`
    :return: column descriptor object for mentioned column id,
            ex: ColumnDescriptor(column_id='1', addable_column_id='', active_mpo_id_for_coloring=, live_report_id='123',
            display_name='name', width='2', color_styles='', filters='', hidden=True, aggregation_type='', id='12')
    """
    return ld_client.column_descriptor(lr_id, addable_column_id=column_id)


def get_live_report_column_names(ld_client, live_report_id):
    """
    Function to get column names present in a live report

    :param ld_client : ldclient object
    :param live_report_id : str, id of the Live Report
    """
    columns = ld_client.live_report_results_metadata(live_report_id).get('columns')
    column_metadata = list(columns.values())
    column_names = [column['name'] for column in column_metadata]
    return column_names


def get_live_report_compound_ids(ld_client, live_report_id):
    """
    Function to get compound id's present in live report

    :param ld_client : ldclient object
    :param live_report_id : str, id of the Live Report
    :return : list, List of all compounds ids present in Live report
    """
    response = execute_live_report(ld_client, live_report_id)
    compound_ids = list(response['rows'].keys())
    return compound_ids
