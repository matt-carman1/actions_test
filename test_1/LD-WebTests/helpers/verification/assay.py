from helpers.change.grid_columns import scroll_to_column_header, get_cell
from helpers.selection.assay import ASSAY_LIMITED_TOOLTIP, ASSAY_LIMITED_TOOLTIP_TITLE, \
    ASSAY_LIMITED_TOOLTIP_CONDITION_LABEL_AND_VALUE, ASSAY_HEADER_AGGREGATION_LABEL
from helpers.selection.grid import AGGREGATE_CELLTIP_TEXT
from helpers.verification.element import verify_is_visible
from library import simulate, dom, wait


def verify_limited_assay_column_tooltip(driver,
                                        limited_assay_column_name,
                                        expected_assay_tooltip_title,
                                        expected_tooltip_text,
                                        exact_text_match=True):
    """
    Check the tooltip for limited assay column

    :param driver: Selenium Webdriver
    :param limited_assay_column_name: str, Limited Assay Column name
    :param expected_assay_tooltip_title: str, text visible in the limited assay column tooltip title. For e.g.
                                        'PK_PO_RAT (Dose)\nLimiting Conditions:'
    :param expected_tooltip_text: list, limiting conditions text visible in the limited assay column tooltip. For e.g.
                                  ['AUC:\n-∞ to 5', 'Dose:\n-∞ to 20']
    :param exact_text_match: Whether text match should be exact. Optional.
    """

    column_header = scroll_to_column_header(driver, column_name=limited_assay_column_name, custom_timeout=10)
    simulate.hover(driver, column_header)
    """Added this wait to ensure that the tooltip is available because when writing this test it was observed that 
    transition from one column tooltip to another column tooltip is not smooth and takes around ~500ms to show up."""
    wait.until_visible(driver,
                       ASSAY_LIMITED_TOOLTIP_TITLE,
                       text=expected_assay_tooltip_title.split('\n')[1],
                       timeout=7,
                       exact_text_match=exact_text_match)

    # Verifying the Tooltip title
    observed_assay_tooltip_title = dom.get_elements(driver, '{} div:first-child'.format(ASSAY_LIMITED_TOOLTIP))[0].text
    # NOTE (tchoi) this is a substring search, not an equals, see SS-42069
    assert expected_assay_tooltip_title in observed_assay_tooltip_title, "Expected {} but got this {}". \
        format(expected_assay_tooltip_title, observed_assay_tooltip_title)

    # Verifying the limiting condition(s) and its value(s)
    """Since we need the limiting condition and its value to be corresponding in the tooltip, we could not simple rely 
    on the  ASSAY_LIMITED_TOOLTIP element to get the tooltip text and then split and sort as that would change order
    such that validation would be useless. For e.g if getting the element for ASSAY_LIMITED_TOOLTIP returns the text:
    'PK_PO_RAT (Dose)\nLimiting Conditions:\nAUC:\n-∞ to 5\nDose:\n-∞ to 20', then split by "\n" followed by sorting
    would give: ['-∞ to 20', '-∞ to 5', 'AUC:', 'Dose:', 'Limiting Conditions:', 'PK_PO_RAT (Dose)']"""
    observed_assay_tooltip_text_elements = dom.get_elements(driver, ASSAY_LIMITED_TOOLTIP_CONDITION_LABEL_AND_VALUE)
    observed_assay_tooltip_text_list = [element.text for element in observed_assay_tooltip_text_elements]
    sorted_observed_assay_tooltip_text_list = observed_assay_tooltip_text_list.sort()
    sorted_expected_tooltip_text = expected_tooltip_text.sort()

    assert sorted_observed_assay_tooltip_text_list == sorted_expected_tooltip_text, "Expected {} but got this {}". \
        format(sorted_expected_tooltip_text, sorted_observed_assay_tooltip_text_list)


def verify_assay_aggregation_column_label(driver, assay_column_name, expected_aggregation_label):
    """
    Verifies the assay's aggregation mode label in the column header is expected text.

    :param driver: Selenium Webdriver
    :param assay_column_name: str, the assay column's name
    :param expected_aggregation_label: str, expected aggregation label text to be found
    """
    possible_labels = {"UNAGGREGATED", "LATEST", "MEDIAN", "ARI", "GEO", "MIN", "MAX", "STDDEV", "COUNT"}
    assert expected_aggregation_label in possible_labels, \
        "`{}` is not one of the possible aggregation labels:\n{}".format(expected_aggregation_label, possible_labels)

    column = scroll_to_column_header(driver, assay_column_name)
    actual_aggregation_label = dom.get_element(column, ASSAY_HEADER_AGGREGATION_LABEL).text
    assert expected_aggregation_label == actual_aggregation_label, \
        "Expected `{}` column header to have aggregation label, `{}`, but got, `{}`".format(
            assay_column_name, expected_aggregation_label, actual_aggregation_label)


def verify_assay_cell_tooltip(driver, compound_id, column_title, expected_assay_tooltip):
    """
    Verify assay tooltip for specified row and column.

    :param driver: selenium webdriver
    :param compound_id: str, ID of the row, ex: For Compound mode: compound ID, Lot mode: Lot ID
    :param column_title: str, column title of the cell
    :param expected_assay_tooltip: str, expected assay tooltip value
    """
    # Getting column cell and hovering on the cell
    assay_cell = get_cell(driver, compound_id=compound_id, column_title=column_title)
    simulate.hover(assay_cell)

    # verify assay tooltip
    verify_is_visible(driver,
                      AGGREGATE_CELLTIP_TEXT,
                      selector_text=expected_assay_tooltip,
                      custom_timeout=5,
                      exact_selector_text_match=True)
