#!/usr/bin/env python

import csv
import sys

import json
import urllib
import urllib2


bay_area = ['0akland', 'Bay Area', 'Berkeley', 'California', 'Palo Alto',
  'Mountain View', 'MTV', 'San Francisco', 'San Jose', 'Silicon Valley',
  'SingularValley', 'Stanford', 'Sunnyvale', 'Los Altos', 'Menlo Park',
  'Mountain View', 'Oakland', 'Sacramento', 'San Carlos', 'Redwood',
  'San Mateo', 'Santa Clara', 'Santa Cruz', 'Sunnyvale', 'Union City',
  'San Ramon', 'Roseville']
bay_area_c = ['SF']

"""
bay_area_c = ['NY', 'IL', 'MA']
bay_area = ['New York', 'Chicago', 'Boston']


bay_area_c = ['WA']
bay_area = ['Seattle', 'Redmond', 'Richland']
"""


bay_area_n = ['Montreal', 'New York', 'Chicago', 'Los Angele', 'Pasadena',
  'Colorado', 'Portland', 'Santa Monica', 'Saint Petersburg', 'Los Angeles',
  'Irvine', 'Covina', 'Palmdale', 'San Diego', 'La Jolla', 'Johannesburg', 'China']

csvfile = open(sys.argv[1], 'rU')
ireader = csv.reader(csvfile)

headers = ireader.next()

o_csvfile = open(sys.argv[2], 'wb')
iwriter = csv.writer(o_csvfile)

iwriter.writerow(headers)

col_index = {}
i = 0
for h in headers:
  col_index[h] = i
  i += 1

for row in ireader:
  added = False

  #if len(row) != len(headers):
  #  print row
  #  continue

  location = row[col_index['location']]

  contact_loc = ''
  if col_index['contact_loc'] < len(row):
    contact_loc = row[col_index['contact_loc']]

  if contact_loc.lower() != location.lower():
    row[col_index['location']] += ' \n' + contact_loc

  if contact_loc != '' and contact_loc is not None:
    location = contact_loc


  for l in bay_area:
    if location.lower().find(l.lower()) >= 0:
      added = True
      break

  for l in bay_area_c:
    if location.find(l) >= 0:
      added = True
      break

  #if location == '':
  # added = True

  # followers = int(row[col_index['followers']])
  # if added and followers < 5:
  #   added = False

  for l in bay_area_n:
    if location.lower().find(l.lower()) >= 0:
      added = False
      break

  bio = row[col_index['bio']]
  company = row[col_index['company']]
  email = row[col_index['email']]
  blog = row[col_index['blog']]

  if bio == '' and company == '' and email == '' and blog == '':
    continue

  #for i in range(len(row)):
  #  if row[i].lower().find('founder') >= 0:
  #    added = True

  contact_angellist = row[col_index['contact_angellist']]
  contact_linkedin = row[col_index['contact_linkedin']]

  #if contact_angellist != '':
  #  added = True

  if added:
    iwriter.writerow(row)
