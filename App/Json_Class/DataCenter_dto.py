from dataclasses import dataclass
from typing import Any, List, Optional, TypeVar, Type, cast, Callable
from App.Json_Class.DtoUtilities import *
from App.Json_Class.COMPort_dto import Comport
from App.Json_Class.TCP_dto import TCPs


@dataclass
class DataCenters:
    COM1: Comport
    COM2: Comport
    TCP: TCPs

    @staticmethod
    def from_dict(obj: Any) -> 'DataCenters':
        assert isinstance(obj, dict)
        COM1 = Comport.from_dict(obj.get("COM1"))
        COM2 = Comport.from_dict(obj.get("COM2"))
        TCP = TCPs.from_dict(obj.get("TCP"))
        return DataCenters(COM1, COM2, TCP)

    def to_dict(self) -> dict:
        result: dict = {"COM1": to_class(Comport, self.COM1), "COM2": to_class(Comport, self.COM2),
                        "TCP": to_class(TCPs, self.TCP)}
        return result
