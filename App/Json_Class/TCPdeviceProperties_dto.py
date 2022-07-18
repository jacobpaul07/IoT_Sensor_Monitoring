from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable
from App.Json_Class.TCPIP_dto import TCPIPs
from App.Json_Class.DtoUtilities import *
from App.Json_Class.TCPExtentionProperties_dto import TCPExtentionProperties


@dataclass
class TCPdeviceProperties:
    Enable: str
    Name: str
    DeviceType: str
    DeviceModel: str
    UnitNumber: str
    Description: str
    AdddevicenameasprefixtoIOTag: str
    TCPIP: TCPIPs
    ExtentionProperties: TCPExtentionProperties

    @staticmethod
    def from_dict(obj: Any) -> 'TCPdeviceProperties':
        assert isinstance(obj, dict)
        Enable = from_str(obj.get("Enable"))
        Name = from_str(obj.get("Name"))
        DeviceType = from_str(obj.get("Device Type"))
        DeviceModel = from_str(obj.get("Device Model"))
        UnitNumber = from_str(obj.get("Unit Number"))
        Description = from_str(obj.get("Description"))
        AdddevicenameasprefixtoIOTag = from_str(obj.get("Add device name as prefix to IO Tag"))
        TCPIP = TCPIPs.from_dict(obj.get("TCP/IP"))
        ExtentionProperties = TCPExtentionProperties.from_dict(obj.get("Extention Properties"))
        return TCPdeviceProperties(Enable, Name, DeviceType, DeviceModel, UnitNumber, Description, AdddevicenameasprefixtoIOTag, TCPIP, ExtentionProperties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Enable"] = from_str(self.Enable)
        result["Name"] = from_str(self.Name)
        result["Device Type"] = from_str(self.DeviceType)
        result["Device Model"] = from_str(self.DeviceModel)
        result["Unit Number"] = from_str(self.UnitNumber)
        result["Description"] = from_str(self.Description)
        result["Add device name as prefix to IO Tag"] = from_str(self.AdddevicenameasprefixtoIOTag)
        result["TCP/IP"] = to_class(TCPIPs, self.TCPIP)
        result["Extention Properties"] = to_class(TCPExtentionProperties, self.ExtentionProperties)
        return result
