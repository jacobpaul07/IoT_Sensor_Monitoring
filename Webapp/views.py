import datetime
import json
import os
import sys
import time
import pandas as pd
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseBadRequest
from App.Json_Class import index as config, Edge
from typing import Any, List, Optional, TypeVar, Type, cast, Callable

from MongoDB_Main import Document as Doc
from App.Json_Class.EdgeDeviceProperties_dto import EdgeDeviceProperties
from App.RTUReaders.modbus_rtu import modbus_rtu
import App.globalsettings as appsetting
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.
from Webapp.configHelper import ConfigComProperties, ConfigTcpProperties, ConfigComDevicesProperties, \
    ConfigTCPDevicesProperties, ConfigPpmpProperties, ConfigDevicesIOTags, ConfigPpmpStation


class ConfigIpChange(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        ip: str = requestData["ip"]
        port: str = requestData["port"]
        deviceName: str = requestData["deviceName"]

        jsonData: Edge = config.read_setting()
        for tcpDevice in jsonData.edgedevice.DataCenter.TCP.devices:
            if tcpDevice.properties.Name == deviceName:
                tcpDevice.properties.TCPIP.IPAdress = ip
                tcpDevice.properties.TCPIP.PortNumber = port
        print(jsonData)
        updated_json_data = jsonData.to_dict()
        print(updated_json_data)
        config.write_setting(updated_json_data)

        return HttpResponse('success', "application/json")


class StartRtuService(APIView):
    @staticmethod
    def post(request):
        StartRtuService.start_rtu()
        return HttpResponse('success', "application/json")

    @staticmethod
    def start_rtu():
        appsetting.startRtuService = True
        modbus_rtu()


class ConfigGatewayProperties(APIView):

    def post(self, request):
        data = request.body.decode("UTF-8")
        requestData = json.loads(data)
        jsonData: Edge = config.read_setting()
        edgeDeviceProperties = jsonData.edgedevice.properties.to_dict()
        for key in requestData:
            value = requestData[key]
            for objectKey in edgeDeviceProperties:
                # for device_key in properties:
                if objectKey == key:
                    edgeDeviceProperties[key] = value

        jsonData.edgedevice.properties = EdgeDeviceProperties.from_dict(edgeDeviceProperties)
        updated_json_data = jsonData.to_dict()
        print(updated_json_data)
        config.write_setting(updated_json_data)

        return HttpResponse('success', "application/json")


class ConfigDataCenterProperties(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        payLoadData = requestData["data"]
        deviceType: str = requestData["deviceType"]
        print("DeviceType:", deviceType)
        if deviceType == "COM1" or deviceType == "COM2":
            ConfigComProperties().updateComPortProperties(requestData=payLoadData, portName=deviceType)
        if deviceType == "TCP":
            ConfigTcpProperties().updateTcpPortProperties(requestData=payLoadData)

        return HttpResponse("Success", "application/json")


class ConfigDataCenterDeviceProperties(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        payLoadData = requestData["data"]
        deviceType: str = requestData["deviceType"]
        deviceName: str = requestData["deviceName"]
        print("DeviceType:", deviceType)
        if deviceType == "COM1" or deviceType == "COM2":
            response = ConfigComDevicesProperties().updateComDeviceProperties(payLoadData, deviceType, deviceName)
            if response == 'success':
                return HttpResponse(response, "application/json")
            else:
                return HttpResponseBadRequest(response)

        if deviceType == "TCP":
            response = ConfigTCPDevicesProperties().updateTCPDeviceProperties(payLoadData, deviceName)
            if response == 'success':
                return HttpResponse(response, "application/json")
            else:
                return HttpResponseBadRequest(response)


class ConfigDataCenterDeviceIOTags(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        payLoadData = requestData["data"]
        deviceType: str = requestData["deviceType"]
        deviceName: str = requestData["deviceName"]
        print("DeviceType:", deviceType)
        if deviceType.startswith("COM") and len(deviceType) == 4:
            response = ConfigDevicesIOTags().updateComIoTags(payLoadData, deviceType, deviceName)
            if response == 'success':
                return HttpResponse(response, "application/json")
            else:
                return HttpResponseBadRequest(response)

        if deviceType == "TCP":
            response = ConfigDevicesIOTags().updateTcpIoTags(payLoadData, deviceName)
            if response == 'success':
                return HttpResponse(response, "application/json")
            else:
                return HttpResponseBadRequest(response)


class ConfigPpmpStations(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        payLoadData = requestData["data"]
        deviceType: str = requestData["deviceType"]
        print("DeviceType:", deviceType)
        if deviceType == "PPMP":
            response = ConfigPpmpStation().updateStations(payLoadData)
            if response == 'success':
                return HttpResponse(response, "application/json")
            else:
                return HttpResponseBadRequest(response)


class ReadDeviceSettings(APIView):

    def get(self, request):
        jsonData: Edge = config.read_setting()
        jsonResponse = json.dumps(jsonData.to_dict(), indent=4)

        return HttpResponse(jsonResponse, "application/json")


class startWebSocket(APIView):

    def post(self, request):
        appsetting.runWebSocket = True
        # thread = threading.Thread(
        #     target=sendDataToWebSocket,
        #     args=())

        # Starting the Thread
        # thread.start()
        return HttpResponse('success', "application/json")


class stopWebSocket(APIView):

    def post(self, request):
        appsetting.runWebSocket = False

        return HttpResponse('success', "application/json")


def sendDataToWebSocket():
    while appsetting.runWebSocket:
        text_data = str(datetime.datetime.now())

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("notificationGroup", {
            "type": "chat_message",
            "message": text_data
        })
        time.sleep(10)


class ConfigDataServiceProperties(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        payLoadData = requestData["data"]
        deviceType: str = requestData["deviceType"]
        print("DeviceType:", deviceType)
        if deviceType == "PPMP":
            response = ConfigPpmpProperties().updatePpmpProperties(requestData=payLoadData)
        else:
            response = "No PPMP"
        #     ConfigTcpProperties().updateTcpPortProperties(requestData=payLoadData)

        if response == 'success':
            return HttpResponse(response, "application/json")
        else:
            return HttpResponseBadRequest(response)


class GetSpecificTimeData(APIView):
    @staticmethod
    def get(request):
        try:
            date_time = request.GET.get("date")
            machine_id = "MID-01"
            db_log = Doc().SpecificDate_Document(Timestamp=date_time, filterField="last_updated_timestamp",
                                                 col="LiveData", machineID=machine_id)

            if db_log:
                return HttpResponse(json.dumps(db_log, indent=4, default=str), "application/json")
            else:
                bad_response = "No Data Available at " + date_time
                print(bad_response)
                return HttpResponseBadRequest(bad_response)

        except Exception as ex:
            print("Error in WebApp/Views.py -> GetSpecificTimeData", ex)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)


class GetLiveData(APIView):
    @staticmethod
    def get(request):
        try:
            machine_id = "MID-01"
            db_log = Doc().Read_Document(col="LiveData", DeviceID=machine_id, filterField="last_updated_timestamp")

            if db_log:
                return HttpResponse(json.dumps(db_log, indent=4, default=str), "application/json")
            else:
                bad_response = "No Data Available"
                print(bad_response)
                return HttpResponseBadRequest(bad_response)

        except Exception as ex:
            print("Error in WebApp/Views.py -> GetSpecificTimeData", ex)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
