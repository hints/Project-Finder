#!/usr/bin/env python

import csv
import json
import sys

filename = sys.argv[1]
with open(filename) as json_file:
  owner_map = json.load(json_file)

f = open(sys.argv[2], "wb+")
w = None

for (url, owner) in owner_map.items():
  # print 'owner:', owner
  if w is None:
    w = csv.DictWriter(f, owner.keys())
    w.writeheader()

  uni = ['name', 'company', 'location', 'blog']
  for u in uni:
    if owner[u] is not None:
      owner[u] = owner[u].encode('utf-8')

  w.writerow(owner)

