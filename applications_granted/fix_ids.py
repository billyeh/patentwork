import os.path
import ast
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process

def gather_data():
  if not os.path.isfile('app_ids'):
    app_ids = []
    for app_num, date in app_session.query(App_Application.number, App_Application.date):
      if app_num and date:
        print(str(date.year) + '/' + app_num)
        app_ids.append(str(date.year) + '/' + app_num)
    open('app_ids', 'a+').write(str(app_ids))
  else:
   print('Already have app_ids file')

def match_ids(r):
  app_ids = ast.literal_eval(open('./parts/' + str(r[0]) + '.' + str(r[1]) + '.part', 'r').read())
  file_path = './data/' + str(r[0]) + '.' + str(r[1])
  if os.path.isfile(file_path):
    start = len(open(file_path, 'a+').read().split('\n'))
  else:
    start = 0
  for i in range(start, 100000):
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
  lower = i * 100000
  upper = (i + 1) * 100000
  print('Starting ' + str(lower) + ',' + str(upper) + '...')
  match_ids([lower, upper])

if __name__ == '__main__':
  gather_data()
  
  jobs = []
  for i in range(0, 5):
    p = Process(target=match_range, args=(i,))
    jobs.append(p)
    p.start()
