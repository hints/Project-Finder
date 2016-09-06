#!/usr/bin/env python

import re

# <https://api.github.com/repositories/45717250/forks?sort=oldest&page=2>; rel="next", <https://api.github.com/repositories/45717250/forks?sort=oldest&page=442>; rel="last"
def getNextLink(link):
  links = re.split('<|>', link)
  # links = link.split('< >')
  print links
  return (links[1], links[-2])

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

import json
import urllib2

def getNextPage(url):
  response = urllib2.urlopen(url)
  (next_link, last_link) = getNextLink(response.headers['Link'])
  ratelimit_remain = int(response.headers['X-RateLimit-Remaining'])
  index = int(next_link.split('=')[-1]) - 1
  last_index = int(last_link.split('=')[-1])

  data = response.read()
  values = json.loads(data)

  owners = []
  for value in values:
    owner = getFork(value)
    owners.append(owner)

  return (ratelimit_remain, owners, next_link)

next_link = "https://api.github.com/repos/tensorflow/tensorflow/forks?sort=oldest"
ratelimit_remain = 100
owners = []

while ratelimit_remain > 45:
  (ratelimit_remain, new_owners, url) = getNextPage(next_link)
  owners.extend(new_owners)

print ratelimit_remain
print next_link
print owners
