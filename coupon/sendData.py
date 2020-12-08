#!/usr/bin/env python 
import numpy as np 
import sys
import socket
from scapy.all import DNS, DNSQR, DNSRR, IP, send, sniff, sr1, UDP

if (len(sys.argv) != 2):
  print("usage: readData.py \{filename\}.npy") 
Trace=np.load(sys.argv[1])
print(Trace[0])
for i in len(Trace):
# for i in range(10):
  srcIP = socket.inet_ntoa(Trace[i][1])
  dstIP = socket.inet_ntoa(Trace[i][2]) 
  packet=IP(dst=dstIP,src=srcIP)/UDP(dport=Trace[i][4],sport=Trace[i][3])
  send(packet)
