# socketRC

## Introduction

SocketRC allows you to send terminal commands to any machine, despite being in a Windows or Linux environment. It connects the slaves and the master to the server machine through websockets. It allows the master to send the same command to one or multiple slaves, and then receive the response from each one. It's useful if you need to configure multiple machines constantly, and they are under a NAT, so you can't ssh then directly if your router doens't allows port forwarding.
