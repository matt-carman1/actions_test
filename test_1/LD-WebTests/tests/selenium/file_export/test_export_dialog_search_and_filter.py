from library import dom

from helpers.change.live_report_menu import open_export_dialog_from_lr_dropdown
from helpers.selection.modal import MODAL_CANCEL_BUTTON, MODAL_DIALOG_HEADER
from helpers.verification.element import verify_is_visible
from helpers.verification.export_dialog import verify_export_dialog_choose_subset_part, \
    search_and_verify_filtered_columns_on_export_dialog

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


def test_export_dialog_search_and_filter(selenium, duplicate_live_report, open_livereport):
    """
    Test to verify that the search and filter works properly on the export dialog
    using three search items (two valid and one invalid item)

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: a fixture which duplicates the live report
    :param open_livereport: a fixture which opens the live report
    """
    # Access Export Dialog from LR Dropdown menu
    open_export_dialog_from_lr_dropdown(selenium, livereport=duplicate_live_report, file_format='SDF')
    verify_is_visible(selenium, selector=MODAL_DIALOG_HEADER, selector_text='Export LiveReport')

    # Expected list of columns
    expected_columns = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Lot Date Registered', 'PK_PO_RAT (AUC)',
        'PK_PO_RAT (Absorption)', 'DRC TEST ASSAY (IC50%)', 'Test RPE Formula', 'Test RPE MPO',
        'CorpID String (CorpID String)'
    ]

    # Verifying 'Choose Subset' part of the dialog
    verify_export_dialog_choose_subset_part(selenium, expected_columns)

    # ----- SEARCH AND VERIFY FILTERED RESULTS FOR THREE CASES ----- #
    # Three characters
    search_and_verify_filtered_columns_on_export_dialog(
        selenium,
        search_item='Rat',
        expected_filtered_columns=['Rationale', 'PK_PO_RAT (AUC)', 'PK_PO_RAT (Absorption)'])
    # Entire column name
    search_and_verify_filtered_columns_on_export_dialog(selenium,
                                                        search_item='Lot Date Registered',
                                                        expected_filtered_columns=['Lot Date Registered'])
    # Invalid name
    search_and_verify_filtered_columns_on_export_dialog(selenium, search_item='RandomStr', expected_filtered_columns=[])

    dom.click_element(selenium, selector=MODAL_CANCEL_BUTTON, text='Cancel')
