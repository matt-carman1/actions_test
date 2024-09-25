from ldclient.models import ModelReturn, ModelCommand
from library.utils import make_unique_name
from helpers.api.actions.model import create_model_via_api, archive_models, update_protocol_via_api
from helpers.api.verification.model import verify_protocol_model_predictions
import pytest

test_protocol_name = 'Protocol'
test_protocol_commands = [ModelCommand(command='${Hello:NUMERIC-INPUT}', driver_id='1')]
test_protocol_predictions = [
    ModelReturn(key="Prediction1", type="REAL", display_name="Prediction1", units="nm", precision=2, tag="DEFAULT"),
    ModelReturn(key="Prediction2", type="BOOLEAN", display_name="Prediction2", units="", precision=0, tag="DEFAULT")
]


def test_protocol_model_predictions(ld_api_client, new_protocol_via_api):
    """
    Testing returns for protocols and models

    1. Create a protocol with multiple returns
    2. Create a model depending on a protocol
    3. Ensure that all predictions in protocols are carried forward to models.
    4. Update the protocol with with another prediction.
    5. Ensure that the new prediction is not carried forward to the model.
    6. Update the model with new predictions.
    7. Ensure that the new model predictions are added.

    :param ld_api_client: LDClient, ldclient object
    :param new_protocol_via_api: Fixture for creating new new protocols
    """

    # ---- Creating a model depending on the protocol ---- #
    model_with_predictions = create_model_via_api(ld_api_client,
                                                  make_unique_name('Model_with_predictions'),
                                                  'description',
                                                  folder=new_protocol_via_api.folder,
                                                  parent=new_protocol_via_api.id)

    verify_protocol_model_predictions(new_protocol_via_api.returns, model_with_predictions.returns)

    # ---- Updating the protocol to add new predictions ---- #
    prediction_to_be_added = [
        ModelReturn(key="Prediction3",
                    type="STRING",
                    display_name="Prediction3",
                    units="nm",
                    precision=0,
                    tag="DEFAULT"),
        ModelReturn(key="Prediction4",
                    type="ATTACHMENT",
                    display_name="Prediction4",
                    units="nm",
                    precision=0,
                    tag="DEFAULT")
    ]

    # Concatenating the old protocol predictions with new predictions
    new_protocol_predictions = test_protocol_predictions + prediction_to_be_added
    sorted_new_protocol_predictions = sorted(new_protocol_predictions, key=lambda x: x.key)

    # Updating the protocol with the new predictions
    new_protocol_via_api.returns = new_protocol_predictions
    updated_protocol = update_protocol_via_api(ld_api_client, new_protocol_via_api.id, new_protocol_via_api)
    sorted_updated_protocol_return = sorted(updated_protocol.returns, key=lambda x: x.key)

    # Verification that protocol predictions are updated
    verify_protocol_model_predictions(sorted_updated_protocol_return, sorted_new_protocol_predictions)

    # Ensuring that updated protocol predictions are not carried forward to model predictions
    updated_model = ld_api_client.model(model_with_predictions.id)
    assert len(updated_model.returns) == len(model_with_predictions.returns), \
        "Models have been updated with new protocol predictions when it should not be"
    assert len(updated_model.returns) != len(updated_protocol.returns), \
        "Models have been updated with new protocol predictions when it should not be"

    # ---- Updating the existing model now to have new predictions types ---- #
    new_model_predictions = [
        ModelReturn(key="Prediction3", type="PROTEIN", display_name="Prediction3", units="", precision=0,
                    tag="DEFAULT"),
        ModelReturn(key="Prediction4", type="LIGAND", display_name="Prediction4", units="", precision=0, tag="DEFAULT")
    ]

    # Concatenating the old model predictions with new predictions
    new_model_predictions = model_with_predictions.returns + new_model_predictions
    sorted_new_model_predictions = sorted(new_model_predictions, key=lambda x: x.key)

    # Updating the model with new predictions now
    model_with_predictions.returns = new_model_predictions
    updated_model = ld_api_client.update_model(model_with_predictions.id, model_with_predictions)
    sorted_updated_model_return = sorted(updated_model.returns, key=lambda x: x.key)

    verify_protocol_model_predictions(sorted_updated_model_return, sorted_new_model_predictions)

    # Archiving dependent models
    archive_models(ld_api_client, [model_with_predictions])
