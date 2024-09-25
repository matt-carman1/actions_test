from ldclient.client import LDClient


def apply_coloring_rule(ldclient: LDClient, live_report_id, column_descriptor, color_style=[]):
    """
    Applies color styles to a column descriptor and returns the updated descriptor

    Example Usage:
    colored_descriptor = apply_coloring_rules(ldclient, live_report_id, column_descriptor,
    color_style=[{
        'color_low': '#999999',
        'color_high': '#6666CC',
        'matching_string': None,
        'matching_strings_list': None,
        'range_low': None,
        'value_low': 2.3,
        'log_scale': False,
        'range_high': None,
        'value_high': 5.4,
        'color_style_type': 'NUMBER',
        'relative': False
    }])

    :param ldclient: livedesign client
    :param live_report_id: str, LiveReport ID
    :param column_descriptor: :class:`~models.ColumnDescriptor`
    :param color_style: list of dict, color style rule as in ldclient.models.ColorStyle(), by default blank
    """
    # update defined color styles to the given column descriptor
    column_descriptor.color_styles = color_style
    # apply the updated descriptor to the livereport column
    colored_descriptor = ldclient.add_column_descriptor(live_report_id, column_descriptor)
    return colored_descriptor
