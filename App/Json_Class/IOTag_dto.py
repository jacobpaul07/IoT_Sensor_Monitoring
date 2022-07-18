from dataclasses import dataclass
from App.Json_Class.DtoUtilities import *

@dataclass
class IOTag:
    Name: str
    SignalType: str
    Conversion: str
    Address: str
    SpanHigh: str
    SpanLow: str
    UnitHigh: str
    UnitLow: str
    InitialValue: str
    ScanRate: str
    ReadWrite: str
    initvalue: str
    Description: str

    @staticmethod
    def from_dict(obj: Any) -> 'IOTag':
        assert isinstance(obj, dict)
        Name = from_str(obj.get("Name"))
        SignalType = from_str(obj.get("Signal Type"))
        Conversion = from_str(obj.get("Conversion"))
        Address = from_str(obj.get("Address"))
        SpanHigh = from_str(obj.get("Span High"))
        SpanLow = from_str(obj.get("Span Low"))
        UnitHigh = from_str(obj.get("Unit High"))
        UnitLow = from_str(obj.get("Unit Low"))
        InitialValue = from_str(obj.get("Initial Value"))
        ScanRate = from_str(obj.get("Scan Rate"))
        ReadWrite = from_str(obj.get("Read Write"))
        initvalue = from_str(obj.get("initvalue"))
        Description = from_str(obj.get("Description"))
        return IOTag(Name, SignalType, Conversion, Address, SpanHigh, SpanLow,UnitHigh, UnitLow, InitialValue, ScanRate, ReadWrite, initvalue, Description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Name"] = from_str(self.Name)
        result["Signal Type"] = from_str(self.SignalType)
        result["Conversion"] = from_str(self.Conversion)
        result["Address"] = from_str(self.Address)
        result["Span High"] = from_str(self.SpanHigh)
        result["Span Low"] = from_str(self.SpanLow)
        result["Unit High"] = from_str(self.UnitHigh)
        result["Unit Low"] = from_str(self.UnitLow)
        result["Initial Value"] = from_str(self.InitialValue)
        result["Scan Rate"] = from_str(self.ScanRate)
        result["Read Write"] = from_str(self.ReadWrite)
        result["initvalue"] = from_str(self.initvalue)
        result["Description"] = from_str(self.Description)
        return result