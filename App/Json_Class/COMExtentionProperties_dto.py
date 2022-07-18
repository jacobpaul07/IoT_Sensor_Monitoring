from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from App.Json_Class.DtoUtilities import *


@dataclass
class COMExtentionProperties:
    CheckSum: str
    Protocol: str
    ModbusDigitalblocksize: str
    ModbusAnalogblockSize: str

    @staticmethod
    def from_dict(obj: Any) -> 'COMExtentionProperties':
        assert isinstance(obj, dict)
        CheckSum = from_str(obj.get("CheckSum"))
        Protocol = from_str(obj.get("Protocol"))
        ModbusDigitalblocksize = from_str(obj.get("ModbusDigital block size"))
        ModbusAnalogblockSize = from_str(obj.get("Modbus Analog block Size"))
        return COMExtentionProperties(CheckSum, Protocol, ModbusDigitalblocksize, ModbusAnalogblockSize)

    def to_dict(self) -> dict:
        result: dict = {"CheckSum": from_str(self.CheckSum), "Protocol": from_str(self.Protocol),
                        "ModbusDigital block size": from_str(self.ModbusDigitalblocksize),
                        "Modbus Analog block Size": from_str(self.ModbusAnalogblockSize)}
        return result