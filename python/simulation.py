import random
import math

class Hash_Function:
    func = {}
    def value(self, key):                 # not to be confused with 'key' in rest of the code
        if key not in self.func:
            self.func[key] = random.uniform(0,1)
        return self.func[key]

class Query:
    def __init__(self, key, attr, T_q, m_q, n_q, p_q, gamma_q):
        self.key = key      
        self.attr = attr                  # key, attr are subsets of [0,1,2,3,4, ... , #pac_info - 1] stored as a 'frozenset'
        self.T_q = T_q
        self.m_q = m_q
        self.p_q = p_q
        self.n_q = n_q
        self.gamma_q = gamma_q

def which_coupon(attr, hashval):
    global attr_to_querylist
    
    for query in attr_to_querylist[attr]:
        if hashval >= query.m_q*query.p_q:
            hashval -= query.m_q*query.p_q
        else:
            coupon = math.floor(hashval/query.p_q)  # indexed from 0
            return (query, coupon)
    return (None, None)

class Packet:
    def __init__(self, pac_info):
        self.pac_info = pac_info      # has srcIP, dstIP, srcPort, dstPort, ... in some fixed order

    def get_timestamp(self):
        return self.pac_info[5];           # modify accordingly

    def extract(self, indset):        # get values for some index subset from pac_info
        val = set()
        for ind in indset:
            val.add(self.pac_info[ind])
        return frozenset(val)

    def collect_coupon_from_attr(self, attr):
        global attr_to_hashfunc

        attrval = self.extract(attr)
        hashval = attr_to_hashfunc[attr].value(attrval)
        query, coupon = which_coupon(attr, hashval)
        # print(hashval)
        # if query != None:
        #     print(query.key)
        # else:
        #     print(query)
        # print(coupon)
        # print()
        return (query, coupon)

    def collect_coupon(self):
        global attributes

        collected = []
        for attr in attributes:
            query, coupon = self.collect_coupon_from_attr(attr)
            if query != None:
                collected.append((query, coupon))

        # print(len(collected))
        if len(collected) == 1:
            return collected[0]
        elif len(collected) == 2:
            return collected[random.getrandbits(1)]
        else:
            return (None, None)


class CCTable:
    # Not doing checksum stuff now. Assuming not too many (query, key) pairs that will be active
    # Also ignoring onehot(c) thing

    table = {}                    # map each (q, k) to a list of length m_q               
    table_timestamp = {}          # map each (q, k) to a timestamp
    table_count = {}
    W = 0

    def __init__(self, W):        # timestamp expire time
        self.W = W

    def add_packet(self, packet):
        query, coupon = packet.collect_coupon()
        if query == None:
            return
        keyval = packet.extract(query.key)

        qk_pair = (query, keyval)
        timestamp = packet.get_timestamp()

        if qk_pair not in self.table.keys() or self.table_timestamp[qk_pair] < timestamp - self.W:
            self.table_timestamp[qk_pair] = timestamp
            self.table[qk_pair] = [0]*query.m_q
            self.table_count[qk_pair] = 0

        if self.table[qk_pair][coupon] != 1:
            self.table[qk_pair][coupon] = 1
            self.table_count[qk_pair] += 1

        if self.table_count[qk_pair] == query.m_q:
            print("Output alert for query, keyval here ")
            print(query.key) 

        # print(self.table[qk_pair])  


# Main

def pre_process():
    global queries, packets, attributes, attr_to_querylist, attr_to_hashfunc

    attributes = set()
    for query in queries:
        attributes.add(query.attr)

    for attr in attributes:
        attr_to_querylist[attr] = []
        attr_to_hashfunc[attr] = Hash_Function();

    for query in queries:
        attr_to_querylist[query.attr].append(query)



# queries, packets as input
queries = [Query(frozenset([1]), frozenset([1,3]), 50, 2, 2, 1/2, 2),  
            Query(frozenset([1, 2]), frozenset([1,3]), 50, 2, 2, 1/2, 2),
            Query(frozenset([1,3,5]), frozenset([1,3]), 50, 2, 16, 0, 2),
            Query(frozenset([1,3,2]), frozenset([1,3]), 50, 2, 16, 0, 2),
            Query(frozenset([2,1,0]), frozenset([2,4,4]), 2, 16, 16, 1/1000, 2),
            Query(frozenset([3, 2]), frozenset([2,3,0]), 2, 16, 16, 1/1000, 2),
            Query(frozenset([4]), frozenset([1]), 50, 16, 16, 1/1000, 2)]
packets = [Packet([0,1,2,3,4,5]),
            Packet([1, 1, 3, 4, 5, 6]),
            Packet([2, 1, 4, 5, 0, 1]), 
            Packet([3, 1, 5, 0, 1, 2])]

attributes = {}
attr_to_querylist = {}
attr_to_hashfunc = {}

pre_process()

cctable = CCTable(5);

for pack in packets:
    cctable.add_packet(pack)


# print(queries)
# print(packets)
# for attr in attributes:
#     print(attr_to_querylist[attr])
# print(attr_to_querylist)
# print(attr_to_hashfunc)

# print(attributes)
# print(packets[3].extract(queries[2].key))
# print(packets[3].extract(queries[2].attr))
# print()

# query, coupon = which_coupon(frozenset([1,3]), 1/4+3/16)
# print(query.key);
# print(coupon)
# print()
# query, coupon = which_coupon(frozenset([1,3]), 3/4-0.001)
# print(query.key);
# print(coupon)
# print()
# query, coupon = which_coupon(frozenset([1,3]), 3/4)
# print(query);
# print(coupon)
# print()
# query, coupon = which_coupon(frozenset([1]), 1/8)
# print(query.key);
# print(coupon)
# print()

# query, coupon = packets[1].collect_coupon()
# if query != None:
#     print(query.key)
# else:
#     print(query)
# print(coupon)
# print()
