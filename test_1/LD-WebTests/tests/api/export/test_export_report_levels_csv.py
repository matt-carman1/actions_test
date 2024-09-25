from collections import OrderedDict

from helpers.api.actions import livereport, row, column, compound
from library.api.wait import wait_until_condition_met
from helpers.api.verification import file_contents

from ldclient.models import LiveReport, FreeformColumn, Observation
import pytest

entity_ids = ['V055812', 'V055813']
"""
    Existing EntityID-Lot-Salt triples in the starting data:
        V055812-C2-H2SO4 
        V055812-V-3HCl 
        V055812-V-chloride
        V055813-C2-HCl
        V055813-V-H2SO4
        
    All of them are added to the report when we add V055812 and V055813.
"""
compound_structure = {
    'V055812': 'CCCCC1=CC(CCCC)=CC=C1',
    'V055813': 'CCCCC1=CC(CCCC)=CC(CCC)=C1',
}
ffc_name = 'FFC1'
ffc_value = '123'
column_names = ["Compound Structure", "ID", "All IDs", ffc_name]


def populate_new_live_report(ld_client, live_report):
    """
    Populate new live report so that it looks as follows (in Compound mode):

    Compound Structure            ID(sort^)  All IDs    FFC1
    -------------------------------------------------------
    CCCCC1=CC(CCCC)=CC=C1         V055812    V055812    123
    CCCCC1=CC(CCCC)=CC(CCC)=C1    V055813    V055813    123

    :param ld_client: LD Client object
    :param live_report: object of a (newly created) LiveReport
    :return: Addable column ID of the new FFC
    """

    live_report_id = live_report.id
    project_id = live_report.project_id

    # Sort by ID column
    live_report.sorted_columns = [{'addable_column_id': '1226', 'ascending': True}]
    live_report = ld_client.update_live_report(live_report_id, live_report)

    # Hide Rationale and Lot Scientist
    column_ids_to_hide = ['1229', '28']
    for column_id in column_ids_to_hide:
        cd = ld_client.column_descriptor(live_report_id, column_id)
        cd.hidden = True
        ld_client.update_column_descriptor(live_report_id, cd)

    # Add entities
    row.add_rows_to_live_report(ld_client, live_report_id, entity_ids)

    # Create new FFC (with the same value for all entity IDs)
    ffc = column.create_freeform_column(ld_client, live_report, name=ffc_name)
    column.add_freeform_values(ld_client, [
        Observation(
            project_id=project_id,
            live_report_id=live_report_id,
            addable_column_id=ffc.id,
            entity_id=entity_id,
            value=ffc_value,
        ) for entity_id in entity_ids
    ])

    def check_ffc_values():
        lr_csv = livereport.get_live_report_as_csv(ld_client, live_report)
        rowlist = list(lr_csv)
        assert len(rowlist) == len(entity_ids)
        for lr_row in rowlist:
            assert (lr_row[ffc_name] == ffc_value)

    wait_until_condition_met(check_ffc_values)

    return ffc.id


