import enum 

class ip_attr(enum.IntEnum):
  srcIP = 0
  dstIP = 1
  srcPort = 2
  dstPort = 3
  timestamp = 4

def writeToFile(file, mask, threhold, numRequired, numCoupon):
    file.write("%d %d %d %d\n" % (mask, threhold, numRequired, numCoupon))

with open("queries.txt", "w+") as file:
  writeToFile(file, 1 << ip_attr.srcPort, 100, 4, 4)
  writeToFile(file, 1 << ip_attr.srcPort | 1 << ip_attr.srcIP, 100, 4, 4)


