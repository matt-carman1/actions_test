import pytest

from helpers.change.filter_actions import remove_all_filters, set_filter_for_r_groups
from helpers.flows import add_compound
from helpers.verification.grid import verify_footer_values

live_report_to_duplicate = {'livereport_name': '4 Compounds 3 formulas', 'livereport_id': '890'}


@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_set_filters_on_R_groups(selenium):
    """
    Test to set filters on the R-groups present in the LR only
    1. Duplicate a live_report and add R-groups via search by ID
    2. Remove all the filters, if previously present
    3. Applying R-group filter via deselecting COMPOUND
    4. Verify the application of R-group filter
    :param selenium: Selenium Webdriver
    """

    # To add R-groups via search by ID
    search_keyword = "R055831, R055832, R055833"

    # To add the R-groups in the livereport
    add_compound.search_by_id(selenium, search_keyword)

    # To verify the total number of compounds present in livereport via footer
    verify_footer_values(selenium, {
        'row_all_count': '7 Total Compounds',
        'column_all_count': '11 Columns',
        'column_hidden_count': '2 Hidden'
    })

    # Remove all applied filters
    remove_all_filters(selenium)

    # Applying filter for R-groups
    set_filter_for_r_groups(selenium)

    # Verify grid contents after R-group filter is applied via footer
    verify_footer_values(
        selenium, {
            'row_all_count': '7 Total Compounds',
            'row_filtered_count': '3 After Filter',
            'row_selected_count': '0 Selected',
            'column_all_count': '11 Columns',
            'column_hidden_count': '2 Hidden'
        })
