#!/usr/bin/env python3

from collections import defaultdict
import sys


FLDS = ['srcIP', 'dstIP', 'srcPort', 'dstPort', 'timestamp']

class Query:
  # initialize by parsing query string
  def __init__(self, s):
    qn, keys, attrs, logp, m, n = s.strip().split()
    self.queryNum = int(qn)
    self.keys = set(keys.split(','))
    self.attrs = set(attrs.split(','))
    for f in self.keys:
      assert f in FLDS
    for f in self.attrs:
      assert f in FLDS
    self.logp = int(logp)
    self.m = int(m)
    self.n = int(n)
    assert self.n <= self.m

  def set_masked(self, flds):
    return [' '.join(f'masked.{fld} = ' + (f'pkt->{fld}' if fld in flds else '0') + ';' for fld in FLDS)]

  def init_attr(self):
    return self.set_masked(self.attrs) + ['h = hash(&masked);']

  def call_query(self, start):
    shift = 32 - self.logp
    per_coupon = (1 << shift)
    end = start + per_coupon * self.m
    assert end <= (1 << 32)
    lines = []
    lines.append(f'{"}"} else if ({start} <= h && h <= {end-1}) {"{"}')
    lines += ['  ' + l for l in self.set_masked(self.keys)]
    lines.append(f'  queueCollection(ctx, {self.queryNum}, {self.n}, (h-{start}) >> {shift}, &masked);')
    return lines, end

queries_by_attrs = defaultdict(list)
for l in sys.stdin.readlines():
  l = l.strip()
  if len(l) == 0 or l[0] == '#':
    continue
  q = Query(l)
  queries_by_attrs[','.join(q.attrs)].append(q)

lines = []
for qs in queries_by_attrs.values():
  assert len(qs) >= 1
  lines += qs[0].init_attr()
  lines.append('if (false) {')
  x = 0
  for q in qs:
    source, x = q.call_query(x)
    assert x <= (1 << 32)
    lines += source
  lines.append('}')
  lines.append('')

for line in lines:
  print('  ' + line)
