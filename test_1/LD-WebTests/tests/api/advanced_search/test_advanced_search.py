from ldclient.__experimental.experimental_models import QueryCondition

test_type = 'api'


def test_advanced_search(experimental_ldclient, new_live_report):
    """
    API Test for text advanced search.
    1. Create a new LR.
    2. Add a published FFC column to advanced query.
    3. Set the query value as "(defined)"
    4. Verify the compound ID(s) returned.
    5. Set the advanced query value as "Sample Published Text"
    6. Verify the compound ID(s) returned.

    :param experimental_ldclient: Experimental ldclient object
    :param new_live_report: LiveReport Model object, fixture to create a new livereport via ldclient api.
    """

    # New LiveReport
    live_report = new_live_report

    # Addable Column ID for the published FFC to be used for Advanced Query.
    published_freeform_text_column_id = '1250'

    # ----- FIRST CONDITION: VALUE IN PUBLISHED FFC SHOULD BE '(defined)' ----- #
    condition_defined = QueryCondition(addable_column_id=published_freeform_text_column_id,
                                       id='1',
                                       type='observation',
                                       value='(defined)',
                                       value_type='value')
    expected_result_compound_ids = {'V035624', 'V035625'}

    # Do an advanced search query based on the new conditions and expression, search should return two compounds
    obsv_result_compounds = set(
        experimental_ldclient.update_lr_query_and_search_compounds(live_report.id, live_report.project_id,
                                                                   [condition_defined], '1'))
    # Verify the returned compound IDs are as expected.
    assert expected_result_compound_ids == obsv_result_compounds, \
        "Mismatch. Expected {} but got {}".format(expected_result_compound_ids, obsv_result_compounds)

    # ----- SECOND CONDITION: VALUE IN PUBLISHED FFC SHOULD BE 'Sample Published Text' ----- #
    condition_text_value = QueryCondition(addable_column_id=published_freeform_text_column_id,
                                          id='1',
                                          type='observation',
                                          value='Sample Published Text',
                                          value_type='value')
    expected_result_compounds = {'V035624'}

    # Do an advanced search query based on the new conditions and expression
    obsv_result_compounds = set(
        experimental_ldclient.update_lr_query_and_search_compounds(live_report.id, live_report.project_id,
                                                                   [condition_text_value], '1'))
    # Verify the returned compound ID is as expected.
    assert expected_result_compounds == obsv_result_compounds, \
        "Mismatch. Expected {} but got {}".format(expected_result_compound_ids, obsv_result_compounds)
