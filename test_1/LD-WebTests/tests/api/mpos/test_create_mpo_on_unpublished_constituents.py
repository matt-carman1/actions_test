from helpers.api.actions.mpo import create_mpo_via_api, create_mpo_constituent
from helpers.api.verification.mpo import verify_mpo
from library import utils


def test_create_mpo_on_unpublished_constituents(ld_api_client):
    """
    Test to create mpo using create_mpo ldclient method

    1. Create MPO with unpublished constituent columns

    :param ld_api_client: LDClient, ldclient object
    """
    # -----  Create MPO on unpublished constituent columns ----- #
    # Creating constituents on unpublished columns
    medium_good_constituent_column_number_upublished = create_mpo_constituent(column_id='3590',
                                                                              column_name='Number  - unpublished',
                                                                              value_distribution='Middle Good',
                                                                              low_threshold='1.0',
                                                                              low_mid_threshold='20.0',
                                                                              mid_high_threshold='30.0',
                                                                              high_threshold='40.0')

    categorical_constituent_on_text_unpublished = create_mpo_constituent(column_id='3589',
                                                                         column_name='Text - unpublished',
                                                                         value_distribution='Categorical',
                                                                         good=['Cool story tho'],
                                                                         ok=['undefined'],
                                                                         bad=['defined'])
    # creating MPO with constituents
    mpo_name = utils.make_unique_name('MPO on Unpublished columns')
    created_mpo = create_mpo_via_api(
        ld_api_client,
        mpo_name,
        project_id='4',
        description='Test MPO unpublished column',
        constituents=[categorical_constituent_on_text_unpublished, medium_good_constituent_column_number_upublished])

    # verify created MPO
    verify_mpo(ld_api_client,
               created_mpo,
               expected_name=mpo_name,
               expected_project='4',
               expected_description='Test MPO unpublished column',
               expected_constituents=[
                   categorical_constituent_on_text_unpublished, medium_good_constituent_column_number_upublished
               ])
