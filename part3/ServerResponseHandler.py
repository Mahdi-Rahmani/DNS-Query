import binascii


class ServerResponseHandler:
    def return_IP(self, message):
        response = self.parse_answer(message)
        if len(response['Answer']) > 0:
            return response['Answer'][0]['RDDATA_DECODED']
        else:
            return 'IP Address Not found'

    def parse_answer(self, message):

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
                   /                    RDDATA                     /
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