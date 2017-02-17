#!/usr/bin/env python

import csv
import sys

import json
import urllib
import urllib2

def getFullcontact(email, apiKey):
  url = "https://api.fullcontact.com/v2/person.json?"

  params = {'email': email}
  url += urllib.urlencode(params)

  print url, ' ', api_key
  
  headers = {'X-FullContact-APIKey': apiKey}

  req = urllib2.Request(url, headers=headers)
  contact = None

  try:
    response = urllib2.urlopen(req)
    contact = json.loads(response.read())
  except urllib2.HTTPError, e:
    if e.code == 404:
      print '404', url
      return None

    print e.code
    print e.msg
    print e.headers
    print e.fp.read()

  return contact

fullcontact_headers = ['contact_websites', 'contact_org', 'contact_angellist',
  'contact_linkedin', 'contact_profiles', 'contact_websites', 'contact_org',
  'contact_loc']

def addContactToOwner(contact, owner):
  owner['contact_websites'] = ''
  owner['contact_org'] = ''

  owner['contact_angellist'] = ''
  owner['contact_linkedin'] = ''
  owner['contact_profiles'] = ''

  owner['contact_websites'] = ''
  owner['contact_loc'] = ''
  owner['contact_org'] = ''

  if contact is None:
    return

  if 'contactInfo' in contact and 'websites' in contact['contactInfo']:
    for web in contact['contactInfo']['websites']:
      owner['contact_websites'] += web['url'].encode('utf-8') + '\n'

  if 'organizations' in contact:
    for org in contact['organizations']:
      title = ''
      name = ''

      if 'title' in org:
        title = org['title'].encode('utf-8')
      if 'name' in org:
        name = org['name'].encode('utf-8')

      owner['contact_org'] += name + '/' + title + '\n'

  if 'demographics' in contact:
    demo = contact['demographics']

    if 'locationDeduced' in demo:
      if 'deducedLocation' in contact['demographics']['locationDeduced']:
        owner['contact_loc'] = contact['demographics']['locationDeduced'][
          'deducedLocation'].encode('utf-8')
      else:
        if 'city' in contact['demographics']['locationDeduced'
          ] and 'state' in contact['demographics']['locationDeduced']:
          owner['contact_loc'] = contact['demographics']['locationDeduced'][
          'city']['name'].encode('utf-8') + ', ' + contact['demographics'][
          'locationDeduced']['state']['name'].encode('utf-8')
        else:
          owner['contact_loc'] = contact['demographics']['locationGeneral'
            ].encode('utf-8')

    elif 'locationGeneral' in demo:
      owner['contact_loc'] = contact['demographics'][
        'locationGeneral'].encode('utf-8')

  if 'socialProfiles' in contact:
    for profile in contact['socialProfiles']:
      type = ''
      if 'type' in profile:
        type = profile['type']
      else:
        type = profile['typeName'].lower()

      if type == 'angellist':
        owner['contact_angellist'] = profile['url'].encode('utf-8')
      elif type == 'linkedin':
        owner['contact_linkedin'] = profile['url'].encode('utf-8')
      else:
        owner['contact_profiles'] += profile['url'].encode('utf-8') + ' \n'

csvfile = open(sys.argv[1], 'rU')
ireader = csv.reader(csvfile)

headers = ireader.next()
headers += fullcontact_headers

api_key = sys.argv[3]

col_index = {}
i = 0
for h in headers:
  col_index[h] = i
  i += 1

relevant_rows = []


o_csvfile = open(sys.argv[2], 'wb')
iwriter = csv.writer(o_csvfile)

iwriter.writerow(headers)

skip_email = ''
skipping = False

if len(sys.argv) > 4:
  skip_email = sys.argv[4]
  skipping = True

for row in ireader:
  if len(row) == 0:
    print 'bad row'
    continue

  if len(row) <= col_index['email']:
    print row
    print col_index['email']

  email = row[col_index['email']]

  if skipping:
    if skip_email != '' and skip_email == email:
      skipping = False
    else:
      continue

  contact = None
  if email != '' and email is not None:
    contact = getFullcontact(email, api_key)

  contact_owner = {}
  addContactToOwner(contact, contact_owner)

  delta = len(headers) - len(fullcontact_headers) - len(row)
  if delta > 0:
   print 'padding: ', delta
   for i in range(delta):
     row.append('')

  for fch in fullcontact_headers:
    row.append(contact_owner[fch])

  relevant_rows.append(row)
  iwriter.writerow(row) # s(relevant_rows)
