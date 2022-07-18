import datetime
import pymongo
from App.Json_Class.index import read_setting
from config.databaseconfig import Databaseconfig
import config.databaseconfig as dbc


class Document:

    def __init__(self):
        data = read_setting()
        DataBase: str = data.edgedevice.Service.MongoDB.DataBase
        connection = Databaseconfig()
        connection.connect()
        self.db = dbc.client[DataBase]

    def DB_Write(self, data, col):
        parameter = data
        collection = self.db[col]
        collection.insert_one(parameter)

    def DB_Read(self, col):
        collection = self.db[col]
        v = collection.find()
        list = []
        for i in v:
            value = i
            list.append(value)
        print(list)
        return list

    def Read_Document(self, col, DeviceID, filterField):
        collection = self.db[col]
        x = list(collection.find().sort(filterField, -1).limit(1))
        return x[0]

    def Write_Document(self, col, DeviceID, data):
        collection = self.db[col]
        myquery = {'DeviceID': DeviceID}
        x = collection.replace_one(myquery, data)
        updatedCount = x.matched_count
        print("documents updated in MongoDB.")
        # print(updatedCount, "documents updated.")
        return updatedCount

    def SpecificDate_Document(self, Timestamp: str, filterField: str, col, machineID):
        collection = self.db[col]
        date_time = datetime.datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S%z")
        from_date = datetime.datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute,
                                       0, 000000)
        to_date = datetime.datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute,
                                     0, 000000) + datetime.timedelta(minutes=10)
        criteria = {"$and": [{filterField: {"$gte": from_date, "$lte": to_date}}]}
        # criteria = {"$and": [{filterField: {"$gte": from_date, "$lte": to_date}}, {"machineID": machineID}]}
        objects_found = list(collection.find(criteria, {"_id": 0}).sort(filterField, pymongo.ASCENDING))
        series = []
        if len(objects_found) > 0:
            series.append(objects_found[0])
        return series
