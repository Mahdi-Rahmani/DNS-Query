import binascii


class ServerResponseHandler:
    """ we can call this function to return IP address if it exist in RD_DATA"""

    def return_IP(self, message):
        response = self.parse_answer(message)
        if len(response['Answer']) > 0:
            return response['Answer'][0]['RDDATA_DECODED']
        else:
            return 'IP Address Not found'

    """ This function parse the answer of server and hold the information
    in a dictionary. """

    def parse_answer(self, message):
        # We want to parse answer in a dictionary
        # first we decode header section
        # The header has a form like this:
        """        0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
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

        response = {'Response RAW': message,
                    'ID': (int(message[0:4], 16)),
                    'QUERY_FIELDS': '{:016b}'.format(int(message[4:8], 16)),
                    'QDCOUNT': (int(message[8:12], 16)),
                    'ANCOUNT': (int(message[12:16], 16)),
                    'NSCOUNT': (int(message[16:20], 16)),
                    'ARCOUNT': (int(message[20:24], 16))}

        # second we Decode question section
        # The question part has a form like this:
        """         0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
                    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                    |                    QNAME                      /
                    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                    |                    QTYPE                      |
                    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                    |                    QCLASS                     |
                    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+"""

        # we use a variable pointer for reading the size of each section
        response['QNAME'] = self.parse_parts(message, 24, [])
        pointer = 26 + (len("".join(response['QNAME']))) + (len(response['QNAME']) * 2)
        # response['QNAME_DECODED'] = '.'.join([binascii.unhexlify(x).decode() for x in q_name_parts])
        response['QTYPE'] = self.get_type(int(message[pointer: (pointer + 4)], 16))
        pointer += 4
        response['QCLASS'] = int(message[pointer: (pointer + 4)], 16)
        pointer += 4

        # third we Decode answer section but also we decode Authority and Additional too
        # The Answer part & Authority part Additional part have a form like this
        """        0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
                   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                   /                    NAME                       /
                   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                   |                    TYPE                       |
                   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                   |                    CLASS                      |
                   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                   |                    TTL                        |
                   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                   |                    RDLENGTH                   |
                   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                   /                    RDATA                      /
                   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ """
        # We know that also with the value of ANCOUNT and NSCOUNT and ARCOUNT the number of this section is determined
        # We create a list that has the number of each part
        Ans_Auth_Add_NUMBER = [response['ANCOUNT'], response['NSCOUNT'], response['ARCOUNT']]
        Ans_Auth_Add_NAME = ['Answer', 'Authority', 'Additional']
        # because of having same job for Answer part & Authority part Additional part so we have a loop with range[0:3]
        for index in range(3):
            response[Ans_Auth_Add_NAME[index]] = []
            if Ans_Auth_Add_NUMBER[index] > 0:
                for i in range(Ans_Auth_Add_NUMBER[index]):
                    # for example if we have 3 Answer we iterate 3 times
                    # then we need to save the part of each Answer section in a variable
                    # so I use section variable to do this
                    section = {}
                    if pointer < len(message):

                        section['NAME'] = message[pointer: (pointer + 4)]
                        pointer += 4
                        section['TYPE'] = self.get_type(int(message[pointer: (pointer + 4)], 16))
                        pointer += 4
                        section['CLASS'] = message[pointer: (pointer + 4)]
                        pointer += 4
                        section['TTL'] = int(message[pointer: (pointer + 8)], 16)
                        pointer += 8
                        section['RDLENGTH'] = int(message[pointer: (pointer + 4)], 16)
                        pointer += 4
                        section['RDDATA'] = message[pointer: (pointer + (section['RDLENGTH'] * 2))]
                        pointer += (section['RDLENGTH'] * 2)

                        # print(int(section['TYPE'], 16) , section['TYPE'] ,self.get_type('A'))
                        if section['TYPE'] == 'A':
                            octets = [section['RDDATA'][i:i + 2] for i in range(0, len(section['RDDATA']), 2)]
                            decoded_RDDATA = '.'.join(str(int(x, 16)) for x in octets)
                        else:
                            decoded_RDDATA = '.'.join(binascii.unhexlify(p).decode('iso8859-1') for p in
                                                      self.parse_parts(section['RDDATA'], 0, []))
                        # print(section)
                        section['RDDATA_DECODED'] = decoded_RDDATA
                    # now we should add this section to the related key in response
                    response[Ans_Auth_Add_NAME[index]].append(section)
        return response

    """ in this function we parse the QNAME of the question part
        and we know in QNAME first of each part we have the length of that part
        and after we have main part.
        in this version of function we find name address parts recursively"""

    def parse_parts(self, message, start, parts):
        part_start = start + 2
        part_len = message[start:part_start]

        if len(part_len) == 0:
            return parts

        part_end = part_start + (int(part_len, 16) * 2)
        parts.append(message[part_start:part_end])

        if message[part_end:part_end + 2] == "00" or part_end > len(message):
            return parts
        else:
            return self.parse_parts(message, part_end, parts)

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

    """ This function like the above function but we find name address parts with a loop"""

    def parse_part_version2(message, start, parts):
        part_end = start
        while ~(message[part_end:part_end + 2] == "00" or part_end > len(message)):
            part_start = start + 2
            part_len = message[start:part_start]

            if len(part_len) == 0:
                return parts

            part_end = part_start + (int(part_len, 16) * 2)
            parts.append(message[part_start:part_end])
            start = part_end
        return parts

    def get_name_address(self, message):
        QUESTION_SECTION_STARTS = 24
        address_name_parts = ServerResponseHandler.parse_parts(message, QUESTION_SECTION_STARTS, [])
        address_name = ".".join(map(lambda p: binascii.unhexlify(p).decode(), address_name_parts))
        return address_name
