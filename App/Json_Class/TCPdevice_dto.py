from dataclasses import dataclass
from typing import Any, List, Optional, TypeVar, Type, cast, Callable
from App.Json_Class.IOTag_dto import IOTag
from App.Json_Class.DtoUtilities import *
from App.Json_Class.TCPdeviceProperties_dto import TCPdeviceProperties


@dataclass
class TCPdevice:
    properties: TCPdeviceProperties
    IOTags: List[IOTag]

    @staticmethod
    def from_dict(obj: Any) -> 'TCPdevice':
        assert isinstance(obj, dict)
        properties = TCPdeviceProperties.from_dict(obj.get("properties"))
        IOTags = from_list(IOTag.from_dict, obj.get("IO Tags"))
        return TCPdevice(properties, IOTags)

    def to_dict(self) -> dict:
        result: dict = {"properties": to_class(TCPdeviceProperties, self.properties),
                        "IO Tags": from_list(lambda x: to_class(IOTag, x), self.IOTags)}
        return result
