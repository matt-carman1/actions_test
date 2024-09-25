import pytest

from helpers.change.actions_pane import open_add_compounds_panel, open_add_data_panel, close_add_data_panel
from helpers.flows.add_compound import search_by_id
from helpers.change.columns_action import add_column_by_name
from helpers.verification.grid import verify_footer_values, verify_grid_contents
from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.live_report_menu import save_as_new_template, delete_open_live_report
from helpers.change.live_report_picker import create_and_open_live_report
from helpers.verification.color import verify_column_color
from helpers.selection.grid import GRID_HEADER_CELL, GRID_COLUMN_HEADER_SORT_ICON_, Footer
from library import dom


def test_saving_a_livereport_template(selenium, new_live_report, open_livereport):
    """
    Test saving a template and verifying it:
    1. Create a new Live Report:
        a) add compounds to it via ID search
        b) adds rows via the Add Data & Columns gadget
        c) adds a range filter
        d) add MPO(This would work for coloring rule as well)
    2. Verify the above content and coloring rule
    3. Creates a template from that Live Report and deletes the original.
    4. Verify that the template is saved and then create a new Live Report from the template and repeats the
    verifications.
    :param selenium: Webdriver
    :param new_live_report: fixture used to create a new LiveReport
    :return:
    """

    live_report_name = new_live_report

    # Add Compounds
    open_add_compounds_panel(selenium)
    search_by_id(selenium, 'CRA-032913, CRA-033084, CRA-033120, CRA-033145, CRA-033148, CRA-033619')

    # Add Columns
    open_add_data_panel(selenium)
    add_column_by_name(selenium, 'BTK-TRFRET (Ki)')
    add_column_by_name(selenium, 'CYP450 3A4_MD-LCMS (%INH@10uM)')
    add_column_by_name(selenium, 'PK_PO_RAT (AUC)')
    add_column_by_name(selenium, '(Global) Lower is Good')
    close_add_data_panel(selenium)

    # Verify # of compounds and columns and grid content
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(11),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })
    sort_grid_by(selenium, 'ID')

    # Save a template
    # NOTE(tchoi) I had to add in the template_name param, otherwise the test would fail here.
    template_name = save_as_new_template(selenium,
                                         template_name='(TEST) New Test Template',
                                         live_report_name=live_report_name)

    # Create and open a new LiveReport based on the template
    lr_created_from_template = create_and_open_live_report(selenium,
                                                           report_name='test_save_template',
                                                           template=template_name)

    # Verify LR is sorted by ID
    id_column = dom.get_element(selenium, GRID_HEADER_CELL, text='ID', exact_text_match=True)
    assert dom.get_element(id_column, GRID_COLUMN_HEADER_SORT_ICON_.format('ASC')), \
        "LR created from template is not sorted by ID"

    # Verify grid contents
    verify_grid_contents(
        selenium, {
            'BTK-TRFRET (Ki) [uM]': ['0.87', '300++', '68.53', '12.58', '40', '3.44'],
            'CYP450 3A4_MD-LCMS (%INH@10uM) [%]': ['37', '66', '50', '<10', '<10', '43.5'],
            'PK_PO_RAT (AUC) [uM.min]': ['0.382\n7.09', '1.15\n14.2', '10.6\n34.4', '1.22\n9.64', '', '6.1'],
            'Lower is Good': ['0.996', '0', '0.019', '0.978', '0.5', '0.994'],
            'BTK-TRFRET (Ki) Desirability': ['0.996', '0', '0.019', '0.978', '0.5', '0.994'],
            'Number of missing inputs': ['0', '0', '0', '0', '0', '0']
        })

    # Verify column color pattern
    verify_column_color(selenium,
                        'BTK-TRFRET (Ki) [uM]',
                        expected_colors=[(2, 255, 0, 1), (255, 0, 0, 1), (254, 9, 0, 1), (11, 255, 0, 1),
                                         (255, 254, 0, 1), (3, 255, 0, 1)])

    # Deleting the LiveReport created using the template at the end of the test.
    delete_open_live_report(selenium, lr_created_from_template)
