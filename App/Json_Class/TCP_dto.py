from dataclasses import dataclass
from typing import Any, List, Optional, TypeVar, Type, cast, Callable
from App.Json_Class.TCPdevice_dto import TCPdevice
from App.Json_Class.DtoUtilities import *
from App.Json_Class.TCPProperties_dto import TCPProperties

@dataclass
class TCPs:
    properties: TCPProperties
    devices: List[TCPdevice]

    @staticmethod
    def from_dict(obj: Any) -> 'TCPs':
        assert isinstance(obj, dict)
        properties = TCPProperties.from_dict(obj.get("properties"))
        TCPdevices = from_list(TCPdevice.from_dict, obj.get("devices"))
        return TCPs(properties, TCPdevices)

    def to_dict(self) -> dict:
        result: dict = {}
        result["properties"] = to_class(TCPProperties, self.properties)
        result["devices"] = from_list(lambda x: to_class(TCPdevice, x), self.devices)
        return result