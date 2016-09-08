#!/usr/bin/env python

import sys
import json
import urllib2

from pprint import pprint

RATE_LIMIT = 500

if len(sys.argv) <= 1:
  sys.exit(1)

access_token = sys.argv[1]
filename = sys.argv[2]

print filename

with open(filename) as json_file:
  owner_map = json.load(json_file)

owners = {}

start_url = ''

if len(sys.argv) > 4:
  start_url = sys.argv[4]

skip = False

if start_url != '':
  skip = True

o_owner_map = {}

for url in sorted(owner_map):

  if skip:
    if start_url == url: skip = False
    else: continue

  print 'url', url

  r_url = url
  if access_token != '':
    r_url += '?access_token=' + access_token

  try:
    response = urllib2.urlopen(r_url)
    owner = json.loads(response.read())
  except Exception:
    print 'failed to process', url
    pass

  (stars, forks) = owner_map[url]

  owner['projfinder_fork_stars'] = stars
  owner['projfinder_fork_count'] = forks

  o_owner_map[url] = owner

  ratelimit_remain = int(response.headers['X-RateLimit-Remaining'])
  print 'ratelimit_remain', ratelimit_remain
  sys.stdout.flush()

  if ratelimit_remain <= RATE_LIMIT:
    print 'last processed url', url
    break

if len(sys.argv) > 3:
  with open(sys.argv[3], 'w') as outfile:
    json.dump(o_owner_map, outfile, indent=2)
else:
  pprint(o_owner_map)

print 'owners', len(o_owner_map)
