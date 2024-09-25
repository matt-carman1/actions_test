import pytest

from helpers.change import actions_pane, filter_actions
from helpers.flows import add_compound
from helpers.change.grid_columns import scroll_to_column_header
from helpers.selection.filter_actions import BOX_WIDGET_BODY_CATEGORY
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values
from library import wait


# TODO: There's a plan to create a set of tests that deal with ID. Once there's a location for that, this can be
# relocated.
# TODO: Take the functionality that is not in test_filter_text.py but that is also not ID-specific (e.g. "Match
# prefix" and "Case sensitive") and move it there.
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures("use_module_isolated_project")
def test_id_filter(selenium):
    """
    Test ID filter with text, range, quick filter along with certain filter settings like "Match Prefix",
    "Match Anywhere" and Case Sensitivity.
    :param selenium: Webdriver
    :return:
    """
    molv3 = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 20 22 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C 2.810857 3.675143 0.000000 0\nM  V30 2 C 2.323143 2.332571 0.000000 0\nM  V30 3 C 3.730286 2.085714 0.000000 0\nM  V30 4 O 1.085429 3.045714 0.000000 0\nM  V30 5 C -0.151143 2.330571 0.000000 0\nM  V30 6 C -1.388857 3.044000 0.000000 0\nM  V30 7 C -2.625429 2.328571 0.000000 0\nM  V30 8 C -2.624286 0.900000 0.000000 0\nM  V30 9 C -1.386571 0.186857 0.000000 0\nM  V30 10 C -0.150000 0.902000 0.000000 0\nM  V30 11 C 1.087714 0.188571 0.000000 0\nM  V30 12 C 2.324286 0.904000 0.000000 0\nM  V30 13 O 3.562000 0.190571 0.000000 0\nM  V30 14 N 1.088857 -1.240000 0.000000 0\nM  V30 15 C 0.079429 -2.250857 0.000000 0\nM  V30 16 C 1.090571 -3.260286 0.000000 0\nM  V30 17 C 2.100000 -2.249429 0.000000 0\nM  V30 18 O 3.528571 -2.248286 0.000000 0\nM  V30 19 C -3.860857 0.184857 0.000000 0\nM  V30 20 N -5.097429 -0.530571 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 2 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 8 9\nM  V30 9 2 9 10\nM  V30 10 1 10 11\nM  V30 11 1 11 12\nM  V30 12 1 12 13\nM  V30 13 1 11 14\nM  V30 14 1 14 15\nM  V30 15 1 15 16\nM  V30 16 1 16 17\nM  V30 17 2 17 18\nM  V30 18 1 8 19\nM  V30 19 3 19 20\nM  V30 20 1 12 2\nM  V30 21 1 17 14\nM  V30 22 1 10 5\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
    search_keyword = "CHEMBL105*,CRA-035507,CHEMBL103*"

    actions_pane.open_add_compounds_panel(selenium)
    # Add compounds by MOLV
    add_compound.add_compound_by_molv_to_active_lr(selenium, molv3)
    # Search Compounds by ID and add to LR
    add_compound.search_by_id(selenium, search_keyword)

    # This function would check in a way that the column is added to the LR
    scroll_to_column_header(selenium, 'ID')

    # Open the Filter Panel and Clear filters if there were some leftover ones
    actions_pane.open_filter_panel(selenium)
    filter_actions.remove_all_filters(selenium)

    # Add ID filter
    filter_actions.add_filter(selenium, 'ID')
    ids_filter_element = filter_actions.get_filter(selenium, 'ID', filter_position=3)
    wait.until_visible(ids_filter_element, BOX_WIDGET_BODY_CATEGORY)

    # Testing TEXT ID FILTER
    # Test "(undefined)" text filter
    filter_actions.type_and_select_filter_item(ids_filter_element, "(undefined)")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(24),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(0)
        })
    filter_actions.select_filter_checkbox_item(ids_filter_element, "(undefined)", do_select=False)
    # Verifying footer values after the filter is removed.
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(24),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(24)
        })

    # Default text filter setting is Case insensitive and Match Exactly
    filter_actions.type_and_select_filter_item(ids_filter_element, "chembl1059")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(24),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(1)
        })

    # Testing with "Match exactly" and "Case sensitive"
    filter_actions.change_filter_settings(ids_filter_element, "Case sensitive", 3, confirm_dialog=False)
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(24),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(0)
        })
    filter_actions.select_filter_checkbox_item(ids_filter_element, "chembl1059", do_select=False)

    # Testing with "Match prefix" and "Case sensitive"
    filter_actions.change_filter_settings(ids_filter_element, "Match prefix", 3, confirm_dialog=False)
    wait.until_loading_mask_not_visible(selenium)

    filter_actions.type_and_select_filter_item(ids_filter_element, "CHEMBL")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(24),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22)
        })
    filter_actions.select_filter_checkbox_item(ids_filter_element, "CHEMBL", do_select=False)
    filter_actions.type_and_select_filter_item(ids_filter_element, "CRA-03")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(24),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(1)
        })
    filter_actions.select_filter_checkbox_item(ids_filter_element, "CRA-03", do_select=False)

    # Testing with "Match anywhere" and "Case sensitive"
    filter_actions.change_filter_settings(ids_filter_element, "Match anywhere", 3, confirm_dialog=False)
    wait.until_loading_mask_not_visible(selenium)
    filter_actions.type_and_select_filter_item(ids_filter_element, "103")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(24),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(11)
        })
    filter_actions.select_filter_checkbox_item(ids_filter_element, "103", do_select=False)

    # Range ID filter test: There is noway to check that the range filter is disabled for text type Filters.
    # Removing the deprecated/invalid code with this comment.

    # Quick filter ID Test: This behavior has changed in 8.9.x. Removing the deprecated behavior.
    # The Test for Real/Virtual Filter would be taken care by QA-3709
    filter_actions.remove_all_filters(selenium)
