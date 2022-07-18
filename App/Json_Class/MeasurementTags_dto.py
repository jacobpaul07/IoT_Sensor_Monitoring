from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Callable, Type, cast
from App.Json_Class.DtoUtilities import *



@dataclass
class MeasurementTags:
    TagName: str
    TagValue: str
    Status: str
    DeviceName: Optional[str] = None
    DeviceType: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MeasurementTags':
        assert isinstance(obj, dict)
        TagName = from_str(obj.get("TagName"))
        TagValue = from_str(obj.get("TagValue"))
        Status = from_str(obj.get("Status"))
        DeviceName = from_union([from_str, from_none], obj.get("Device Name"))
        DeviceType = from_union([from_str, from_none], obj.get("Device-Type"))
        return MeasurementTags(TagName, TagValue, Status, DeviceName, DeviceType)

    def to_dict(self) -> dict:
        result: dict = {}
        result["TagName"] = from_str(self.TagName)
        result["TagValue"] = from_str(self.TagValue)
        result["Status"] = from_str(self.Status)
        result["Device Name"] = from_union([from_str, from_none], self.DeviceName)
        result["Device-Type"] = from_union([from_str, from_none], self.DeviceType)
        return result
