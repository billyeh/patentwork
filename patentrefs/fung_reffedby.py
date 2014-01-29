#!/usr/bin/env python

import csv, json, os, sqlite3
from urllib import urlopen

## Process reffedby.csv into a random sample of 200
## patents, showing each patent which references it

random_patents = []

print('Checking for data from Fung Institute...')
try:
  with open('clean_200_random.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
      random_patents += row
except:
  print('Error: download clean_200_random.csv first, link in readme')
  raise SystemExit

samples = ''

if not os.path.exists('reffedby_sample.csv'):
  try:
    conn = sqlite3.connect('citations_and_refs_mar262013.sqlite3')
  except:
    print('Error: download citations_and_refs_mar262013.sqlite3 first, link in readme')
    raise SystemExit
  for patent in random_patents:
    print(patent)
    for row in conn.execute('SELECT * FROM reffedby WHERE patent=? OR patent=?', ['0' + patent, patent]):
      if row[0][0] != '0':
        row = ['0' + row[0], row[1]]
      samples += ','.join(row) + '\n'

  with open('reffedby_sample.csv', 'w+') as newfile:
    newfile.write(samples)

## Note: selected random patents and references now extracted to reffedby_sample.csv

## Turn the sample of patents from our data referencing each random
## patent into a hash

fung_ref_hash = {}

with open('reffedby_sample.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  for row in reader:
    if (row[0][1:] not in fung_ref_hash.keys()):
      fung_ref_hash[row[0][1:]] = []
    fung_ref_hash[row[0][1:]] += [row[1]]

  open('fung_ref_hash.json', 'w').write(json.dumps(fung_ref_hash, indent=2))

## Note: ref data now in fung_ref_hash.json

print('Done!')
