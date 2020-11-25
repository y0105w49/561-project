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

// TODO: support key with multiple attribute
struct query_t {
  enum ip_attr key; 
  enum ip_attr attr;
  int threhold;
};

struct table_key_t{
  int query_num;
  long long query_key; 
}; 

//BPF_TABLE("hash", struct table_key_t, long long, stats, 10000);
BPF_HASH(stats, struct table_key_t, long long);
BPF_HASH(queries, int, struct query_t, 10000); 

// BPF_PERF_OUTPUT(events);

static long long getAttr(struct iphdr* ip, enum ip_attr attr){
  if (attr == srcIP)
    return ip->saddr;
  else if (attr == dstIP)
    return ip->daddr;
  else
    return 0;
}

static void updateQueries(){
  struct query_t query1;
  query1.key = srcIP;
  query1.attr = dstIP;
  query1.threhold = 100;
  struct query_t query2;
  query2.key = dstIP;
  query2.attr = srcIP;
  query2.threhold = 100;
  int one = 0;
  int two = 1;
  queries.update(&one, &query1);
  queries.update(&two, &query2);
}

static int incrementCoupon(struct iphdr* ip){
  updateQueries();
  // random find a query type to increment 
  struct table_key_t key;
  key.query_num = bpf_get_prandom_u32() % 2; // number of queries
  struct query_t* query = queries.lookup(&key.query_num);
  if (query == NULL){
    return -1;
  }
  key.query_key = getAttr(ip, query->key);
  long long query_val = getAttr(ip, query->attr);  
  // this hash is incorrect, need to use fixed seeded hashes 
  // for each attribute 
  if (bpf_get_prandom_u32() % query->threhold == 0){
    char coupon = bpf_get_prandom_u32() % 4; //number of coupons
    long long shift = 1 << coupon; 
    long long* count = stats.lookup(&key);
    
    if (count != NULL) 
      *count = *count | 1 << coupon; 
    else{ 
      stats.update(&key, &shift);
    }
    // long long count = *(stats.lookup(&key.query_key)) | 1 << coupon;   
  } 
  return 0;
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
        // newly added line to increment stats
         int success = incrementCoupon(ip);
         bpf_trace_printk("success or not: %d", success);
      }
    }
  }
  return XDP_PASS;
}

