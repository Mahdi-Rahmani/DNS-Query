from socket import *
serverPort = 53
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('the server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(message)
    ackResponse = 'Your DNS query has been received'
    serverSocket.sendto(ackResponse.encode(), clientAddress)