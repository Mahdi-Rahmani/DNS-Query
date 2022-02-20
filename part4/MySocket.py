from socket import *
from DNSMessage import DNSMessage
from ServerResponseHandler import ServerResponseHandler
import binascii

# we can find the list of types from searching(specially wikipedia)
types = ["ERROR", "A", "NS", "MD", "MF", "CNAME", "SOA", "MB", "MG", "MR", "NULL", "WKS", "PTR", "HINFO",
         "MINFO", "MX", "TXT", 'RP', 'AFSDB', 'X25', 'ISDN', 'RT', 'NSAP', 'NSAP-PTR', 'SIG', 'KEY', 'PX',
         'GPOS', 'AAAA','LOC', 'NXT', 'EID', 'NB', 'NBSTAT','ATMA']

""" This function get name address and  DNSType from user """


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


""" This function create a DNS query for us.
for this job first the function create a new object 
from DNSMessage class and then call the message_builder function
from that class."""


def message_creator(DNSType, nameAddress):
    # now we should create an object from DNSMessage class
    myDNSQuery = DNSMessage(DNSType, nameAddress)
    return myDNSQuery.message_builder()


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


""" if we want to request in iterative form we can do that with this function"""


def iterative_query(message, DNSType, nameAddress):
    # first we should parse the response of server
    My_ServerResponseHandler = ServerResponseHandler()
    parsed_response = My_ServerResponseHandler.parse_answer(message)
    while parsed_response['ARCOUNT'] != 0 and parsed_response['ANCOUNT'] == 0:
        for part in parsed_response['Additional']:
            if part['TYPE'] == 'A':
                newIPAddress = part['RDDATA_DECODED']
                response = send_message(53, newIPAddress, message_creator(DNSType, nameAddress))
                parsed_response = My_ServerResponseHandler.parse_answer(response)
                break
    return My_ServerResponseHandler.return_IP(response)


# first we get nameAddress and DNSType from user
nameAddress, DNSType = user_interface()

# now we should create a Message
message = message_creator(DNSType, nameAddress)

# now we should create a socket and send
response = send_message(53, '198.41.0.4', message)

# now we can find IP in iterative form
ip_address = iterative_query(response, DNSType, nameAddress)

print('The IP-Address is:\n', ip_address)