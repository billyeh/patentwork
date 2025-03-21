#!/usr/bin/env python

import os.path
import ast
import requests
import sys

from bs4 import BeautifulSoup
from multiprocessing import Process

partition_size = 100000

def gather_data():
  file_name = 'app_ids'
  if not os.path.isfile(file_name):
    app_ids = []
    for app_num, date in app_session.query(App_Application.number, App_Application.date):
      if app_num and date:
        print(str(date.year) + '/' + app_num)
        app_ids.append(str(date.year) + '/' + app_num)
    open(file_name, 'a+').write(str(app_ids))
  else:
   print('Already have app_ids file')

def match_ids(r):
  app_ids = ast.literal_eval(open('./parts/' + str(r[0]) + '.' + str(r[1]) + '.part', 'r').read())
  file_path = './data/' + str(r[0]) + '.' + str(r[1])
  if os.path.isfile(file_path):
    start = len(open(file_path, 'a+').read().split('\n'))
  else:
    start = 0
  for i in range(start, partition_size):
    year, app_id = app_ids[i].split('/')
    uspto_id = get_id(app_id, year)
    if uspto_id:
      print(uspto_id)
      open(file_path, 'a+').write(app_ids[i] + ' ' + uspto_id + '\n')

def get_id(id, year):
  url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=1&f=G&l=50&s1=%22_______%22.PGNR.&OS=DN/_______&RS=DN/_______'
  query_url = url.replace('_______', id)
  soup = BeautifulSoup((requests.get(query_url)._content), "lxml")
  for d in soup.find_all('b'):
    if d.string:
      numbers = d.string.strip().split('/')
      if len(numbers) == 2:
        s1, s2 = numbers
        if len(s1) == 2 and len(s2) == 6:
          return str(year) + '/' + d.string.strip().replace('/', '')

def match_range(i):
  lower = i * partition_size
  upper = (i + 1) * partition_size
  print('Starting ' + str(lower) + ',' + str(upper) + '...')
  match_ids([lower, upper])

def main(parts_to_run):
  gather_data()
  jobs = []
  for i in parts_to_run:
    p = Process(target=match_range, args=(i,))
    jobs.append(p)
    p.start()

if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.exit('Specify the jobs you want to be run')
  partitions_to_run = []
  try:
    for arg in sys.argv[1:]:
      partitions_to_run.append(int(arg))
  except:
    sys.exit('Error reading arguments, must be integers')
  main(partitions_to_run)
