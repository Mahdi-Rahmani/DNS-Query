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