from helpers.api.extraction.mpo import get_mpo_names_from_project
from library.api.utils import sort_objects_based_on_field


def validate_mpo_objects(actual_mpo, expected_mpo):
    """
    Verify whether 2 mpo objects are same.

    :param actual_mpo: ldclient.models.MPO, actual MPO object
    :param expected_mpo: ldclient.models.MPO, expected MPO object
    """
    for field in vars(expected_mpo).keys():
        # getting field values from object
        actual_field = getattr(actual_mpo, field)
        field_from_mpo_by_id = getattr(expected_mpo, field)

        # sorting constituents as constituents order is not same always
        if field == 'constituents':
            actual_field = str(sort_objects_based_on_field(actual_field, 'addable_column_id'))
            field_from_mpo_by_id = str(sort_objects_based_on_field(field_from_mpo_by_id, 'addable_column_id'))

        assert actual_field == field_from_mpo_by_id, \
            "{} value doesn't match, Expected value:{}, But got:{}".format(field, actual_field, field_from_mpo_by_id)


def verify_mpo(ldclient, created_mpo, expected_name, expected_project, expected_constituents, expected_description):
    """
    verify whether MPO created properly

    """
    # verify MPO name, description and constituents
    assert created_mpo.name == expected_name
    assert created_mpo.description == expected_description

    # sorting constituents as order is not same always
    actual_sorted_constituents = str(sort_objects_based_on_field(created_mpo.constituents, 'addable_column_id'))
    expected_sorted_constituents = str(sort_objects_based_on_field(expected_constituents, 'addable_column_id'))
    assert actual_sorted_constituents == expected_sorted_constituents, "Expected constituents:{}, But got:{}".format(
        expected_sorted_constituents, actual_sorted_constituents)

    # verify whether mpo created in project
    assert created_mpo.name in get_mpo_names_from_project(ldclient, project_ids=[expected_project])

    # verifying created mpo with MPO which got from get_mpo_by_id method
    mpo_by_id_object = ldclient.get_mpo_by_id(created_mpo.id)
    validate_mpo_objects(created_mpo, mpo_by_id_object)
