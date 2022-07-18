import os
import socket
import sys
from App.Gps_Socket_Listner.socketThreading import SocketThread

LOCALHOST = str(os.environ['SOCKET_HOST'])
PORT = int(os.environ['SOCKET_PORT'])


def socket_listener():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LOCALHOST, PORT))
        print("Socket Server started")
        print("Waiting for Device..")
        deviceCount: int = 0
        print("Service is hosted on host:", LOCALHOST, "and port:", PORT)

        while True:
            deviceCount = deviceCount + 1
            server.listen()
            clientsock, clientAddress = server.accept()
            new_thread = SocketThread(clientAddress, clientsock, deviceCount)
            new_thread.start()

    except Exception as ex:
        print("Socket Listener Error: ", ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)

