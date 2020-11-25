#!/usr/bin/env python3
from bcc import BPF
import time

device = "lo"
b = BPF(src_file="filter.c")
fn = b.load_func("monitor", BPF.XDP)
b.attach_xdp(device, fn, 0)

def print_event():
  for k, v in b["stats"].items():
      print("%lld:  # of coupons: %d" %(k, v.value))

# b["events"].open_perf_buffer(print_event)

while(True):
  print_event()
  time.sleep(5)
'''
try:
  b.trace_print()
  # b.perf_buffer_poll()
  print(b["stats"].items())
except KeyboardInterrupt:
  pass
'''
b.remove_xdp(device, 0)
