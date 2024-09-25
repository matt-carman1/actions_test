import time


def get_cell_values_for_rows_and_columns(ldclient, livereport_id, column_ids, row_ids):
    """
    Function to retrieve cell values for specific rows and specific columns from an LR

    :param ldclient: LDClient, ldclient object
    :param livereport_id: str, Livereport ID
    :param column_ids: List(str), list of addable column ids
    :param row_ids: List(str), list of row ids
    :return: dict, dictionary with row_id:list of column_values pairs
    """
    actual_cell_values = {}

    # extra execute to process lazy events
    ldclient.execute_live_report(live_report_id=livereport_id)
    time.sleep(3)
    livereport_data = ldclient.execute_live_report(live_report_id=livereport_id)['rows']
    for row_id in row_ids:
        row_data = livereport_data[row_id]
        cell_values = []
        for column_id in column_ids:
            cell_data = row_data['cells'][column_id]['values']
            if len(cell_data) > 1:
                cell_values.append([item['value'] for item in cell_data])
            elif len(cell_data) == 1:
                cell_values.append(cell_data[0]['value'])
            else:
                cell_values.append('')
        actual_cell_values[row_id] = cell_values
    return actual_cell_values
