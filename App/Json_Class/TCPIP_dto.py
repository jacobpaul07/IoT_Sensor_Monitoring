from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable
from App.Json_Class.DtoUtilities import *
@dataclass
class TCPIPs:
    IPAdress: str
    PortNumber: str

    @staticmethod
    def from_dict(obj: Any) -> 'TCPIPs':
        assert isinstance(obj, dict)
        IPAdress = from_str(obj.get("IP Adress"))
        PortNumber = from_str(obj.get("Port Number"))
        return TCPIPs(IPAdress, PortNumber)

    def to_dict(self) -> dict:
        result: dict = {}
        result["IP Adress"] = from_str(self.IPAdress)
        result["Port Number"] = from_str(self.PortNumber)
        return result