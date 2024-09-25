from ldclient import LDClient
from typing import List, Optional

from library.api.extended_ldclient.models import Reaction
from library.api.extended_ldclient.paths import ENUMERATION_PATH, REACTIONS_PATH, STARTUP_HOOKS_PATH
from library.api.extended_ldclient.requests import RGroupEnumerationRequest, ReactionEnumerationRequest
from library.api.extended_ldclient.responses import RGroupEnumerationPreview, EnumerationResponse, \
    ReactionEnumerationPreview


class ExtendedLDClient(LDClient):
    """
    A subclass of LDClient with added functionality used in API tests.  For example, these could be
    endpoints that we don't want to expose in LDClient proper, but do want to access in API testing.
    """

    def rgroup_enumeration_preview(self, request: RGroupEnumerationRequest) -> RGroupEnumerationPreview:
        """
        This endpoint is used in the preview pane on the frontend

        :return: list of products
        """
        response = self.client.post(service_path=ENUMERATION_PATH, path='/r_group', json_data=request.as_dict())
        return RGroupEnumerationPreview.from_dict(response)

    def rgroup_enumeration_async(self, request: RGroupEnumerationRequest) -> str:
        """
        This endpoint is used when actually running the R-Group enumeration

        :return: The async task ID
        """
        response = self.client.post(service_path=ENUMERATION_PATH,
                                    path='/r_group/async_task',
                                    json_data=request.as_dict())
        return response['async_task_id']

    def rgroup_enumeration_sync(self, request: RGroupEnumerationRequest) -> EnumerationResponse:
        async_task_id = self.rgroup_enumeration_async(request)
        result_url = self.wait_and_get_result_url(async_task_id)
        return EnumerationResponse.from_dict(self.get_task_result(result_url))

    def reaction_enumeration_preview(self, request: ReactionEnumerationRequest) -> ReactionEnumerationPreview:
        """
        This endpoint is used in the preview pane on the frontend

        :return: list of products
        """
        response = self.client.post(service_path=ENUMERATION_PATH, path='/reaction', json_data=request.as_dict())
        return ReactionEnumerationPreview.from_dict(response)

    def reaction_enumeration_async(self, request: ReactionEnumerationRequest) -> str:
        """
        This endpoint is used when actually running the Reaction enumeration

        :return: The async task ID
        """
        response = self.client.post(service_path=ENUMERATION_PATH,
                                    path='/reaction/async_task',
                                    json_data=request.as_dict())
        return response['async_task_id']

    def reaction_enumeration_sync(self, request: ReactionEnumerationRequest) -> EnumerationResponse:
        async_task_id = self.reaction_enumeration_async(request)
        result_url = self.wait_and_get_result_url(async_task_id)
        return EnumerationResponse.from_dict(self.get_task_result(result_url))

    def list_reactions(self) -> List[Reaction]:
        """
        Fetches all saved reactions on the server, including schrodinger library & user defined.

        :return: list of save reactions
        """
        return Reaction.from_list(self.client.get(service_path=REACTIONS_PATH, path='/'))

    def get_reaction_from_name(self, reaction_name: str) -> Optional[Reaction]:
        """
        Retrieves a saved reaction given the name

        :param reaction_name: name of reaction to get

        :return: reaction object

        :raises: :class:`RuntimeError`
        """
        reactions: List[Reaction] = self.list_reactions()
        matching_reactions = [r for r in reactions if r.name == reaction_name]
        if len(matching_reactions) == 0:
            return None
        if len(matching_reactions) > 1:
            raise RuntimeError(f"Found more than one reaction with name {reaction_name}")
        return matching_reactions[0]

    def create_reaction(self, reaction: Reaction) -> Reaction:
        """
        Saves a new user-defined reaction

        :param reaction: the reaction to create

        :return: the persisted reaction
        """
        return Reaction.from_dict(self.client.post(service_path=REACTIONS_PATH, path='/', json_data=reaction.as_dict()))

    def get_startup_hooks_status(self):
        """
        Gets the pass/fail status for each startup hook

        :rtype: :class:`dict`
        :return: a dictionary mapping Startup hooks name to pass/fail status.
        """
        return self.client.get(service_path=STARTUP_HOOKS_PATH, path='')
