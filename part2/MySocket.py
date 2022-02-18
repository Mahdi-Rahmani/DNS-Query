from socket import *
import binascii

def send_message(serverPort, serverAddress, message):
    # now we should create a socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(binascii.unhexlify(message), (serverAddress, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    response = binascii.hexlify(response).decode("utf-8")
    clientSocket.close()
    return response

serverAddress = '127.0.0.1'
serverPort = 52
message = '463f010000010000000000000377777706676f6f676c6503636f6d0000010001'

response = send_message(serverPort,serverAddress,message)
print('The response is:\n', response)



