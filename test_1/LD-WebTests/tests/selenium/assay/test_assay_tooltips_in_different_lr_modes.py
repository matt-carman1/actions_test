import pytest

from helpers.change.actions_pane import toggle_lr_mode, click_expand_row
from helpers.verification.assay import verify_assay_cell_tooltip

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('duplicate_live_report')
def test_assay_tooltips_in_different_lr_modes(selenium):
    """
    Test to check assay tooltips shows up in following lr modes

    1. Row per compound mode
    2. Row per Lot mode
    3. Row per Salt mode
    4. Row per Lot Salt mode
    5. Row per Pose mode
    6. Row per Experiment mode

    (Due to insufficient data, this test is only to check
    that the tooltips appear and does not validate the data integrity)
    :param selenium: Selenium webdriver
    """
    column_name = 'PK_PO_RAT (AUC) [uM]'
    # verify assay tooltip in Row per compound mode
    verify_assay_cell_tooltip(selenium,
                              compound_id='V055682',
                              column_title=column_name,
                              expected_assay_tooltip="\n".join([
                                  "2 Data points", "20 uM", "Batch:", "1", "Concentration Units:", "%", "Date:",
                                  "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2", "10 uM", "Batch:", "0", "Concentration Units:", "%",
                                  "Date:", "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2"
                              ]))

    # Verify assay tooltip in Row per Lot mode
    toggle_lr_mode(selenium, 'Lot')
    verify_assay_cell_tooltip(selenium,
                              compound_id='V055682-V',
                              column_title=column_name,
                              expected_assay_tooltip="\n".join([
                                  "2 Data points", "20 uM", "Batch:", "1", "Concentration Units:", "%", "Date:",
                                  "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2", "10 uM", "Batch:", "0", "Concentration Units:", "%",
                                  "Date:", "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2"
                              ]))

    # Verify assay tooltip in Row per Salt mode
    toggle_lr_mode(selenium, 'Salt')
    verify_assay_cell_tooltip(selenium,
                              compound_id='V055682',
                              column_title=column_name,
                              expected_assay_tooltip="\n".join([
                                  "2 Data points", "20 uM", "Batch:", "1", "Concentration Units:", "%", "Date:",
                                  "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2", "10 uM", "Batch:", "0", "Concentration Units:", "%",
                                  "Date:", "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2"
                              ]))

    # Verify assay tooltip in Row per Lot Salt mode
    toggle_lr_mode(selenium, 'Lot Salt')
    verify_assay_cell_tooltip(selenium,
                              compound_id='V055682-V',
                              column_title=column_name,
                              expected_assay_tooltip="\n".join([
                                  "2 Data points", "20 uM", "Batch:", "1", "Concentration Units:", "%", "Date:",
                                  "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2", "10 uM", "Batch:", "0", "Concentration Units:", "%",
                                  "Date:", "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2"
                              ]))

    # Verify assay tooltip in Row per Pose mode
    toggle_lr_mode(selenium, 'Pose')
    verify_assay_cell_tooltip(selenium,
                              compound_id='V055682',
                              column_title=column_name,
                              expected_assay_tooltip="\n".join([
                                  "2 Data points", "20 uM", "Batch:", "1", "Concentration Units:", "%", "Date:",
                                  "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2", "10 uM", "Batch:", "0", "Concentration Units:", "%",
                                  "Date:", "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2"
                              ]))

    # verify assay tooltip in Experiment mode
    click_expand_row(selenium, column_name)
    verify_assay_cell_tooltip(selenium,
                              compound_id='V055682-V-1',
                              column_title=column_name,
                              expected_assay_tooltip="\n".join([
                                  "1 Data point", "20 uM", "Batch:", "1", "Concentration Units:", "%", "Date:",
                                  "Mon Nov 16 2015", "Lot Number:", "V", "Notebook:", "N/A", "Notebook Page:",
                                  "Unknown", "Protocol:", "2"
                              ]))
