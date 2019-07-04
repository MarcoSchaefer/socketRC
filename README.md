# socketRC

## Introduction

SocketRC allows you to send terminal commands to any machine, despite being in a Windows or Linux environment. It connects the slaves and the master to the server machine through websockets. It allows the master to send the same command to one or multiple slaves, and then receive the response from each one. It's useful if you need to configure multiple machines constantly, and they are under a NAT, so you can't ssh then directly if your router doesn't allows port forwarding.

### Get Started

First setup your server by building the container and running, this container will run server, need to connect by

```sh
docker build --tag marcoschaefer/socketrc-server .
docker run -d -p 8000:8000 marcoschaefer/socketrc-server
```

now in machine you want to remote control run ...
```sh
python slave.py {socketrc-server-ip} 8000
```

now in machine you want to control run
```sh
python master.py {socketrc-server-ip} 8000
```