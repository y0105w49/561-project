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

struct query_t {
  uint8_t mask;
  uint8_t threshold;
  uint8_t numRequired;
  uint8_t numCoupons;
};
#define SIZE 16
#define SIZEEXP 4
typedef uint64_t entry_t;
BPF_HASH(stats, struct table_key_t, entry_t);
BPF_ARRAY(queries, struct query_t, SIZE);  

// BPF_PERF_OUTPUT(events);

static bool isQueryValid(struct query_t* query){
  if (query == NULL)
    return false; 
  return (query->mask | query->threshold | query->numRequired | query->numCoupons) != 0;
}

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
// Linda: why PERCPU_ARRAY instead of ARRAY? 
#define queueCollection collect

#define setFld(f, p, d, m) (d)->f = ((m) & 1 << f) ? (p)->f : 0
#define populateData(p, d, m) setFld(srcIP, p,d,m); setFld(dstIP, p,d,m); setFld(srcPort, p,d,m); setFld(dstPort, p,d,m); setFld(timestamp, p,d,m)
#define clr(m) m.srcIP=0, m.dstIP=0, m.srcPort=0, m.dstPort=0, m.timestamp=0

// Changed hash function to one with larger multiplicative  
static uint32_t hash(struct data_t* data) {
  uint64_t x1 = ((uint64_t)data->srcIP << 32) + (uint64_t)data->dstIP;
  uint64_t x2 = ((uint64_t)data->srcPort << 48) + ((uint64_t)data->dstPort << 32) + (uint64_t)data->timestamp;
  uint64_t x = x1 ^ x2; 
  x = x * 3935559000370003845 + 2691343689449507681;

  x ^= x >> 21;
  x ^= x << 37;
  x ^= x >>  4;

  x *= 4768777513237032717;

  x ^= x << 20;
  x ^= x >> 41;
  x ^= x <<  5;

  return x;
}

//TODO: use log function to find query hash range instead of hard code 
static void processPacket(struct data_t* pkt) {
  struct data_t masked;
  clr(masked); 
  masked.timestamp = pkt->timestamp;
  uint32_t h = hash(&masked);
  int i = h >> (32 - SIZEEXP);
  struct query_t* query = queries.lookup(&i);
  if (isQueryValid(query)){
    populateData(pkt, &masked, query->mask);
    uint32_t h2 = hash(&masked);
    uint32_t couponNum = ((uint64_t)(h2)*(uint64_t)(query->threshold) >> 32);
    //bpf_trace_printk("coupon %d being considered", couponNum);
    if (couponNum < query->numCoupons){
      queueCollection(i, query->numRequired, couponNum, &masked);
    }
  } 
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

