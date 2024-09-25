from typing import List, Optional

from library.api.extended_ldclient.base import BaseModel


class RGroupEnumerationPreview(BaseModel):
    products: List[str]


class ReactionEnumerationPreview(BaseModel):
    products: List[str]


class EnumerationResponse(BaseModel):
    live_report_id: str
    promise_id: Optional[str]
