import binascii


class DNSMessage:
    def __init__(self, type, address , id):

        ID = id
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

        QCLASS = 1

        self.question = [
            address,
            '{:04x}'.format(self.get_type(type)),
            '{:04x}'.format(QCLASS),
        ]
