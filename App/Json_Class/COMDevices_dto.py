from dataclasses import dataclass
from typing import Any, List, Optional, TypeVar, Type, cast, Callable
from App.Json_Class.IOTag_dto import IOTag
from App.Json_Class.COMdeviceProperties_dto import COMdeviceProperties
from App.Json_Class.DtoUtilities import *


@dataclass
class COMdevice:
    properties: COMdeviceProperties
    IOTags: List[IOTag]

    @staticmethod
    def from_dict(obj: Any) -> 'COMdevice':
        assert isinstance(obj, dict)
        properties = COMdeviceProperties.from_dict(obj.get("properties"))
        IOTags = from_list(IOTag.from_dict, obj.get("IO Tags"))
        return COMdevice(properties, IOTags)

    def to_dict(self) -> dict:
        result: dict = {"properties": to_class(COMdeviceProperties, self.properties),
                        "IO Tags": from_list(lambda x: to_class(IOTag, x), self.IOTags)}
        return result
