#!/usr/bin/env python

import sys
import json
import urllib2

from pprint import pprint

if len(sys.argv) <= 1:
  sys.exit(1)

access_token = sys.argv[1]
filename = sys.argv[2]

print filename

with open(filename) as json_file:
  owner_map = json.load(json_file)

owners = {}

for url in sorted(owner_map):

  r_url = url
  if access_token != '':
    r_url += '?access_token=' + access_token
  response = urllib2.urlopen(r_url)

  owner = json.loads(response.read())
  (stars, forks) = owner_map[url]

  owner['projfinder_fork_stars'] = stars
  owner['projfinder_fork_count'] = forks

  owner_map[url] = owner

  ratelimit_remain = int(response.headers['X-RateLimit-Remaining'])

  print 'ratelimit_remain', ratelimit_remain
  sys.stdout.flush()

  if ratelimit_remain <= 500:
    print 'last processed url', url
    break

if len(sys.argv) > 3:
  with open(sys.argv[3], 'w') as outfile:
    json.dump(owner_map, outfile, indent=2)
else:
  pprint(owner_map)

