from helpers.api.actions.livereport import create_new_live_report, convert_live_report_into_template
from helpers.api.verification.live_report import verify_column_names_and_compound_ids
from library.utils import make_unique_name

live_report_to_duplicate = {'livereport_name': '2 Compounds 2 Freeform Column', 'livereport_id': 891}
test_type = 'api'


def test_create_new_template(ld_api_client, duplicate_live_report):
    """
    Test to create a new template and apply the newly created template to a LiveReport

    ld_api_client : Fixture for accessing LD client api
    duplicate_live_report : Fixture that will duplicate the given LiveReport
    """
    # make the live report into template
    template = convert_live_report_into_template(ld_api_client, duplicate_live_report)
    # verify if the template is saved by verifying if the template attribute of LiveReport object is set to true
    assert template.template, "Template is not saved"

    # create a new Live Report
    live_report_name = make_unique_name('lr')
    lr_response = create_new_live_report(ld_api_client, live_report_name, project_id='4')
    lr_id = lr_response.id

    # apply template created to new LR that's created
    ld_api_client.apply_template_to_live_report(template.id, lr_id)

    # verify of the template is applied to newly created live report
    # expected columns are columns in the template and expected to be present in live report
    expected_column_names = [
        'Unpublished Freeform Text Column', 'Published Freeform Text Column', 'Entity ID', 'ID', 'All IDs',
        'Lot Scientist', 'Compound Structure', 'Rationale', 'Lot Date Registered', 'Entity Type'
    ]
    # expected compound id's will have compound id's present in template and live report
    expected_compound_ids = ['V035624', 'V035625']

    verify_column_names_and_compound_ids(ld_api_client, lr_id, expected_column_names, expected_compound_ids)
    # delete live report after verification is done
    ld_api_client.delete_live_report(lr_id)
