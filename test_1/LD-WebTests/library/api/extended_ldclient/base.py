from enum import Enum

from pydantic import BaseModel as PydanticBaseModel
from typing import Dict, List, Optional


class LDEnum(str, Enum):

    @classmethod
    def from_str(cls, value):
        return cls(value.lower())

    # For if enum value isn't found - then we try case insensitive
    @classmethod
    def _missing_(cls, name):
        for member in cls:
            if member.value.lower() == name.lower():
                return member


class BaseModel(PydanticBaseModel):
    """
    NOTE(badlato): This is a POC of a desired future state of LDClient (LDIDEAS-4725)
     As of August 2021, this is blocked by ldclient's support for hacky installations that do not install
     ldclient's listed dependencies.

    Relevant Intellij plugin: https://plugins.jetbrains.com/plugin/12861-pydantic
    """

    # Pydantic config
    class Config:
        use_enum_values = True

    # @deprecated('9.0', replacement=':meth:`~pydantic.BaseModel.dict`')
    def as_dict(self):
        """
        :return: The instance as a dict
        :rtype: :class:`dict`
        """
        return super().dict()

    # @deprecated('9.0', replacement=':meth:`~pydantic.BaseModel.json`')
    def as_json(self, **kwargs):
        """
        :return: The instance as a Json string
        """
        return super().json(**kwargs)

    @staticmethod
    def as_list(models):
        return [model.as_dict() for model in models or []]

    @classmethod
    def from_dict(cls, data):
        return super().parse_obj(data)

    @classmethod
    def from_json(cls, data):
        return super().parse_raw(data)

    @classmethod
    def from_list(cls, arr):
        return [cls.from_dict(elem) for elem in arr]
