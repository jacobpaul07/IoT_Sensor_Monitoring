import datetime
from socket import socket, timeout
import threading
from App.Gps_Socket_Listner.gps_monitor import convert_raw_to_information
import pytz

global_lock = threading.Lock()
stopThread: bool = False


class SocketThread(threading.Thread):
    def __init__(self, clientAddress: str, clientsocket: socket, deviceCount: int):
        threading.Thread.__init__(self)

        self.csocket = clientsocket
        self.clientAddress = clientAddress
        self.timeout = 300
        self.count = 0
        self.deviceCount = deviceCount
        self.gpslist_lat = []
        self.gpslist_lon = []
        self.maxRetryCount = 4
        self.currentRetryCount = 0
        setTimeout: int = self.timeout / self.maxRetryCount
        clientsocket.settimeout(setTimeout)
        print("New connection added: ", clientAddress)

    def run(self):
        print("Started")
        self.start = True
        # cli = boto3.client('s3')
        while self.start:
            try:
                data = self.csocket.recv(1024)
                print(data)
                self.currentRetryCount = 0

                if not data:
                    return

                with global_lock:
                    IST = pytz.timezone('Asia/Kolkata')
                    dateTimeIND = datetime.datetime.now(IST).strftime("%Y-%m-%dT%H:%M:%S.%f")
                    fData = convert_raw_to_information(data)

                    if fData["Live/Memory"] == "L":
                        gen_data = {
                            "TimeStamp: ": dateTimeIND,
                            "Connection from : ": self.clientAddress,
                            "device number": self.deviceCount,
                            "thread identity": str(threading.get_ident()),
                            "Live Data ": data
                        }
                        print(gen_data)
                    else:
                        print(" 'H' data Received: ")

                    IMEI = fData["IMEI"]
                    atIMEI = "@" + IMEI
                    messageType = "00"
                    sequenceNumber = fData["Sequence No"]
                    checkSum = "*CS"
                    packet = atIMEI, messageType, sequenceNumber, checkSum
                    seperator = ","
                    joinedPacket = seperator.join(packet)
                    bytesPacket = bytes(joinedPacket, 'utf-8')
                    print("Return Packet:", bytesPacket)
                    self.csocket.send(bytesPacket)
                    print("Client at", self.clientAddress, "Packet Completely Received...")

            except timeout as exception:
                print("Timeout raised and caught.", exception)
                self.currentRetryCount = self.currentRetryCount + 1

                if self.currentRetryCount > self.maxRetryCount:
                    status: str = "OFF"
                    print("Device", status)
                    self.csocket.close()
                    self.start = False
                    self.currentRetryCount = 0
                else:
                    status: str = "IDLE"
                    print("Device", status)

            except Exception as exception:
                print("Error occured with exception:", exception)

            print("--------------------------------------------------------------------------------------------")
