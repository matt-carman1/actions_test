from helpers.api.actions.mpo import create_mpo_via_api, create_mpo_constituent
from helpers.api.verification.mpo import verify_mpo
from library import utils


def test_create_mpo_on_published_constituents(ld_api_client):
    """
    Test to create mpo using create_mpo ldclient method

    1. Create MPO with published constituent columns

    :param ld_api_client: LDClient, ldclient object
    """
    # --- create MPO with multiple published columns ----- #
    # Creating different types of constituents on published columns
    higher_better_on_pk_mouse_auc = create_mpo_constituent('781',
                                                           'PK_IP_MOUSE (AUC)',
                                                           'Higher Better',
                                                           low_threshold='100.0',
                                                           high_threshold='300.0')
    lower_better_on_number_published = create_mpo_constituent('3596',
                                                              'Number - published',
                                                              'Lower Better',
                                                              low_threshold='2.0',
                                                              high_threshold='500.0')
    medium_bad_constituent_column = create_mpo_constituent('1266',
                                                           'AlogP (AlogP)',
                                                           'Middle Bad',
                                                           low_threshold='1.0',
                                                           low_mid_threshold='20.3',
                                                           mid_high_threshold='30.0',
                                                           high_threshold='40.0')

    # Creating MPO using constituents
    mpo_name = utils.make_unique_name('MPO on published columns')
    created_mpo = create_mpo_via_api(
        ld_api_client,
        name=mpo_name,
        project_id='4',
        description='Test MPO',
        constituents=[medium_bad_constituent_column, higher_better_on_pk_mouse_auc, lower_better_on_number_published])

    # verifying MPO
    verify_mpo(ld_api_client,
               created_mpo,
               expected_name=mpo_name,
               expected_project='4',
               expected_description='Test MPO',
               expected_constituents=[
                   medium_bad_constituent_column, higher_better_on_pk_mouse_auc, lower_better_on_number_published
               ])
