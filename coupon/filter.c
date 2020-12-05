#define KBUILD_MODNAME "filter"
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <linux/udp.h>
#include <linux/kernel.h>
/** Note: using global variables in this file may cause segfault. 
 */
enum ip_attr {
  srcIP = 0,
  dstIP = 1,
  srcPort = 2,
  dstPort = 3,
  timestamp = 4,
};

struct data_t {
  __be32 srcIP;
  __be32 dstIP;
  __be16 srcPort;
  __be16 dstPort;
  uint32_t timestamp;
};

struct table_key_t {
  int16_t queryNum;
  struct data_t queryKey;
};

typedef uint64_t entry_t;

BPF_HASH(stats, struct table_key_t, entry_t);
// BPF_PERF_OUTPUT(events);

static void collect(int16_t queryNum, uint8_t queryN, uint8_t couponNum, struct data_t* queryKey) {
  struct table_key_t key;
  key.queryNum = queryNum;
  key.queryKey = *queryKey;

  entry_t x = 1u << couponNum;
  entry_t* p = stats.lookup(&key);
  if (p == NULL) {
    stats.update(&key, &x);
  } else {
    x |= *p;
    *p = x;
  }

  if (__builtin_popcount(x) >= queryN) {
    /*   bpf_trace_printk("hit threshold for query %d!", queryNum); */
  }
}

// TODO actually enqueue here, using BPF_PERCPU_ARRAY likely
#define queueCollection collect

#define setFld(f, p, d, m) (d)->f = ((m) & 1 << f) ? (p)->f : 0
#define populateData(p, d, m) setFld(srcIP, p,d,m); setFld(dstIP, p,d,m); setFld(srcPort, p,d,m); setFld(dstPort, p,d,m); setFld(timestamp, p,d,m)
#define clr(m) m.srcIP=0, m.dstIP=0, m.srcPort=0, m.dstPort=0, m.timestamp=0

static uint32_t hash(struct data_t* data) {
  uint64_t x = ((uint64_t)data->srcIP << 32) + (uint64_t)data->dstIP;
  uint64_t y = ((uint64_t)data->srcPort << 48) + ((uint64_t)data->dstPort << 32) + (uint64_t)data->timestamp;
  x = x * 3935559000370003845LL + 2691343689449507681LL;
  y = y * 8327418273481278347LL + 8374128374718273187LL;
  x ^= y;

  x ^= x >> 21;
  x ^= x << 37;
  x ^= x >>  4;

  x *= 4768777513237032717;

  x ^= x << 20;
  x ^= x >> 41;
  x ^= x <<  5;

  return x >> 32 ^ x;
}

static void processPacket(struct data_t* pkt) {
  collect(-1,0,0,pkt);
  struct data_t masked;
  uint32_t h;
#if 1
  /* populateData(pkt, &masked, 1 << dstPort); */
  clr(masked); masked.timestamp = pkt->timestamp;
  h = hash(&masked);
  if (false) { // just to make formatting consistent
  } else if (0u << 30 <= h && h <= (1u << 30) - 1) {
    populateData(pkt, &masked, 1 << srcPort);
    queueCollection(0, 4, (h - (0u << 30)) >> 28, &masked);
  } else if (1u << 30 <= h && h <= (2u << 30) - 1) {
    populateData(pkt, &masked, 1 << srcIP | 1 << srcPort);
    queueCollection(1, 8, (h - (1u << 30)) >> 27, &masked);
  }
#else
#include "queries.h"
#endif
}

int monitor(struct xdp_md *ctx) {
  bpf_trace_printk("got a packet\n");
  void *data = (void *)(long)ctx->data;
  void *data_end = (void *)(long)ctx->data_end;
  struct ethhdr *eth = data;
  if ((void*)eth + sizeof(*eth) <= data_end) {
    struct iphdr *ip = data + sizeof(*eth);
    if ((void*)ip + sizeof(*ip) <= data_end) {
      if (ip->protocol == IPPROTO_UDP) {
        struct udphdr *udp = (void*)ip + sizeof(*ip);
        if ((void*)udp + sizeof(*udp) <= data_end) {
          struct data_t packet;
          packet.srcIP = ip->saddr;
          packet.dstIP = ip->daddr;
          packet.srcPort = udp->source;
          packet.dstPort = udp->dest;
          packet.timestamp = bpf_ktime_get_ns();
          processPacket(&packet);
        }
      }
    }
  }
  return XDP_PASS;
}
