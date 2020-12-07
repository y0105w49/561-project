import random
import math
from HLL import HyperLogLog

EST = 6

class Hash_Function:
    func = {}
    def value(self, key):              # not to be confused with 'key' in rest of the code
        if key not in self.func:
            self.func[key] = random.uniform(0,1)
        return self.func[key]

class Query:
    def __init__(self, key, attr, T_q, gamma):
        self.key = key      
        self.attr = attr             
        self.T_q = T_q
        self.p_q = gamma
        self.n_q = int(T_q * gamma)

def which_coupon(attr, hashval):
    global attr_to_querylist
    
    for query in attr_to_querylist[attr]:
        if hashval >= query.p_q:
            hashval -= query.p_q
        else:
            return (query, attr)
    return (None, attr)

class Packet:
    def __init__(self, pac_info):
        self.pac_info = pac_info      # has srcIP, dstIP, srcPort, dstPort, ... in some fixed order

    def get_timestamp(self):
        return self.pac_info[5];      # TODO: modify accordingly

    def extract(self, indset):        # get values for some index subset from pac_info
        val = []
        for ind in indset:
            val.append(self.pac_info[ind])
        return tuple(val)

    def collect_coupon_from_attr(self, attr):
        global attr_to_hashfunc

        attrval = self.extract(attr)
        hashval = attr_to_hashfunc[attr].value(attrval)
        # query, coupon = which_coupon(attr, hashval)
        # print(hashval)
        # if query != None:
        #     print(query.key)
        # else:
        #     print(query)
        # print(coupon)
        # print()
        return which_coupon(attr, hashval)

    def collect_coupon(self):
        global attributes

        collected = []
        for attr in attributes:
            query, attr = self.collect_coupon_from_attr(attr)
            if query != None:
                collected.append((query, attr))

        # print(len(collected))
        if len(collected) == 1:
            return collected[0]
        elif len(collected) == 2:
            return collected[random.getrandbits(1)]
        else:
            return (None, None)


class HLLTable:
    # not doing checksum stuff now. Assuming not too many (query, key) pairs that will be active
    # also ignoring onehot(c) thing

    table = {}                    # map each (q, k) to a 0/1 list of length m_q               
    table_count = {}              # map each (q, k) to no. of ones in above list
    table_timestamp = {}          # map each (q, k) to a timestamp
    W = 0

    def __init__(self, W):        # timestamp expire time
        self.W = W

    def add_packet(self, packet):
        query, attr = packet.collect_coupon()
        if query == None:
            return
        keyval = packet.extract(query.key)

        qk_pair = (query, keyval)
        timestamp = packet.get_timestamp()

        if qk_pair not in self.table.keys() or self.table_timestamp[qk_pair] < timestamp - self.W:
            self.table_timestamp[qk_pair] = timestamp
            self.table[qk_pair] = HyperLogLog(EST)
            self.table_count[qk_pair] = self.table[qk_pair].cardinality()

        self.table[qk_pair].add(str(attr)) # expect attr to be string
        self.table_count[qk_pair] = self.table[qk_pair].cardinality

        if self.table_count[qk_pair] == query.n_q:
            # TODO
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
queries = [Query(frozenset([1]), frozenset([1,3]), 50, 1/2),  
            Query(frozenset([1, 2]), frozenset([1,3]), 50, 1/2),
            Query(frozenset([1,3,5]), frozenset([1,3]), 50, 1/2),
            Query(frozenset([1,3,2]), frozenset([1,3]), 50, 1/2),
            Query(frozenset([2,1,0]), frozenset([2,4,4]), 2, 1/2),
            Query(frozenset([3, 2]), frozenset([2,3,0]), 2, 1/2),
            Query(frozenset([4]), frozenset([1]), 50, 1/2)]
packets = [Packet([0,1,2,3,4,5]),
            Packet([1, 1, 3, 4, 5, 6]),
            Packet([2, 1, 4, 5, 0, 1]), 
            Packet([3, 1, 5, 0, 1, 2])]

attributes = {}
attr_to_querylist = {}
attr_to_hashfunc = {}

pre_process()

hlltable = HLLTable(5);

for pack in packets:
    hlltable.add_packet(pack)


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

######################################################################

hll = HyperLogLog(6)
data = range(5000)
for i in data:
    if random.random() > 0.2:
        hll.add(str(i) + str(random.random()))
hll.cardinality()