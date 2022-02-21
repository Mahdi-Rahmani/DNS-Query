import pickle
from socket import *
from DNSMessage import DNSMessage
from ServerResponseHandler import ServerResponseHandler
import binascii

# we can find the list of types from searching(specially wikipedia)
types = ["ERROR", "A", "NS", "MD", "MF", "CNAME", "SOA", "MB", "MG", "MR", "NULL", "WKS", "PTR", "HINFO",
         "MINFO", "MX", "TXT", 'RP', 'AFSDB', 'X25', 'ISDN', 'RT', 'NSAP', 'NSAP-PTR', 'SIG', 'KEY', 'PX',
         'GPOS', 'AAAA', 'LOC', 'NXT', 'EID', 'NB', 'NBSTAT', 'ATMA']

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


def query(message, serverAddress, is_iterative):
    response = send_message(53, serverAddress, message)
    if is_iterative:
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
    return response


""" This function cache the resolved DNS queries for us
 first it opens a file and then check if the message exists and its value is 0,1,2
 then add 1 to that. if the value is bigger than 2 we should copy the response of 
 server instead of that value. then if want that query again we can read it from our cache."""


def cache_data(message, serverAddress, is_iterative, cacheAddress):
    my_cache = {}
    try:
        with open(cacheAddress, 'rb') as my_db:
            my_cache = pickle.load(my_db)
    except:
        pass
    # here first we check the value of the related key is an integer or not
    value = my_cache.get(message, 0)
    if isinstance(value, int):
        # if it has 0,1,2 value we should add 1 to it
        my_cache[message] = value + 1
        # now we should get the response from server
        response = query(message, serverAddress, is_iterative)
        # if the value is 3 we should save the response(that for example has ip_address)
        if (my_cache[message] > 2):
            my_cache[message] = response
        print('The response from server:')
    # if the value is not integer we should response from the cache
    else:
        response = my_cache[message]
        print('The response from cache:')

    with open(cacheAddress, 'wb') as my_db:
        pickle.dump(my_cache, my_db)

    return response


# first we get nameAddress and DNSType from user
nameAddress, DNSType = user_interface()

# now we should create a Message
message = message_creator(DNSType, nameAddress)

# now we should get the response of this message
# for that we have two state :1) the server must response 2) we read from cache
response = cache_data(message, '1.1.1.1', False, '.\cache.dict')

# now we pass the response to the serverResponseHandler to return IP
My_ServerResponseHandler = ServerResponseHandler()
IP_Address = My_ServerResponseHandler.return_IP(response)
print('The IP-Address is:\n', IP_Address)
