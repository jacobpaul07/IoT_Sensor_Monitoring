from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable
from App.Json_Class.DtoUtilities import *
from App.Json_Class.COMDevices_dto import COMdevice
from App.Json_Class.COMProperties_dto import COMPORTProperties


@dataclass
class Comport:
    properties: COMPORTProperties
    devices: List[COMdevice]

    @staticmethod
    def from_dict(obj: Any) -> 'Comport':
        assert isinstance(obj, dict)
        properties = COMPORTProperties.from_dict(obj.get("properties"))
        COMdevices = from_list(COMdevice.from_dict, obj.get("devices"))
        return Comport(properties, COMdevices)

    def to_dict(self) -> dict:
        result: dict = {"properties": to_class(COMPORTProperties, self.properties),
                        "devices": from_list(lambda x: to_class(COMdevice, x), self.devices)}
        return result
