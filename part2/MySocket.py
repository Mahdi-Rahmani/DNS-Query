from socket import *
import binascii

""" This function is used after creating a DNS query.
first we should create a socket. after that we send the query
with this socket. then we recieve the server response and return it."""


def send_message(serverPort, serverAddress, message):
    # now we should create a socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(binascii.unhexlify(message), (serverAddress, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    response = binascii.hexlify(response).decode("utf-8")
    clientSocket.close()
    return response


# if we want to use our server we should change the serverName in to 127.0.0.1 and comment the line 28
# serverAddress = '127.0.0.1'
serverAddress = '1.1.1.1'
serverPort = 53
message = '463f010000010000000000000377777706676f6f676c6503636f6d0000010001'

response = send_message(serverPort,serverAddress,message)
print('The response is:\n', response)

