from websocket import create_connection
import time
import json
import threading
import requests

def receive():
    while:
        global ws
        data = ws.recv()
        result = json.loads(data)
        if 'result' in result:
            print(result['result'])
        else:
            print(result)

def send(data):
    global ws
    ws.send(json.dumps(data))
    return

ws = create_connection("ws://192.168.0.2:8000")
send({'role': 'master'})

receiverThread = threading.Thread(target=receive)
receiverThread.start()
