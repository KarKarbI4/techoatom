from socket import socket
server = socket()
address = '127.0.0.1', 54670
server.bind(address)
server.listen(1)
client.client_address = server.accept