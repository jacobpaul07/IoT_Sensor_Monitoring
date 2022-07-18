# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = edge_class_from_dict(json.loads(json_string))

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, TypeVar, Callable, Type, cast
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class GpsData:
    imei: str
    latitude: str
    no_s: str
    longitude: str
    eo_w: str
    bat_level: str
    signal_strength: int
    status: str
    time_stamp: str

    @staticmethod
    def from_dict(obj: Any) -> 'GpsData':
        assert isinstance(obj, dict)
        imei = from_str(obj.get("IMEI"))
        latitude = from_str(obj.get("latitude"))
        no_s = from_str(obj.get("NoS"))
        longitude = from_str(obj.get("longitude"))
        eo_w = from_str(obj.get("EoW"))
        bat_level = from_str(obj.get("batLevel"))
        signal_strength = int(from_str(obj.get("SignalStrength")))
        status = from_str(obj.get("Status"))
        time_stamp = from_str(obj.get("TimeStamp"))
        return GpsData(imei, latitude, no_s, longitude, eo_w, bat_level, signal_strength, status, time_stamp)

    def to_dict(self) -> dict:
        result: dict = {"IMEI": from_str(self.imei), "latitude": from_str(self.latitude), "NoS": from_str(self.no_s),
                        "longitude": from_str(self.longitude), "EoW": from_str(self.eo_w),
                        "batLevel": from_str(self.bat_level), "SignalStrength": from_str(str(self.signal_strength)),
                        "Status": from_str(self.status), "TimeStamp": from_str(self.time_stamp)}
        return result


@dataclass
class SensorDatum:
    tag_name: str
    value: float

    @staticmethod
    def from_dict(obj: Any) -> 'SensorDatum':
        assert isinstance(obj, dict)
        tag_name = from_str(obj.get("tagName"))
        value = from_float(obj.get("value"))
        return SensorDatum(tag_name, value)

    def to_dict(self) -> dict:
        result: dict = {"tagName": from_str(self.tag_name), "value": to_float(self.value)}
        return result


@dataclass
class EdgeClass:
    sensor_data: List[SensorDatum]
    last_updated_timestamp: datetime
    gps_data: GpsData

    @staticmethod
    def from_dict(obj: Any) -> 'EdgeClass':
        assert isinstance(obj, dict)
        sensor_data = from_list(SensorDatum.from_dict, obj.get("sensor_data"))
        last_updated_timestamp = from_datetime(obj.get("last_updated_timestamp"))
        gps_data = GpsData.from_dict(obj.get("gps_data"))
        return EdgeClass(sensor_data, last_updated_timestamp, gps_data)

    def to_dict(self) -> dict:
        result: dict = {"sensor_data": from_list(lambda x: to_class(SensorDatum, x), self.sensor_data),
                        "last_updated_timestamp": self.last_updated_timestamp.isoformat(),
                        "gps_data": to_class(GpsData, self.gps_data)}
        return result


def edge_class_from_dict(s: Any) -> EdgeClass:
    return EdgeClass.from_dict(s)


def edge_class_to_dict(x: EdgeClass) -> Any:
    return to_class(EdgeClass, x)
