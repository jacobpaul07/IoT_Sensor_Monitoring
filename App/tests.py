
import time
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from App.Utilities import read_result_file


def sentLiveData(data):
    text_data = json.dumps(data, indent=4)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("notificationGroup", {
        "type": "chat_message",
        "message": text_data
    })


def read_json_to_websocket():

    try:
        while True:
            result_file_contents = read_result_file()
            sentLiveData(result_file_contents)
            # mqtt_publish(message=result_file_contents)
            print(result_file_contents)
            time.sleep(3)
    except Exception as exception:
        print("Device is not Connected Error:", exception)
