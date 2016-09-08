#!/usr/bin/env python

import csv
import sys

bay_area = ['0akland', 'Bay Area', 'Berkeley', 'California', 'Palo Alto',
  'Mountain View', 'MTV', 'San Francisco', 'San Jose', 'Silicon Valley',
  'SingularValley', 'Stanford', 'Sunnyvale']
bay_area_c = ['CA', 'SF']
bay_area_n = ['Montreal', 'New York', 'Chicago', 'Los Angele', 'Pasadena',
  'Colorado', 'Portland', 'Santa Monica', 'Saint Petersburg', 'Los Angeles',
  'Irvine', 'Covina', 'Palmdale', 'San Diego', 'La Jolla']

csvfile = open(sys.argv[1], 'rb')
ireader = csv.reader(csvfile)

headers = ireader.next()

col_index = {}
i = 0
for h in headers:
  col_index[h] = i
  i += 1

relevant_rows = []

for row in ireader:
  added = False
  location = row[col_index['location']]

  for l in bay_area:
    if location.lower().find(l.lower()) >= 0:
      # print 'loc: ', location.lower(), ' l:', l.lower()
      added = True
      break
 
  for l in bay_area_c:
    if location.find(l) >= 0:
      added = True
      break

  if location == '':
    added = True

  followers = int(row[col_index['followers']]) 
  if added and followers < 5:
    added = False

  for l in bay_area_n:
    if location.lower().find(l.lower()) >= 0:
      added = False
      break

  bio = row[col_index['bio']]
  company = row[col_index['company']]
  email = row[col_index['email']]
  blog = row[col_index['blog']]
  # organizations_url = row[col_index['organizations_url']]

  if bio == '' and company == '' and email == '' and blog == '':
    continue 

  if added:
    # print 'loc:', location
    relevant_rows.append(row)

o_csvfile = open(sys.argv[2], 'wb') 
iwriter = csv.writer(o_csvfile)

iwriter.writerow(headers)
iwriter.writerows(relevant_rows)

