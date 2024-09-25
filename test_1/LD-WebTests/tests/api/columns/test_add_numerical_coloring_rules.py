from helpers.api.actions.color import apply_coloring_rule
from helpers.api.extraction.livereport import get_column_descriptor

live_report_to_duplicate = {'livereport_name': 'Coloring Rules', 'livereport_id': '879'}
test_type = 'api'


def test_add_numerical_coloring_rules(ld_client, duplicate_live_report):
    """
    API test to apply and verify coloring rules to a numerical column by

    1. Applying rules in range
    2. Applying rules in range with log scale
    3. Applying rules in categorical
    4. Clear all coloring rules
    :param ld_client: LDClient, ldclient object
    :param duplicate_live_report: fixture which duplicates livereport
    """
    # addable column id for 'CR GScore (undefined)' column
    numeric_column_id = '835'
    live_report_id = duplicate_live_report.id

    # getting column descriptor for the numeric column
    initial_column_descriptor = get_column_descriptor(ld_client, live_report_id, numeric_column_id)

    # set color styles in range rule for the column as defined in class ColorStyle()
    range_color_styles = [{
        'color_low': '#33FF33',
        'color_high': '#6666CC',
        'matching_string': None,
        'matching_strings_list': None,
        'range_low': None,
        'value_low': -10.2,
        'log_scale': False,
        'range_high': None,
        'value_high': -1.1,
        'color_style_type': 'NUMBER',
        'relative': False
    }]

    # applying color styles to the column
    updated_column_descr_after_range_coloring_rule = apply_coloring_rule(ld_client, live_report_id,
                                                                         initial_column_descriptor, range_color_styles)

    # verify color added
    assert updated_column_descr_after_range_coloring_rule.color_styles == range_color_styles, \
        "Color styles format does not match for addable_col_id {}".format(numeric_column_id)

    # set color styles in range rule with log scale
    range_color_styles_log = [{
        'color_low': '#FF6600',
        'color_high': '#FF99FF',
        'matching_string': None,
        'matching_strings_list': None,
        'range_low': -11.0,
        'value_low': -10.2,
        'log_scale': True,
        'range_high': 0.0,
        'value_high': -1.1,
        'color_style_type': 'NUMBER',
        'relative': False
    }]

    # applying log scale color styles to the column
    updated_column_descr_after_log_coloring_rule = apply_coloring_rule(ld_client, live_report_id,
                                                                       initial_column_descriptor,
                                                                       range_color_styles_log)

    # verify color added
    assert updated_column_descr_after_log_coloring_rule.color_styles == range_color_styles_log, \
        "Color styles format does not match for addable_col_id {}".format(numeric_column_id)

    # set color styles in categorical rule
    categorical_green_color_styles = {
        'color_low': '#33FF33',
        'color_high': None,
        'matching_string': '"-5.5"|"-8"',
        'matching_strings_list': ['-5.5', '-8'],
        'range_low': None,
        'value_low': -10.2,
        'log_scale': False,
        'range_high': None,
        'value_high': -1.1,
        'color_style_type': 'CATEGORICAL',
        'relative': False
    }
    categorical_red_color_styles = {
        'color_low': '#FF0000',
        'color_high': None,
        'matching_string': '"-10.2"|"-1.1"',
        'matching_strings_list': ['-10.2', '-1.1'],
        'range_low': None,
        'value_low': -10.2,
        'log_scale': False,
        'range_high': None,
        'value_high': -1.1,
        'color_style_type': 'CATEGORICAL',
        'relative': False
    }

    # applying color styles to the column
    updated_column_descr_after_categorical_coloring_rule = apply_coloring_rule(
        ld_client, live_report_id, initial_column_descriptor,
        [categorical_green_color_styles, categorical_red_color_styles])

    # verify color added
    assert updated_column_descr_after_categorical_coloring_rule.color_styles == [
        categorical_green_color_styles, categorical_red_color_styles
    ], "Color styles format does not match for addable_col_id {}".format(numeric_column_id)

    # clear all coloring rule and verify
    updated_column_descr_after_clearing_coloring_rule = apply_coloring_rule(ld_client, live_report_id,
                                                                            initial_column_descriptor)
    assert updated_column_descr_after_clearing_coloring_rule.color_styles == [], \
        "Color styles format does not match for addable_col_id {}".format(numeric_column_id)
