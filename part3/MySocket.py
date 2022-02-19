import csv
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


def message_creator(DNSType, nameAddress, id):
    # now we should create an object from DNSMessage class
    myDNSQuery = DNSMessage(DNSType, nameAddress, id)
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


""" This function create an object from ServerResponseHandler.
if the record type is A Then we can find IP address with return_IP function of that object """


def IPAddressFinder(response):
    My_ServerResponseHandler = ServerResponseHandler()
    return My_ServerResponseHandler.return_IP(response)


""" This function creat an object from ServerResponsHandler.
Then it calls the parse_answer method of that object 
and return the dictionary of response information """


def response_parser(response):
    My_ServerResponseHandler = ServerResponseHandler()
    return My_ServerResponseHandler.parse_answer(response)


""" The input file that we read from has a form like this:
      DNS_type   Name-Address   ID   server-Address
    The out put file that we save the response answer inside it has a form like this:
      Type  class  TTL  RD_length  RD_DATA """


def requests_from_csv(in_file_add, out_file_add):
    response_list = [("Type", "Class", "TTL", "RD_length", "RD_DATA")]
    index = 0
    with open(in_file_add, 'r') as input:
        for current_row in csv.reader(input):
            if index == 0:
                index += 1
                continue
            message = message_creator(current_row[0], current_row[1], int(current_row[2]))
            response = send_message(53, current_row[3], message)
            parsed_response = response_parser(response)
            temp = [(parsed_response['Answer'][0]["TYPE"], parsed_response['Answer'][0]["CLASS"],
                     parsed_response['Answer'][0]["TTL"],
                     parsed_response['Answer'][0]["RDLENGTH"], parsed_response['Answer'][0]["RDDATA_DECODED"])]
            response_list.append(temp)

    with open(out_file_add, 'w') as output:
        spamWriter = csv.writer(output)
        for part in response_list:
            spamWriter.writerow(part)


# first we get nameAddress and DNSType from user
nameAddress, DNSType = user_interface()

# now we should create a Message
message = message_creator(DNSType, nameAddress, 43690)

# now we should create a socket and send message
response = send_message(53, '1.1.1.1', message)

# now we can find the IP address if exist
ip_address = IPAddressFinder(response)
print('The IP-Address is:\n', ip_address)

# now we send multiple query and then save info in csv file
requests_from_csv('./myInputs.csv', './myOutputs.csv')
