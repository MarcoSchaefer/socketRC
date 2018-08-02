#!/usr/bin/python

import tornado.web
import tornado.websocket
import tornado.ioloop
import json

master_socket = False
slave_sockets = []


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def send(self,data):
        self.write_message(json.dumps(data))

    def open(self):
        global master_socket
        print("New client connected")
        self.send({'status':'CONNECTED'})

    def on_message(self, data):
        global master_socket
        global slave_sockets
        print("RECEIVED: " + data)
        message = json.loads(data)
        if 'role' in message:
            if message['role'] == "master":
                print("NEW MASTER ASSIGNED")
                master_socket = self
            elif message['role'] == "slave":
                print("NEW SLAVE ASSIGNED")
                try:
                    master_socket.send(message)
                except:
                    print("NO MASTER FOUND")
                slave_sockets.append(self)
        elif 'command' in message:
            if master_socket != self:
                self.send({'error':'INSUFFICIENT PERMISSIONS'})
            for slave in slave_sockets:
                slave.send(message)
        self.send(message)

    def on_close(self):
        print("Client disconnected")


application = tornado.web.Application([
    (r"/", WebSocketHandler),
])

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
