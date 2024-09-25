from helpers.api.extraction.livereport import get_column_descriptor
from helpers.api.actions.color import apply_coloring_rule

live_report_to_duplicate = {'livereport_name': 'Test Date Assay Column', 'livereport_id': '2699'}
test_type = 'api'


def test_add_date_coloring_rules(ld_client, duplicate_live_report):
    """
    API test to check coloring rules for date column

    1. Apply Coloring rules with Range query
    2. Apply Coloring rules Range query with log scale
    3. Apply coloring rule with Categorical query
    4. Clear all Coloring rules

    :param ld_client: LDClient, ldclient object
    :param duplicate_live_report: fixture which duplicates livereport
    """
    # addable column id for 'Test Dates Assay (date)' column
    date_column_id = '83201'
    live_report_id = duplicate_live_report.id

    # getting column descriptor for the date column
    initial_column_descriptor = get_column_descriptor(ld_client, live_report_id, date_column_id)

    # set color styles with range query
    range_color_style = [{
        'color_low': '#999999',
        'color_high': '#FF99FF',
        'matching_string': None,
        'matching_strings_list': None,
        'range_low': None,
        'value_low': 1230768000000.0,
        'log_scale': False,
        'range_high': None,
        'value_high': 1546365600000.0,
        'color_style_type': 'DATE',
        'relative': False
    }]
    # applying color styles to the column
    updated_column_descr_after_range_coloring_rule = apply_coloring_rule(ld_client, live_report_id,
                                                                         initial_column_descriptor, range_color_style)

    # verify color added
    assert updated_column_descr_after_range_coloring_rule.color_styles == range_color_style, \
        "Color styles format does not match for addable_col_id {}".format(date_column_id)

    # set color styles range query with log scale
    range_log_color_style = [{
        'color_low': '#3366FF',
        'color_high': '#CC9933',
        'matching_string': None,
        'matching_strings_list': None,
        'range_low': 1228867200000.0,
        'value_low': 1230768000000.0,
        'log_scale': True,
        'range_high': 1552348800000.0,
        'value_high': 1546365600000.0,
        'color_style_type': 'DATE',
        'relative': False
    }]
    # applying color styles to the column
    updated_column_descr_after_log_coloring_rule = apply_coloring_rule(ld_client, live_report_id,
                                                                       initial_column_descriptor, range_log_color_style)

    # verify color added
    assert updated_column_descr_after_log_coloring_rule.color_styles == range_log_color_style, \
        "Color styles format does not match for addable_col_id {}".format(date_column_id)

    # set color style with categorical query
    categorical_color_style1 = {
        'color_low': '#336666',
        'color_high': None,
        'matching_string': '"2009-01-01"|"2019-01-01 18:00:00"',
        'matching_strings_list': ['2009-01-01', '2019-01-01 18:00:00'],
        'range_low': None,
        'value_low': 1230768000000.0,
        'log_scale': False,
        'range_high': None,
        'value_high': 1546365600000.0,
        'color_style_type': 'CATEGORICAL',
        'relative': False
    }
    categorical_color_style2 = {
        'color_low': '#FF9900',
        'color_high': None,
        'matching_string': '"2009-02-01 16:00:00"|"2019-01-01"',
        'matching_strings_list': ['2009-02-01 16:00:00', '2019-01-01'],
        'range_low': None,
        'value_low': 1230768000000.0,
        'log_scale': False,
        'range_high': None,
        'value_high': 1546365600000.0,
        'color_style_type': 'CATEGORICAL',
        'relative': False
    }
    # applying color styles to the column
    updated_column_descr_after_categorical_coloring_rule = apply_coloring_rule(
        ld_client, live_report_id, initial_column_descriptor, [categorical_color_style1, categorical_color_style2])

    # verify color added
    assert updated_column_descr_after_categorical_coloring_rule.color_styles == [
        categorical_color_style1, categorical_color_style2
    ], "Color styles format does not match for addable_col_id {}".format(date_column_id)

    # clear all coloring rule and verify
    updated_column_descr_after_clearing_coloring_rule = apply_coloring_rule(ld_client, live_report_id,
                                                                            initial_column_descriptor)
    assert updated_column_descr_after_clearing_coloring_rule.color_styles == [], \
        "Color styles format does not match for addable_col_id {}".format(date_column_id)
