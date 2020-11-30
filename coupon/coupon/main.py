#!/usr/bin/env python3
from bcc import BPF
import time
from ctypes import * # c_uint8, c_uint16

mode = "DEBUG"

def fmtIP(x):
  octets = [x>>24, (x>>16)&255, (x>>8)&255, x&255]
  octets = octets[::-1]
  return f'{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}'
def fmtPort(x):
  return (x>>8) + ((x&255)<<8)

def print_event():
  print('all coupons:')
  for key, coups in b["stats"].items():
    query = key.queryKey
    print(f'coupon for query #{key.queryNum:2}, '
          f'key {fmtIP(query.srcIP):>15}:{fmtPort(query.srcPort):<5} '
          f'-> {fmtIP(query.dstIP):>15}:{fmtPort(query.dstPort):<5} '
          f't={query.timestamp%1000:03d}, collected {bin(coups.value)}')
  print()
# b["events"].open_perf_buffer(print_event)
print('loaded!')

def enqueue(queryNum, mask, threhold, numRequired, numCoupons):
  b["queries"][queryNum] = (c_uint8 *4)(mask, threhold, numRequired, numCoupons)
   
device = "lo"
b = BPF(src_file="filter.c")
fn = b.load_func("monitor", BPF.XDP)
b.attach_xdp(device, fn, 0)
   
with open("queries.txt", "r+") as file:
  queryNum = 0
  for line in file:
    mask, threhold, numRequired, numCoupons = [int(x) for x in line.split()]
    enqueue(queryNum, mask, threhold, numRequired, numCoupons)
    queryNum += 1

if (mode == "DEBUG"):
  print('DEBUG: all queries:')
  for key, q in b["queries"].items():
    print(f'queryNum {key}: mask {q.mask}, threhold {q.threshold}, m {q.numCoupons}, n {q.numRequired}')

'''
while(True):
  print_event()
  # b.trace_print()
  time.sleep(2)
'''
try:
  b.trace_print()
  # b.perf_buffer_poll()
  print(b["stats"].items())
except KeyboardInterrupt:
  pass

b.remove_xdp(device, 0)
