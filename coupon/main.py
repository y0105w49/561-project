#!/usr/bin/env python3

import time

from bcc import BPF
from bcc.utils import printb
import ctypes as ct


device = "lo"
b = BPF(src_file="filter.c", cflags=["-I/vagrant/coupon"])
fn = b.load_func("monitor", BPF.XDP)
b.attach_xdp(device, fn, 0)

def fmtIP(x):
  octets = [x>>24, (x>>16)&255, (x>>8)&255, x&255]
  octets = octets[::-1]
  return f'{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}'
def fmtPort(x):
  return (x>>8) + ((x&255)<<8)

def print_coupons():
  print('all coupons:')
  for key, coups in b["stats"].items():
    query = key.queryKey
    if key.queryNum == -1:
      continue
    print(f'coupon for query #{key.queryNum:2}, '
          f'key {fmtIP(query.srcIP):>15}:{fmtPort(query.srcPort):<5} '
          f'-> {fmtIP(query.dstIP):>15}:{fmtPort(query.dstPort):<5} '
          f't={query.timestamp%1000:03d}, collected {bin(coups.value)}')

seen = set()
def print_event(cpu, data, size):
  qn = ct.cast(data, ct.POINTER(ct.c_short)).contents.value
  if qn in seen:
    return
  seen.add(qn)
  print(f'event {qn} triggered!')

b['events'].open_perf_buffer(print_event)

print('loaded!')

while(True):
  b.perf_buffer_poll()

  print_coupons()
  print()

  # b.trace_print()

  time.sleep(2)
'''
try:
  b.trace_print()
  # b.perf_buffer_poll()
  print(b["stats"].items())
except KeyboardInterrupt:
  pass
'''
b.remove_xdp(device, 0)
