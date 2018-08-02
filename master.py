from websocket import create_connection
import time
import json


def send(data):
    global ws
    ws.send(json.dumps(data))
    return


def receive():
    global ws
    data = ws.recv()
    return json.loads(data)


ws = create_connection("ws://localhost:8000")


result = receive()
send({'role': 'master'})
result = receive()
