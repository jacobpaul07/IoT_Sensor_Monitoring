from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Callable, Type, cast
from App.Json_Class.DtoUtilities import *
from App.Json_Class.MeasurementTags_dto import MeasurementTags


@dataclass
class Stations:
    Enable: str
    API: str
    UpdateTime: str
    MeasurementTag: List[MeasurementTags]
    StationID: Optional[str] = None
    DeviceID: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Stations':
        assert isinstance(obj, dict)
        Enable = from_str(obj.get("Enable"))
        API = from_str(obj.get("API"))
        UpdateTime = from_str(obj.get("UpdateTime"))
        MeasurementTag = from_list(MeasurementTags.from_dict, obj.get("MeasurementTag"))
        StationID = from_union([from_str, from_none], obj.get("StationID"))
        DeviceID = from_union([from_str, from_none], obj.get("DeviceID"))
        return Stations(Enable, API, UpdateTime, MeasurementTag, StationID, DeviceID)

    def to_dict(self) -> dict:
        result: dict = {"Enable": from_str(self.Enable), "API": from_str(self.API),
                        "UpdateTime": from_str(self.UpdateTime),
                        "MeasurementTag": from_list(lambda x: to_class(MeasurementTags, x), self.MeasurementTag),
                        "StationID": from_union([from_str, from_none], self.StationID),
                        "DeviceID": from_union([from_str, from_none], self.DeviceID)}
        return result

