import threading
# from random import randint
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from App.MQTT.mqtt_publisher import mqtt_publish
# from App.Utilities import read_result_file, write_result_file
from App.Json_Class.COMProperties_dto import COMPORTProperties
from App.Json_Class.COMDevices_dto import *
from App.Json_Class.SerialPortSetting_dto import SerialPortSettings
import datetime
# from MongoDB_Main import Document as Doc


def sentLiveData(data):
    text_data = json.dumps(data, indent=4)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("notificationGroup", {
        "type": "chat_message",
        "message": text_data
    })


def ReadRTU(settings: SerialPortSettings, ComDevices: COMdevice, comProperties: COMPORTProperties, threadsCount,
            callback, com):
    success = True
    datas_list = []

    if ComDevices.properties.Enable == "True":
        c = ModbusClient(method=settings.Method, port=settings.Port, timeout=int(settings.Timeout),
                         stopbits=int(settings.StopBit), bytesize=int(settings.DataBit), parity=settings.Parity,
                         baudrate=int(settings.BaudRate))

        # open or reconnect TCP to server
        if not c.connect():
            print("unable to connect to", settings.Port)
        # if open() is ok, read register
        try:
            if c.connect():
                # if True:
                # read 8 registers at address 0, store result in regs list

                for tags in ComDevices.IOTags:
                    register_data = c.read_input_registers(address=int(tags.Address),
                                                           count=1,
                                                           unit=int(ComDevices.properties.UnitNumber))
                    registerValue = register_data.registers

                    data = {
                        "tagName": tags.Name,
                        "value": registerValue[0] / 10,
                    }

                    datas_list.append(data)
                mqtt_publish(message=datas_list)
                sentLiveData(datas_list)

                print(datas_list)
                c.close()

                # result_file_contents = read_result_file()
                # result_file_contents["sensor_data"]: list = datas_list
                # result_file_contents["last_updated_timestamp"] = str(time_stamp)
                # datas_list = result_file_contents
                # sentLiveData(result_file_contents)
                # col = "ModbusRTU"
                # # Update Json Data
                # write_result_file(result_file_contents)
                # # Write data to DB
                # Doc().DB_Write(result_file_contents, col)

        except Exception as exception:
            success = False
            print("Device is not Connected Error:", exception)

        thread = threading.Thread(
            target=callback,
            args=(settings, ComDevices, comProperties, threadsCount, datas_list, success, com)
        )
        thread.start()

    return datas_list
