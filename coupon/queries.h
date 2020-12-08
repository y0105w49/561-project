  masked.srcIP = 0; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 4026531839) {
    masked.srcIP = pkt->srcIP; masked.dstIP = 0; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
    key.queryNum = 1;
    queueCollection(ctx, 20, (h-0) >> 27, &key);
  }
  
  masked.srcIP = pkt->srcIP; masked.dstIP = 0; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 2013265919) {
    masked.srcIP = 0; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
    key.queryNum = 2;
    queueCollection(ctx, 20, (h-0) >> 26, &key);
  }
  
  masked.srcIP = 0; masked.dstIP = 0; masked.srcPort = 0; masked.dstPort = pkt->dstPort; masked.timestamp = 0;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 1073741823) {
    masked.srcIP = pkt->srcIP; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
    key.queryNum = 3;
    queueCollection(ctx, 2, (h-0) >> 28, &key);
  }
  
  masked.srcIP = 0; masked.dstIP = 0; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = pkt->timestamp;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 805306367) {
    masked.srcIP = pkt->srcIP; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = 0; masked.timestamp = 0;
    key.queryNum = 4;
    queueCollection(ctx, 3, (h-0) >> 28, &key);
  } else if (805306368 <= h && h <= 2952790015) {
    masked.srcIP = pkt->srcIP; masked.dstIP = pkt->dstIP; masked.srcPort = pkt->srcPort; masked.dstPort = pkt->dstPort; masked.timestamp = 0;
    key.queryNum = 5;
    queueCollection(ctx, 6, (h-805306368) >> 28, &key);
  }
  
  masked.srcIP = pkt->srcIP; masked.dstIP = 0; masked.srcPort = pkt->srcPort; masked.dstPort = 0; masked.timestamp = 0;
  h = hash(&masked);
  if (false) {
  } else if (0 <= h && h <= 1073741823) {
    masked.srcIP = 0; masked.dstIP = pkt->dstIP; masked.srcPort = 0; masked.dstPort = pkt->dstPort; masked.timestamp = 0;
    key.queryNum = 6;
    queueCollection(ctx, 6, (h-0) >> 27, &key);
  }
  
