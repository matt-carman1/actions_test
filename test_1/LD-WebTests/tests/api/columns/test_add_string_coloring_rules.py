from helpers.api.extraction.livereport import get_column_descriptor
from helpers.api.actions.color import apply_coloring_rule

live_report_to_duplicate = {'livereport_name': 'Coloring Rules', 'livereport_id': '879'}
test_type = 'api'


def test_add_string_coloring_rules(ld_client, duplicate_live_report):
    """
    API test to apply and verify coloring rules to a string type (categorical) column

    :param ld_client: LDClient, ldclient object
    :param duplicate_live_report: fixture which duplicates livereport
    """
    # addable column id for 'Author (undefined)' column
    categorical_column_id = '834'
    live_report_id = duplicate_live_report.id

    # getting column descriptor of the column
    initial_column_descriptor = get_column_descriptor(ld_client, live_report_id, categorical_column_id)

    # color style for a single entry
    single_color = {
        'color_low': '#33FF33',
        'color_high': None,
        'matching_string': '"bob"',
        'matching_strings_list': ['bob'],
        'range_low': None,
        'value_low': None,
        'log_scale': False,
        'range_high': None,
        'value_high': None,
        'color_style_type': 'CATEGORICAL',
        'relative': False
    }
    # same color styles for multiple entries
    multiple_color = {
        'color_low': '#FFFF99',
        'color_high': None,
        'matching_string': '"Mike"|"John"',
        'matching_strings_list': ['Mike', 'John'],
        'range_low': None,
        'value_low': None,
        'log_scale': False,
        'range_high': None,
        'value_high': None,
        'color_style_type': 'CATEGORICAL',
        'relative': False
    }
    # applying color styles to the column
    updated_column_descr_after_coloring_rule = apply_coloring_rule(ld_client, live_report_id, initial_column_descriptor,
                                                                   [single_color, multiple_color])

    # verify color added
    assert updated_column_descr_after_coloring_rule.color_styles == [single_color, multiple_color], \
        "Color styles format does not match for addable_col_id {}".format(categorical_column_id)

    # clear all coloring rule
    updated_column_descr_after_clearing_coloring_rule = apply_coloring_rule(ld_client, live_report_id,
                                                                            initial_column_descriptor)

    # verify color styles cleared
    assert updated_column_descr_after_clearing_coloring_rule.color_styles == [], \
        "Color styles format does not match for addable_col_id {}".format(categorical_column_id)
