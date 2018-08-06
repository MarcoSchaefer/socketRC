#!/usr/bin/python

import tornado.web
import tornado.websocket
import tornado.ioloop
import json
import requests


import logging
logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


master_sockets = []
slave_sockets = []


def MasterHandler(socket, message):
    global master_sockets
    global slave_sockets
    if 'command' in message:
        if socket not in master_sockets:
            socket.send({'error':'INSUFFICIENT PERMISSIONS'})
            return
        else:
            for slave in slave_sockets:
                slave.send(message)

def SlaveHandler(socket, message):
    global master_sockets
    global slave_sockets
    if 'result' in message:
        for master in master_sockets:
            master.send(message)
        return



class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def send(self,data):
        self.write_message(json.dumps(data))

    def open(self):
        print("New client connected")
        self.send({'status':'CONNECTED'})

    def on_message(self, data):
        global master_sockets
        global slave_sockets
        print("RECEIVED: " + data)
        message = json.loads(data)
        if 'role' in message:
            if message['role'] == "master":
                print("NEW MASTER ASSIGNED")
                if self not in master_sockets:
                    master_sockets.append(self)
                if self in slave_sockets:
                    slave_sockets.remove(self)
            elif message['role'] == "slave":
                if self not in slave_sockets:
                    slave_sockets.append(self)
                if self in master_sockets:
                    master_sockets.remove(self)
                print("NEW SLAVE ASSIGNED")
                try:
                    for master in master_sockets:
                        master.send({'slave': self.request.remote_ip})
                except:
                    print("NO MASTER FOUND")
        if self in master_sockets:
            MasterHandler(self,message)
        elif self in slave_sockets:
            SlaveHandler(self,message)

    def on_close(self):
        try:
            slave_sockets.remove(self)
        except:
            pass
        try:
            master_sockets.remove(self)
        except:
            pass
        print("Client disconnected")


application = tornado.web.Application([
    (r"/", WebSocketHandler),
])

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
