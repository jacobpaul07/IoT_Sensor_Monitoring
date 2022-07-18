from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable
from App.Json_Class.DtoUtilities import *
from App.Json_Class.COMExtentionProperties_dto import COMExtentionProperties


@dataclass
class COMdeviceProperties:
    Enable: str
    Name: str
    DeviceType: str
    DeviceModel: str
    UnitNumber: str
    Description: str
    AdddevicenameasprefixtoIOTag: str
    ExtentionProperties: COMExtentionProperties

    @staticmethod
    def from_dict(obj: Any) -> 'COMdeviceProperties':
        assert isinstance(obj, dict)
        Enable = from_str(obj.get("Enable"))
        Name = from_str(obj.get("Name"))
        DeviceType = from_str(obj.get("Device Type"))
        DeviceModel = from_str(obj.get("Device Model"))
        UnitNumber = from_str(obj.get("Unit Number"))
        Description = from_str(obj.get("Description"))
        AdddevicenameasprefixtoIOTag = from_str(obj.get("Add device name as prefix to IO Tag"))
        ExtentionProperties = COMExtentionProperties.from_dict(obj.get("Extention Properties"))
        return COMdeviceProperties(Enable, Name, DeviceType, DeviceModel, UnitNumber, Description,
                                   AdddevicenameasprefixtoIOTag, ExtentionProperties)

    def to_dict(self) -> dict:
        result: dict = {"Enable": from_str(self.Enable), "Name": from_str(self.Name),
                        "Device Type": from_str(self.DeviceType), "Device Model": from_str(self.DeviceModel),
                        "Unit Number": from_str(self.UnitNumber), "Description": from_str(self.Description),
                        "Add device name as prefix to IO Tag": from_str(self.AdddevicenameasprefixtoIOTag),
                        "Extention Properties": to_class(COMExtentionProperties, self.ExtentionProperties)}
        return result
