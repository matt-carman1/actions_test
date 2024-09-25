from helpers.change.grid_column_menu import sort_grid_by, click_column_menu_item
from helpers.flows.live_report_management import duplicate_livereport
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_grid_contents, verify_footer_values, verify_column_contents

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


def test_duplicate_livereport_with_sort_order(selenium, duplicate_live_report, open_livereport):
    """
    Test duplicate livereport with sort order.

    1. Duplicate LR with sorting applied on 2 columns(AlogP and PSA)
    2. Verify grid results of duplicated livereport having same order as original livereport
    3. Duplicate LR with selecting one sorting applied column(PSA)
    4. Verify grid results of duplicated livereport, sort order applied on only PSA
    5. Duplicate LR with not selecting any of the sorting applied columns
    6. verify default sort order applied to the duplicated livereport

    :param selenium: Selenium webdriver
    :param duplicate_live_report: a fixture which duplicates live report
    :param open_livereport: a fixture which opens live report
    """
    # Apply sorting on AlogP(AlogP) - Ascending, PSA(PSA) - Descending
    sort_grid_by(selenium, 'AlogP (AlogP)')
    click_column_menu_item(selenium, 'PSA (PSA)', 'Sort', 'Add to Sort, Descending')

    # ----- Duplicate Livereport with sorting applied on 2 columns(AlogP and PSA) ----- #
    duplicated_lr = duplicate_livereport(selenium,
                                         duplicate_live_report,
                                         selected_columns=['AlogP (AlogP)', 'PSA (PSA)'])

    # ----- Verify grid results of duplicated livereport having same order as original livereport ----- #
    verify_footer_values(
        selenium, {
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(7),
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)
        })
    verify_grid_contents(
        selenium, {
            'ID': ['V035752', 'V041170', 'V038399', 'V041471', 'V044401'],
            'AlogP (AlogP)': ['1.4', '4.1', '4.8', '4.8', '5.2'],
            'PSA (PSA)': ['145.1', '61.7', '177.2', '12.5', '124.1']
        })

    # ----- Duplicate LR with selecting one sorting applied column(PSA) ----- #
    new_lr = duplicate_livereport(selenium, duplicated_lr, selected_columns=['PSA'])

    # ----- Verify grid results of duplicated livereport, sort order applied on only PSA ----- #
    verify_footer_values(
        selenium, {
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)
        })
    verify_grid_contents(
        selenium, {
            'ID': ['V038399', 'V035752', 'V044401', 'V041170', 'V041471'],
            'PSA (PSA)': ['177.2', '145.1', '124.1', '61.7', '12.5']
        })

    # ----- Duplicate LR with not selecting any of the sorting applied columns ----- #
    duplicate_livereport(selenium, new_lr, selected_columns=[])

    # ----- verify default sort order(ascending order on ID) applied to the duplicated livereport ----- #
    verify_footer_values(
        selenium, {
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)
        })
    verify_column_contents(selenium, 'ID', ['V035752', 'V038399', 'V041170', 'V041471', 'V044401'])
