from dataclasses import dataclass
from typing import Any, List, Optional, TypeVar, Type, cast, Callable
from App.Json_Class.DtoUtilities import *

@dataclass
class TCPExtentionProperties:
    DeviceAddress: str
    UseUDP: str

    @staticmethod
    def from_dict(obj: Any) -> 'TCPExtentionProperties':
        assert isinstance(obj, dict)
        DeviceAddress = from_str(obj.get("Device Address"))
        UseUDP = from_str(obj.get("Use UDP"))
        return TCPExtentionProperties(DeviceAddress, UseUDP)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Device Address"] = from_str(self.DeviceAddress)
        result["Use UDP"] = from_str(self.UseUDP)
        return result
