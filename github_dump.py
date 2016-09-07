#!/usr/bin/env python

import re

# <https://api.github.com/repositories/45717250/forks?sort=oldest&page=2>; rel="next", <https://api.github.com/repositories/45717250/forks?sort=oldest&page=442>; rel="last"
def getNextLink(link):
  ex_next = '.*<([^<>]+)>; rel="next".*'
  ex_last = '.*<([^<>]+)>; rel="last".*'

  mn = re.match(ex_next, link)
  ml = re.match(ex_last, link)

  next_link = ''
  last_link = ''

  if mn: next_link = mn.group(1)
  if ml: last_link = ml.group(1)

  return (next_link, last_link)

"""
u 'owner': {
      u 'following_url': u 'https://api.github.com/users/rockt/following{/other_user}',
      u 'events_url': u 'https://api.github.com/users/rockt/events{/privacy}',
      u 'organizations_url': u 'https://api.github.com/users/rockt/orgs',
      u 'url': u 'https://api.github.com/users/rockt',
      u 'gists_url': u 'https://api.github.com/users/rockt/gists{/gist_id}',
      u 'html_url': u 'https://github.com/rockt',
      u 'subscriptions_url': u 'https://api.github.com/users/rockt/subscriptions',
      u 'avatar_url': u 'https://avatars.githubusercontent.com/u/1196835?v=3',
      u 'repos_url': u 'https://api.github.com/users/rockt/repos',
      u 'received_events_url': u 'https://api.github.com/users/rockt/received_events',
      u 'gravatar_id': u '',
      u 'starred_url': u 'https://api.github.com/users/rockt/starred{/owner}{/repo}',
      u 'site_admin': False,
      u 'login': u 'rockt',
      u 'type': u 'User',
      u 'id': 1196835,
      u 'followers_url': u 'https://api.github.com/users/rockt/followers'
    }
"""
def getFork(value):
  stargazers_count = value['stargazers_count']
  owner_url = value['owner']['url']
  return (stargazers_count, owner_url)

import sys
import json
import urllib2
import urlparse

def getNextPage(url, access_token):
  if access_token != '':
    url += '&access_token=' + access_token

  response = urllib2.urlopen(url)
  (next_link, last_link) = getNextLink(response.headers['Link'])
  ratelimit_remain = int(response.headers['X-RateLimit-Remaining'])

  parts = urlparse.parse_qs(next_link)
  index = int(parts['page'][0])


  last_parts = urlparse.parse_qs(last_link)
  last_index = int(last_parts['page'][0])

  data = response.read()
  values = json.loads(data)

  owners = []
  for value in values:
    owner = getFork(value)
    owners.append(owner)

  return (ratelimit_remain, owners, next_link, last_link)


from pprint import pprint

access_token = ''
if len(sys.argv) > 1:
  access_token = sys.argv[1]

next_link = "https://api.github.com/repos/tensorflow/tensorflow/forks?sort=oldest" # &page=440"

next_next_link = next_link
last_link = ''

ratelimit_remain = 100
owners = []

while ratelimit_remain > 45 and next_link != last_link:
  print 'ratelimit_remain', ratelimit_remain
  print 'next_link', next_link

  sys.stdout.flush()

  (ratelimit_remain, new_owners, next_next_link, last_link) = getNextPage(next_link, access_token)
  owners.extend(new_owners)

  next_link = next_next_link

uniq_owners = {}
for owner in owners:
  (stars, owner_url) = owner
  if owner_url not in owners:
    uniq_owners[owner_url] = (int(stars), 0)
  else:
    (pre_stars, count) = uniq_owners[owner_url]
    uniq_owners[owner_url] = (pre_stars + int(stars), count + 1)

if len(sys.argv) > 2:
  with open(sys.argv[2], 'w') as outfile:
    json.dump(uniq_owners, outfile, indent=2) 
else:
 pprint(uniq_owners)

