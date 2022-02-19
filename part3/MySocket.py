import csv
from socket import *
from ServerResponseHandler import ServerResponseHandler
from DNSMessage import DNSMessage
import binascii

# we can find the list of types from searching(specially wikipedia)
types = ["ERROR", "A", "NS", "MD", "MF", "CNAME", "SOA", "MB", "MG", "MR", "NULL", "WKS", "PTR", "HINFO",
         "MINFO", "MX", "TXT", 'RP', 'AFSDB', 'X25', 'ISDN', 'RT', 'NSAP', 'NSAP-PTR', 'SIG', 'KEY', 'PX',
         'GPOS', 'AAAA','LOC', 'NXT', 'EID', 'NB', 'NBSTAT','ATMA']

def user_interface():
    # we should get the address and type from user
    name_address = input('Please enter the name address:\n')
    while True:
        DNSType = input('please enter the type of query:\n')
        if DNSType.isdigit():
            DNSType = int(DNSType)
            if DNSType < len(types):
                break
        if DNSType in types:
            break
    return name_address, DNSType

def message_creator(DNSType, nameAddress, id):
    # now we should create an object from DNSMessage class
    myDNSQuery = DNSMessage(DNSType, nameAddress, id)
    return myDNSQuery.message_builder()


def send_message(serverPort, serverAddress, message):
    # now we should create a socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(binascii.unhexlify(message), (serverAddress, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    response = binascii.hexlify(response).decode("utf-8")
    clientSocket.close()
    return response

def IPAddressFinder(response):
    My_ServerResponseHandler = ServerResponseHandler()
    return My_ServerResponseHandler.return_IP(response)


def response_parser(response):
    My_ServerResponseHandler = ServerResponseHandler()
    return My_ServerResponseHandler.parse_answer(response)