def verify_export_correctness(selected_entity_ids, selected_column_names, entity_id_to_display_ids, bytes):
    """
    Verify that the exported CSV bytes match the expected values in the data table when exporting a subset of
    columns and entity_ids.

    Note that when exporting a subset of entity_ids, all rows that correspond to the selected entity_ids are exported
    (i.e. there might be multiple display_ids (and rows) presented for a given entity_id).

    :param selected_entity_ids: List of selected Entity IDs
    :param selected_column_names: List of selected Column names
    :param entity_id_to_display_ids: Dict. mapping Entity ID -> list of Display IDs
    :param bytes: Exported CSV (bytes)
    :return: None
    """
    # Override empty selected_entity_ids to mean that we export all entities
    if len(selected_entity_ids) == 0:
        selected_entity_ids = entity_id_to_display_ids.keys()

    # Override empty selected_column_names to mean that we export all columns
    if len(selected_column_names) == 0:
        selected_column_names = ["Compound Structure", "ID", "All IDs", ffc_name]

    expected_display_ids = sorted(
        [display_id for entity_id in selected_entity_ids for display_id in entity_id_to_display_ids[entity_id]])

    def get_entity_id(display_id):
        return display_id.split('-')[0]

    def get_structure(display_id):
        return compound_structure[get_entity_id(display_id)]

    def get_all_ids(display_id):
        return get_entity_id(display_id)

    def get_ffc_value(display_id):
        return ffc_value

    column_name_to_values = {
        "Compound Structure": [get_structure(display_id) for display_id in expected_display_ids],
        "ID": expected_display_ids,
        "All IDs": [get_all_ids(display_id) for display_id in expected_display_ids],
        ffc_name: [get_ffc_value(display_id) for display_id in expected_display_ids],
    }

    file_contents.verify_csv_contents(
        bytes,
        OrderedDict([(column_name, column_name_to_values[column_name]) for column_name in selected_column_names]))


test_type = 'api'


@pytest.mark.parametrize('report_level,entity_id_to_display_ids', [
    ('PARENT', {
        'V055812': ['V055812'],
        'V055813': ['V055813'],
    }),
    ('PARENT_BATCH', {
        'V055812': ['V055812-C2'],
        'V055813': ['V055813-C2'],
    }),
    ('PARENT_SALT', {
        'V055812': ['V055812-H2SO4', 'V055812-3HCl', 'V055812-chloride'],
        'V055813': ['V055813-HCl', 'V055813-H2SO4'],
    }),
    ('PARENT_BATCH_SALT', {
        'V055812': ['V055812-C2-H2SO4', 'V055812-V-3HCl', 'V055812-V-chloride'],
        'V055813': ['V055813-C2-HCl', 'V055813-V-H2SO4'],
    }),
])
@pytest.mark.parametrize(
    'selected_entity_ids,selected_column_names',
    [
        ([], []),  # () and ()
        ([], column_names[2:4]),  # () and (All IDs, FFC1)
        (entity_ids[0:1], []),  # (V055812) and ()
        (entity_ids[0:1], column_names[2:4]),  # (V055812) and (All IDs, FFC1)
        (entity_ids, column_names),  # (V055812, V055813) and (Compound Structure, ID, All IDs, FFC1)
    ])
@pytest.mark.app_defect(reason="SS-37664: Adding rows times out")
def test_export_subsets(ld_api_client, new_live_report, report_level, entity_id_to_display_ids, selected_entity_ids,
                        selected_column_names):
    """
    Confirm that correct column_ids and row_keys are exported in Compound, Lot, Salt, Lot-Salt, and Pose modes
    when exporting subsets of columns anr rows/

    :param ld_api_client: LDClient object (provided by Pytest fixture)
    :param new_live_report: New LiveReport (provided by Pytest fixture, is auto-deleted at the end)
    :param report_level: Report level (i.e. mode) to test
    :param entity_id_to_display_ids: Mapping EntityID -> list of DisplayIDs for this report_level
    """

    lr = new_live_report
    live_report_id = lr.id
    ffc_id = populate_new_live_report(ld_api_client, lr)

    # Set report_level (i.e. mode)
    lr = ld_api_client.live_report(live_report_id)
    lr.report_level = report_level
    ld_api_client.update_live_report(live_report_id, lr)
    ld_api_client.execute_live_report(live_report_id)

    column_name_to_column_id = {
        'Compound Structure': '1228',
        'ID': '1226',
        'All IDs': '1227',
        ffc_name: ffc_id,
    }

    selected_column_ids = [column_name_to_column_id[column_name] for column_name in selected_column_names]

    # Export
    bytes = livereport.export_live_report(ld_api_client,
                                          live_report_id,
                                          entity_ids=selected_entity_ids,
                                          column_ids=selected_column_ids)

    verify_export_correctness(selected_entity_ids, selected_column_names, entity_id_to_display_ids, bytes)
