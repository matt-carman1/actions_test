from ldclient.enums import MPOConstituentType
from ldclient.models import MPO, MPOConstituent, MPOConstituentBellThreshold, MPOConstituentMonoThreshold, \
    MPOConstituentCategory

from library.api.exceptions import LiveDesignAPIException


def create_mpo_via_api(ldclient, name, project_id, description, constituents=None):
    """
    Creates MPO for provided input values

    :param ldclient: LDClient, ldclient object
    :param name: str, name of the MPO
    :param project_id: str, project id of the MPO
    :param description: str, description for the MPO
    :param constituents: list[MPOConstituent], list of constituent columns on MPO. constituents can be created by
    create_mpo_constituent_columns existed method, which will deal with creation of constituent column based on inputs

    :return: MPO, create mpo object
    """
    return ldclient.create_mpo(MPO(name, project_id=project_id, description=description, constituents=constituents))


def create_mpo_constituent(column_id,
                           column_name,
                           value_distribution,
                           property_weight=1.0,
                           good=None,
                           bad=None,
                           ok=None,
                           low_threshold=None,
                           low_mid_threshold=None,
                           mid_high_threshold=None,
                           high_threshold=None):
    """
    This will creates constituents for MPO, this works like 'Add Constituent' in UI, you need to add costituent list
    explicitly for MPO

    :param column_id: str, id of the constituent column
    :param column_name: str, name of the constituent column
    :param value_distribution: str, value distribution for the constituent.
        Supported Values: 'Categorical', 'Higher Better', 'Lower Better', 'Middle Good', 'Middle Bad'
    :param property_weight: float, property wight to be applied on constituent
    :param good: list, values to be added under good category(needed only for 'Categorical' distribution)
    :param bad: list, values to be added under bad category(needed only for 'Categorical' distribution)
    :param ok: list, values to be added under ok category(needed only for 'Categorical' distribution)
    :param low_threshold: float, low threshold value(needed for all distributions except 'Categorical')
    :param low_mid_threshold: float, low to middle threshold value(needed for all distributions except 'Categorical')
    :param mid_high_threshold: float, mid to high threshold value(needed for all distributions except 'Categorical')
    :param high_threshold: float, high threshold value(needed for all distributions except 'Categorical')

    :return: ldclient.models.MPOConstituent, Constituent object for given inputs
    """
    constituent = None
    if value_distribution == 'Categorical':
        constituent = MPOConstituent(addable_column_id=column_id,
                                     addable_column_name=column_name,
                                     category=MPOConstituentCategory(good=good, bad=bad, ok=ok),
                                     type=MPOConstituentType.CATEGORY,
                                     weight=property_weight)

    elif value_distribution == 'Higher Better':
        constituent = MPOConstituent(addable_column_id=column_id,
                                     addable_column_name=column_name,
                                     mono_threshold=MPOConstituentMonoThreshold(low_threshold=low_threshold,
                                                                                high_threshold=high_threshold,
                                                                                high_good=True),
                                     type=MPOConstituentType.MONO,
                                     weight=property_weight)

    elif value_distribution == 'Lower Better':
        constituent = MPOConstituent(addable_column_id=column_id,
                                     mono_threshold=MPOConstituentMonoThreshold(low_threshold=low_threshold,
                                                                                high_threshold=high_threshold,
                                                                                high_good=False),
                                     addable_column_name=column_name,
                                     type=MPOConstituentType.MONO,
                                     weight=property_weight)

    elif value_distribution == 'Middle Good':
        constituent = MPOConstituent(addable_column_id=column_id,
                                     addable_column_name=column_name,
                                     bell_threshold=MPOConstituentBellThreshold(
                                         low_threshold=low_threshold,
                                         low_middle_threshold=low_mid_threshold,
                                         middle_high_threshold=mid_high_threshold,
                                         high_threshold=high_threshold,
                                         middle_good=True),
                                     type=MPOConstituentType.BELL,
                                     weight=property_weight)

    elif value_distribution == 'Middle Bad':
        constituent = MPOConstituent(addable_column_id=column_id,
                                     addable_column_name=column_name,
                                     bell_threshold=MPOConstituentBellThreshold(
                                         low_threshold=low_threshold,
                                         low_middle_threshold=low_mid_threshold,
                                         middle_high_threshold=mid_high_threshold,
                                         high_threshold=high_threshold,
                                         middle_good=False),
                                     type=MPOConstituentType.BELL,
                                     weight=property_weight)

    else:
        raise LiveDesignAPIException(
            'Please pass valid value, value_destribution should be either of Categorical, Higher Better, Lower Better, '
            'Middle Good, Middle Bad')
    return constituent
