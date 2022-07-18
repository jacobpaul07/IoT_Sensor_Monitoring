from dataclasses import dataclass
from typing import List, Any, Optional
from App.Json_Class.DtoUtilities import *


@dataclass
class SerialPortSettings:
    Method: str
    Port: str
    BaudRate: str
    DataBit: str
    StopBit: str
    Timeout: str
    Parity: str
    RTS: str
    DTR: str

    @staticmethod
    def from_dict(obj: Any) -> 'SerialPortSettings':
        assert isinstance(obj, dict)
        Method = from_str(obj.get("Method"))
        Port = from_str(obj.get("Port"))
        BaudRate = from_str(obj.get("Baud Rate"))
        DataBit = from_str(obj.get("Data Bit"))
        StopBit = from_str(obj.get("Stop Bit"))
        Timeout = from_str(obj.get("Timeout"))
        Parity = from_str(obj.get("Parity"))
        RTS = from_str(obj.get("RTS"))
        DTR = from_str(obj.get("DTR"))
        return SerialPortSettings(Method, Port, BaudRate, DataBit, StopBit, Timeout, Parity, RTS, DTR)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Method"] = from_str(self.Method)
        result["Port"] = from_str(self.Port)
        result["Baud Rate"] = from_str(self.BaudRate)
        result["Data Bit"] = from_str(self.DataBit)
        result["Stop Bit"] = from_str(self.StopBit)
        result["Timeout"] = from_str(self.Timeout)
        result["Parity"] = from_str(self.Parity)
        result["RTS"] = from_str(self.RTS)
        result["DTR"] = from_str(self.DTR)
        return result