#!/usr/bin/env python

import sqlalchemy as sa
import os.path
import ast
from schema import *

grant_engine = sa.create_engine('mysql://root:330Ablumhall@169.229.7.251:3306/usptofixed')
Session = sa.orm.sessionmaker(bind=grant_engine, _enable_transaction_accounting=False)
grant_session = Session()

app_engine = sa.create_engine('mysql://root:330Ablumhall@169.229.7.251:3306/apptest')
Session = sa.orm.sessionmaker(bind=app_engine, _enable_transaction_accounting=False)
app_session = Session()

def gather_grant_data():
  application_ids = []
  for (app_id,) in grant_session.query(Application.id):
    if app_id:
      a = str(app_id).replace('/', '')
      application_ids.append(a)
  open('grant_apps', 'a+').write(str(application_ids))

def gather_app_data():
  application_ids = []
  for (app_id,) in app_session.query(App_Application.id):
    if app_id:
      a = str(app_id).split('/')[1]
      application_ids.append(a)
  open('app_apps', 'a+').write(str(application_ids))

if __name__ == '__main__':
  if not os.path.isfile('grant_apps'):
    gather_grant_data()
  if not os.path.isfile('app_apps'):
    gather_app_data()

