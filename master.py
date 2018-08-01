from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace

#import logging
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)


def on_some_response(*data):
    if data:
        print('RESPONSE: ', data)

socketIO = SocketIO('localhost', 8000, LoggingNamespace)
#data_namespace = socketIO.define(DataNamespace, '/data')
control_namespace = socketIO.define(LoggingNamespace, '/control')
#control_namespace = socketIO.define(LoggingNamespace, '/control')

#socketIO.on('ping',on_some_response)

#control_namespace.on('ping',on_some_response)

#socketIO.on('reply', on_some_response)
#socketIO.on('ping', on_some_response)
socketIO.on('root', on_some_response)

def Ping():
    socketIO.emit('root',{'data':'something'}, on_some_response)
    socketIO.wait_for_callbacks(seconds=1)
