highlighted_substructure_image_detail_list = [{
    "entity_id": "CRA-035526",
    "column_id": "84851"
}, {
    "entity_id": "CRA-035531",
    "column_id": "84851"
}, {
    "entity_id": "CRA-035574",
    "column_id": "84851"
}, {
    "entity_id": "CRA-035509",
    "column_id": "84851"
}]

scaffold_image_detail_list = [{
    'row_key': 'CRA-035513',
    'scaffold_column_name': '1230',
    'scaffold_id': '9'
}, {
    'row_key': 'CRA-035517',
    'scaffold_column_name': '1230',
    'scaffold_id': '9'
}, {
    'row_key': 'CRA-035526',
    'scaffold_column_name': '1230',
    'scaffold_id': '9'
}, {
    'row_key': 'CRA-035531',
    'scaffold_column_name': '1230',
    'scaffold_id': '9'
}]

# Note: Removing the entity_id: CRA-035513 from the list to fix SS-39924.
#       CRA-035513 compound is not matching with the scaffold_id: 9 as result not displaying the R-group images
#       Added R3 (SAR) column to the list for CRA-035517 to test R3 (SAR) column image as well
rgroup_image_detail_list = [{
    'entity_id': 'CRA-035517',
    'scaffold_id': '9',
    'column_header': 'R1 (SAR)',
    'column_id': '1233'
}, {
    'entity_id': 'CRA-035517',
    'scaffold_id': '9',
    'column_header': 'R2 (SAR)',
    'column_id': '1234'
}, {
    'entity_id': 'CRA-035517',
    'scaffold_id': '9',
    'column_header': 'R3 (SAR)',
    'column_id': '1235'
}]
