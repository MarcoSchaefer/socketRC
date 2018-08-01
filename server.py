import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
import logging

sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect')
def connect(sid, environ):
    print("CONNECTED: ", sid)

@sio.on('connect', namespace='/control')
def connect(sid, environ):
    #sio.emit('reply','some data here')
    #sio.emit('reply','some data here', room=sid)
    print("CONNECTED: ", sid)
    return True

@sio.on('root', namespace='/')
def Ping(sid, data):
    print("ROOT: ", data)
    return sio.emit('root',{'data':'RESPONSE FROM SERVER'}, room=sid)
    #sio.emit('root',{'data':'RESPONSE FROM SERVER'}, room=sid)
    #sio.emit('root',{'data':'RESPONSE FROM SERVER'}, room=sid)

@sio.on('ping', namespace='/control')
def Ping(sid, data):
    print("CONTROL: ", data)
    sio.emit('reply','LUL')
    sio.emit('reply','AAA', room=sid)
    sio.emit('ping','some data here', room=sid)
    sio.emit('ping', 'pong', namespace='/control')

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
