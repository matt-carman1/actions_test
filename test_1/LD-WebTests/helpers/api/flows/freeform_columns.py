from helpers.api.actions.row import create_observation
from helpers.api.actions.column import add_freeform_values
from helpers.api.verification.live_report import verify_column_values_for_compounds


def add_values_for_ffcs(ldclient, project_id, lr_id, input_info):
    """
    Function to add observations (values) to respective FFCs

    :param ldclient:
    :param project_id: str, Project ID
    :param lr_id: str, LiveReport ID
    :param input_info: dict, Dictionary in specific format
                             Single Value => {'FFC_ID': {'ENTITY_ID': 'VALUE'}}
                             Multi Value => {'FFC_ID': {'ENTITY_ID': ['VALUE_1', 'VALUE2']}}
    """
    observations, temp = [], []
    expected_ffc_values = {}
    # Creates observations and expected_ffc_values dictionary based on the data from input_info parameter
    for ffc_id, value_dict in input_info.items():
        for entity_id, values in value_dict.items():
            # For multi-value FFCs, we can pass list of values for specific compound and FFC ID
            # This will create observation for each of the value in the values list
            if type(values) == list and len(values) > 1:
                for value in values:
                    observations.append(
                        create_observation(project_id=project_id,
                                           entity_id=entity_id,
                                           live_report_id=lr_id,
                                           addable_column_id=ffc_id,
                                           value=value))
                # Passing the values list directly into the expected_ffc_values dict
                expected_ffc_values[entity_id] = values
            else:
                observations.append(
                    create_observation(project_id=project_id,
                                       entity_id=entity_id,
                                       live_report_id=lr_id,
                                       addable_column_id=ffc_id,
                                       value=values))
                # Appending the values into a temp list and passing that list into expected_ffc_values dict
                temp.append(values)
                expected_ffc_values[entity_id] = temp

    add_freeform_values(ld_client=ldclient, observations=observations)
