from dataclasses import dataclass
from App.Json_Class.SerialPortSetting_dto import SerialPortSettings
from App.Json_Class.DtoUtilities import *


@dataclass
class COMPORTProperties:
    Enable: str
    Type: str
    Name: str
    Description: str
    ScanTimems: str
    TimeOutms: str
    RetryCount: str
    AutoRecoverTimes: str
    SerialPortSetting: SerialPortSettings

    @staticmethod
    def from_dict(obj: Any) -> 'COMPORTProperties':
        assert isinstance(obj, dict)
        Enable = from_str(obj.get("Enable"))
        Type = from_str(obj.get("Type"))
        Name = from_str(obj.get("Name"))
        Description = from_str(obj.get("Description"))
        ScanTimems = from_str(obj.get("Scan Time(ms)"))
        TimeOutms = from_str(obj.get("Time Out(ms)"))
        RetryCount = from_str(obj.get("Retry Count"))
        AutoRecoverTimes = from_str(obj.get("Auto Recover Time(s)"))
        SerialPortSetting = SerialPortSettings.from_dict(obj.get("SerialPort Setting"))
        return COMPORTProperties(Enable, Type, Name, Description, ScanTimems, TimeOutms, RetryCount, AutoRecoverTimes, SerialPortSetting)

    def to_dict(self) -> dict:
        result: dict = {"Enable": from_str(self.Enable), "Type": from_str(self.Type), "Name": from_str(self.Name),
                        "Description": from_str(self.Description), "Scan Time(ms)": from_str(self.ScanTimems),
                        "Time Out(ms)": from_str(self.TimeOutms), "Retry Count": from_str(self.RetryCount),
                        "Auto Recover Time(s)": from_str(self.AutoRecoverTimes),
                        "SerialPort Setting": to_class(SerialPortSettings, self.SerialPortSetting)}
        return result
