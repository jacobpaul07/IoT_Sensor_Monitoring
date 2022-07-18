import json
import os
import sys
import datetime
import pytz
from App.json_class import EdgeClass
from App.Utilities import write_result_file, read_result_file, read_class_result_file


def convert_LOGIN_data(login_data):
    """
    Function that'll convert Raw LOGIN data to Readable JSON Object
    """
    # --------- Headers for final dictionary ---------
    HEADERS = ['Live/Memory', 'Signature', 'IMEI', 'Message Type', 'Sequence No', 'CHECKSUM']

    # Result dictionary
    result = {}

    # --------- Data Processing ---------
    for index, header in enumerate(HEADERS):
        result[header] = login_data[index]

    return result


def convert_GPS_data(gps_data):
    """
    Function that'll convert Raw GPS data to Readable JSON Object
    """

    if len(gps_data) == 23:
        # --------- Headers for final dictionary ---------
        HEADERS = ['Live/Memory', 'Signature', 'IMEI', 'Message Type', 'Sequence No', 'Time (GMT)', 'Date',
                   'valid/invalid', 'Latitude', 'Longitude', 'Speed (knots)', 'Angle of motion', 'Odometer (KM)',
                   'Internal battery Level (Volts)', 'Signal Strength', 'Mobile country code', 'Mobile network code',
                   'Cell id', 'Location area code',
                   '#Ignition(0/1), RESERVED ,Harsh Braking / Acceleration//Non(0/2/3),Main power status(0/1)',
                   'Over speeding', 'Signature', 'CHECKSUM']

        # Result dictionary
        result = {}

        # --------- Data Processing ---------
        for index, header in enumerate(HEADERS):
            result[header] = gps_data[index]

        return result

    else:
        # --------- Headers for final dictionary ---------
        HEADERS = ['Live/Memory', 'Signature', 'IMEI', 'Message Type', 'Sequence No', 'Time (GMT)', 'Date',
                   'valid/invalid', 'Latitude', 'North/South', 'Longitude', 'East/West', 'Speed (knots)',
                   'Angle of motion', 'Odometer (KM)', 'Internal battery Level (Volts)', 'Signal Strength',
                   'Mobile country code', 'Mobile network code', 'Cell id', 'Location area code',
                   '#Ignition(0/1), RESERVED ,Harsh Braking / Acceleration//Non(0/2/3),Main power status(0/1)',
                   'Over speeding', 'Signature', 'CHECKSUM']

        # Result dictionary
        result = {}

        # --------- Data Processing ---------
        for index, header in enumerate(HEADERS):
            result[header] = gps_data[index]

        return result


def convert_OBD_data(obd_data):
    """
    Function that'll convert Raw OBD data to Readable JSON Object
    """

    # --------- Headers for final dictionary ---------
    HEADERS = ['Live/Memory', 'Signature', 'IMEI', 'Message Type', 'Sequence No', 'Time (GMT)', 'Date', 'OBD Protocol']

    # Result dictionary
    result = {}

    # --------- Data processing ---------
    first_half_raw = obd_data[:8]
    second_half_raw = obd_data[8:-1]

    # --------- First Half Data Processing ---------
    for index, header in enumerate(HEADERS):
        result[header] = first_half_raw[index]

    # --------- Second Half Data Processing ---------
    for pid in second_half_raw:
        i = pid.split(':')
        if len(i) > 1:
            result[i[0]] = i[1]

    return result


def convert_raw_to_information(input_data):
    """
    Function that'll convert Raw input from OBD to formatted dictionary containing all the information
    needed for the UI
    """
    try:
        IST = pytz.timezone('Asia/Kolkata')
        dateTimeIND = datetime.datetime.now(IST).strftime("%Y-%m-%dT%H:%M:%S.%f")
        # --------- Data decoding from byte to str ---------
        input_file = input_data.decode("UTF-8", errors='ignore')

        # --------- Data splitting based on comma ---------
        input_file = input_file.replace(';', ',')
        raw_data = input_file.split(',')
        # DB Collection
        col: str = "OBD_Device_Status"
        colHistory: str = "OBD_Device_Status_History"
        # --------- Check for Login packet ---------
        if len(raw_data) < 8:
            login_data = convert_LOGIN_data(raw_data)
            return login_data

        # --------- GPS Data ---------
        elif raw_data[1] == "ATL":
            read_package: EdgeClass = read_class_result_file()
            gps_data_object = read_package.gps_data
            gps_data = convert_GPS_data(raw_data)

            # MongoDB Device Status Data
            if raw_data[0] == "L":
                if not gps_data["Latitude"] == "":
                    gps_data_object.imei = gps_data["IMEI"]
                    gps_data_object.latitude = gps_data["Latitude"]
                    gps_data_object.NoS = gps_data["North/South"]
                    gps_data_object.longitude = gps_data["Longitude"]
                    gps_data_object.EoW = gps_data["East/West"]
                    gps_data_object.batLevel = gps_data["Internal battery Level (Volts)"]
                    gps_data_object.SignalStrength = gps_data["Signal Strength"]
                    gps_data_object.Status = "ON"
                    gps_data_object.time_stamp = str(dateTimeIND)
                    # write to json
                    write_result_file(read_package.to_dict())

                else:
                    Status: str = "ON"
                    TimeStamp: str = dateTimeIND


            elif raw_data[0] == "H":
                if not gps_data["Latitude"] == "":
                    print("History ---- Stored")
                    gps_data_object.imei = gps_data["IMEI"]
                    gps_data_object.latitude = gps_data["Latitude"]
                    gps_data_object.NoS = gps_data["North/South"]
                    gps_data_object.longitude = gps_data["Longitude"]
                    gps_data_object.EoW = gps_data["East/West"]
                    gps_data_object.batLevel = gps_data["Internal battery Level (Volts)"]
                    gps_data_object.SignalStrength = gps_data["Signal Strength"]
                    gps_data_object.Status = "ON"
                    gps_data_object.time_stamp = str(dateTimeIND)

                    # Send to MQTT Server
                    # mqtt_publish(message=read_package_file)

                    # write to json
                    write_result_file(read_package.to_dict())

                else:
                    print("GPSData", gps_data)

            return gps_data

        # --------- OBD Data ---------
        elif raw_data[1] == "ATLOBD":
            obd_data = convert_OBD_data(raw_data)
            return obd_data
        # -----------------------------------

    except Exception as ex:
        print(ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)

