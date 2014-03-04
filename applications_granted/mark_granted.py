#!/usr/bin/env python

import sqlalchemy as sa
import os.path
import sys
import gc
import logging
from schema import *
from ast import literal_eval
from multiprocessing import Process

grant_engine = sa.create_engine('mysql://root:330Ablumhall@169.229.7.251:3306/usptofixed')
Session = sa.orm.sessionmaker(bind=grant_engine, _enable_transaction_accounting=False)
grant_session = Session()

app_engine = sa.create_engine('mysql://root:330Ablumhall@169.229.7.251:3306/apptest')
Session = sa.orm.sessionmaker(bind=app_engine, _enable_transaction_accounting=False)
app_session = Session()

logging.basicConfig(filename='mark_granted.log',level=logging.DEBUG)

def gather_grant_data():
  if (os.path.isfile('grant_apps')):
    return
  application_ids = []
  for (app_id,) in grant_session.query(Application.id):
    print(app_id)
    if app_id:
      application_ids.append(app_id)
  open('grant_apps', 'a+').write(str(application_ids))

def gather_app_data():
  if (os.path.isfile('app_apps')):
    return
  application_ids = []
  for (app_id,) in app_session.query(App_Application.number):
    print(app_id)
    if app_id:
      application_ids.append(app_id)
  open('app_apps', 'a+').write(str(application_ids))

def mark_granted(app_apps, process_num, freq):
  fname = 'progress' + str(process_num)
  if not os.path.isfile(fname):
    f = open(fname, 'w')
    f.write('0')
    f.close()
  with open(fname) as f:
    index = int(f.read())

  for i in range(len(app_apps) - index):
    progress = i + index
    app_id = app_apps[progress]
    app = app_session.query(App_Application).filter(App_Application.number == app_id).one()
    if not app:
      logging.info('Nothing found for ' + app_id)
      continue
    print(str(process_num) + '.' + str(progress) + ': ' + app_id)
    app.granted = 1
    if progress % freq == 0:
      app_session.commit()
      with open(fname, 'w') as f:
        f.write(str(progress))
  app_session.commit()
  return

def partition_data(num_processes):
  print('Creating partitions of app numbers...')
  grant_apps = set(literal_eval(open('grant_apps', 'r').read()))
  app_apps = literal_eval(open('app_apps').read())
  job_size = len(app_apps) / num_processes
  for i in range(num_processes):
    print('Part ' + str(i) + ' being created.')
    start = i * job_size
    end = (i + 1) * job_size
    partition = filter(lambda x: x in grant_apps, app_apps[start:end])
    open('part' + str(i), 'w').write(str(partition))
  print('Part ' + str(num_processes) + ' being created.')
  open('part' + str(num_processes), 'w').write(str(app_apps[num_processes * job_size:]))

if __name__ == '__main__':
  if (len(sys.argv) < 2):
    num_processes = 4
  else:
    try:
      num_processes = int(sys.argv[1])
    except:
      print('First argument should be integer number of processes')
  if len(sys.argv) < 3:
    freq = 10
  else:
    try:
      freq = int(sys.argv[2])
    except:
      print('Second argument should be integer commit frequency')

  gather_grant_data()
  gather_app_data()
  partition_data(num_processes)
  gc.collect()
  for i in range(num_processes + 1):
    part = literal_eval(open('part' + str(i)).read())
    p = Process(target=mark_granted, args=(part, i, freq))
    print('Starting process ' + str(i))
    p.start()

