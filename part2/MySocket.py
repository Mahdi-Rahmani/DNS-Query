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


