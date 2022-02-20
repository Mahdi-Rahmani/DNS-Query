import binascii

""" In this class we create a new DNS Message with a given type and
 the address name that the user give us """


class DNSMessage:
    """ in we should ask from user to enter a name address and a type
    after that we should build a message to get the record with that type"""

    def __init__(self, type, address):
        # the message has a header and a question part
        # the header has a form like this:
        """ 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                       ID                      |
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    QDCOUNT                    |
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    ANCOUNT                    |
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    NSCOUNT                    |
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    ARCOUNT                    |
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+"""
        # We hold the header in a List
        ID = 43690
        QR = '0'
        OPCODE = '0000'
        AA = '0'
        TC = '0'
        RD = '1'
        RA = '0'
        Z = '000'
        RCODE = '0000'
        QDCOUNT = 1  # Number of questions           4bit
        ANCOUNT = 0  # Number of answers             4bit
        NSCOUNT = 0  # Number of authority records   4bit
        ARCOUNT = 0  # Number of additional records  4bit

        self.header = [
            '{:04x}'.format(ID),
            '{:04x}'.format(int(''.join((QR, OPCODE, AA, TC, RD, RA, Z, RCODE)), 2)),
            '{:04x}'.format(QDCOUNT),
            '{:04x}'.format(ANCOUNT),
            '{:04x}'.format(NSCOUNT),
            '{:04x}'.format(ARCOUNT)
        ]

        # the question part has a form like this:
        """ 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    QNAME                      /
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    QTYPE                      |
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    QCLASS                     |
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+"""
        # We hold the question part in a List
        # QNAME = address
        # QTYPE = type
        QCLASS = 1

        self.question = [
            address,
            '{:04x}'.format(self.get_type(type)),
            '{:04x}'.format(QCLASS),
        ]

    """ in the constructor of this class we create a list for holding header 
    and a list for holding question part. now we need to create the message from 
     the information that we hold later with this function"""

    def message_builder(self):
        # We hold the final message in message variable
        # add the header in message
        message = ''.join(self.header)
        # add the address in message after some processes
        address_parts = self.question[0].split(".")
        for part in address_parts:
            address_len = "{:02x}".format(len(part))
            address_part = binascii.hexlify(part.encode())
            message += address_len
            message += address_part.decode()
        # Terminating bits for QNAME
        message += '00'

        # add the other parts of question part
        message += self.question[1]
        message += self.question[2]
        message = message.replace(" ", "").replace("\n", "")
        return message

    """ We should save a list of types. each type has a specific number. 
    if user enter the name of type in string format we return that 
    else if the user enter a number we should find type peer to that number in the list"""

    def get_type(self, DNSType):
        # we can find the list of types from searching(specially wikipedia)
        types = ["ERROR", "A", "NS", "MD", "MF", "CNAME", "SOA", "MB", "MG", "MR", "NULL", "WKS", "PTR", "HINFO",
                 "MINFO", "MX", "TXT", 'RP', 'AFSDB', 'X25', 'ISDN', 'RT', 'NSAP', 'NSAP-PTR', 'SIG', 'KEY', 'PX',
                 'GPOS', 'AAAA', 'LOC', 'NXT', 'EID', 'NB', 'NBSTAT', 'ATMA']
        # if the entry type was a string we should return it
        # else if the user enter the number we should return the peer type in list
        if isinstance(DNSType, str):
            return types.index(DNSType)
        else:
            return types[DNSType]
