from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable
from App.Json_Class.DtoUtilities import *

@dataclass
class TCPProperties:
    Enable: str
    Type: str
    Name: str
    Description: str
    ScanTimems: str
    TimeOutms: str
    RetryCount: str
    AutoRecoverTimes: str

    @staticmethod
    def from_dict(obj: Any) -> 'TCPProperties':
        assert isinstance(obj, dict)
        Enable = from_str(obj.get("Enable"))
        Type = from_str(obj.get("Type"))
        Name = from_str(obj.get("Name"))
        Description = from_str(obj.get("Description"))
        ScanTimems = from_str(obj.get("Scan Time(ms)"))
        TimeOutms = from_str(obj.get("Time Out(ms)"))
        RetryCount = from_str(obj.get("Retry Count"))
        AutoRecoverTimes = from_str(obj.get("Auto Recover Time(s)"))
        return TCPProperties(Enable, Type, Name, Description, ScanTimems, TimeOutms, RetryCount, AutoRecoverTimes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Enable"] = from_str(self.Enable)
        result["Type"] = from_str(self.Type)
        result["Name"] = from_str(self.Name)
        result["Description"] = from_str(self.Description)
        result["Scan Time(ms)"] = from_str(self.ScanTimems)
        result["Time Out(ms)"] = from_str(self.TimeOutms)
        result["Retry Count"] = from_str(self.RetryCount)
        result["Auto Recover Time(s)"] = from_str(self.AutoRecoverTimes)
        return result
