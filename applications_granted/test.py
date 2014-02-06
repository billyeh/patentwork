#!/bin/python

import os
from ast import literal_eval
from fix_ids import get_id

def main():
  missingnos = {}
  errors = {}
  for filename in os.listdir('./data'):
    ids = open('./data/' + filename, 'r').read().split('\n')
    missingnos[filename] = set([x.split(' ')[0] for x in ids])

  golden_set = literal_eval(open('app_ids', 'r').read())

  for i, app_id in enumerate(golden_set):
    filename = get_filename(i)
    if app_id not in missingnos[filename]:
      year, app = app_id.split('/')
      correct_id = get_id(app, year)
      if correct_id:
        print(filename + ' missing ' + app_id + ', needs to have ' + correct_id)
        open('./data/' + filename, 'a+').write(app_id + ' ' + correct_id + '\n')
      else:
        if not filename in errors:
          errors[filename] = []
        errors[filename] += [app_id]

  log_errors(errors)

def get_filename(index):
  lower = index / 100000 * 100000
  if lower == 3000000 or lower == 3100000:
    lower = 3000000
    higher = 3137677
  else:
    higher = lower + 100000
  return str(lower) + '.' + str(higher)

def log_errors(errors):
  total = 0
  for filename in errors:
    total += len(errors[filename])
    print(filename + ': ' + str(errors[filename]))
  print(total)

if __name__ == '__main__':
  main()
