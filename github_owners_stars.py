#!/usr/bin/env python

import sys
import json
import urllib2
import csv

from pprint import pprint

RATE_LIMIT = 500

HEADER = None

def readCsvUrls(blacklist_file):
  csvfile = open(blacklist_file, 'rb')
  ireader = csv.reader(csvfile)

  headers = ireader.next()
  index = {}
  i = 0
  for h in headers:
    index[h] = i
    i+=1

  u_i = index['url']
  urls = []

  for o in ireader:
    urls.append(o[u_i])

  return urls 

if len(sys.argv) <= 1:
  sys.exit(1)

access_token = sys.argv[1]
filename = sys.argv[2]

print filename

with open(filename) as json_file:
  owners = json.load(json_file)

blacklist = sys.argv[3]
b_urls = readCsvUrls(blacklist)

start_url = ''
if len(sys.argv) > 5:
  start_url = sys.argv[5]

skip = False

if start_url != '':
  skip = True

o_owner_map = {}

if len(sys.argv) > 4:
  outfile = open(sys.argv[4], 'w')
  iwriter = csv.writer(outfile)

for owner in owners:
  url = owner['url']

  if skip:
    if start_url == url: skip = False
    else: continue

  print 'url', url
  if url in b_urls:
    continue

  r_url = url
  if access_token != '':
    r_url += '?access_token=' + access_token

  try:
    response = urllib2.urlopen(r_url)
    owner = json.loads(response.read())
  except Exception:
    print 'failed to process', url
    pass

  ratelimit_remain = int(response.headers['X-RateLimit-Remaining'])
  print 'ratelimit_remain', ratelimit_remain
  sys.stdout.flush()

  if ratelimit_remain <= RATE_LIMIT:
    print 'last processed url', url
    break

  if HEADER is None:
    HEADER = []
    for o in owner:
      HEADER.append(o)
    iwriter.writerow(HEADER)

  row = []
  for o in owner:
    if isinstance(owner[o], basestring):
      row.append(owner[o].encode('utf-8'))
    else:
      row.append(owner[o])

  iwriter.writerow(row)

