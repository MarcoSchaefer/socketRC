from websocket import create_connection
import time
import json
import threading
import requests
import sys

def receive():
    while True:
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

ip = sys.argv[1]
port = sys.argv[2]
ws = create_connection("ws://"+ip+":"+port)
send({'role': 'master'})

receiverThread = threading.Thread(target=receive)
receiverThread.start()


while True:
  command = input()
  payload = {'command': command}
  send(payload)