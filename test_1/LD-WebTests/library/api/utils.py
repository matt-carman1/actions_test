import operator


def sort_objects_based_on_field(list_of_objects, field_name_to_apply_sorting):
    """
    This will sort list of objects with mentioned field name

    :param list_of_objects: list, list of class objects to sort
    :param field_name_to_apply_sorting: str, name of the field on which sorting should be applied

    :return: list, sorted list of objects
    """
    return sorted(list_of_objects, key=operator.attrgetter(field_name_to_apply_sorting))
