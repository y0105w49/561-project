  masked.srcIP = 0; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 4026531839) {
    masked.srcIP = pkt->srcIP; masked.dstIP = 0; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
    queueCollection(1, 20, (h-0) >> 27, &masked);
  }
  
  masked.srcIP = pkt->srcIP; masked.dstIP = 0; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 2013265919) {
    masked.srcIP = 0; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
    queueCollection(2, 20, (h-0) >> 26, &masked);
  }
  
  masked.srcIP = 0; masked.dstIP = 0; masked.srcPort = 0; masked.dstPort = pkt->dstPort; masked.timestamp = 0;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 1342177279) {
    masked.srcIP = pkt->srcIP; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
    queueCollection(3, 10, (h-0) >> 27, &masked);
  }
  
  masked.srcIP = 0; masked.dstIP = 0; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = pkt->timestamp;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 805306367) {
    masked.srcIP = pkt->srcIP; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
    queueCollection(4, 3, (h-0) >> 28, &masked);
  } else if (805306368 <= h && h <= 1879048191) {
    masked.srcIP = pkt->srcIP; masked.dstIP = pkt->dstIP; masked.srcPort = pkt->srcPort; masked.dstPort = pkt->dstPort; masked.timestamp = 0;
    queueCollection(5, 6, (h-805306368) >> 27, &masked);
  }
  
  masked.srcIP = pkt->srcIP; masked.dstIP = 0; masked.srcPort = pkt->srcPort; masked.dstPort = 0; masked.timestamp = 0;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 1073741823) {
    masked.srcIP = 0; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = pkt->dstPort; masked.timestamp = 0;
    queueCollection(6, 6, (h-0) >> 27, &masked);
  }
  
