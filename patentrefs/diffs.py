#!/usr/bin/env python

import json

fung = json.loads(open('fung_ref_hash.json').read())
uspto = json.loads(open('uspto_ref_hash.json').read())
google = json.loads(open('google_ref_hash.json').read())

for patent in fung.keys():
  print("*" + patent + ' ' + str(len(fung[patent])) + ' ' + str(len(uspto[patent])) + ' ' + str(len(google[patent])))

  fung_pats = ''
  for ref in fung[patent]:
    if ref not in google[patent] and ref not in fung[patent]:
      fung_pats += ' ' + ref
  if len(fung_pats) != 0:
    print('Fung has ' + fung_pats)

  uspto_pats = ''
  for ref in uspto[patent]:
    if ref not in fung[patent] and ref[:2] != '0D':
      uspto_pats += ' ' + ref
  if len(uspto_pats) != 0:
    print('USPTO has ' + uspto_pats)

  google_pats = ''
  for ref in google[patent]:
    if ref.replace('US', '0') not in fung[patent]:
      google_pats += ' ' + ref
  if len(google_pats) != 0:
    print('Google has ' + google_pats)
