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

def gather_data():
  if not os.path.isfile('application_ids'):
    application_ids = []
    for app_id, date in grant_session.query(Application.id, Application.date):
      if date:
        a = str(date.year) + '/' + str(app_id).replace('/', '')
        application_ids.append(a)
        print(a)
    open('application_ids', 'a+').write(str(application_ids))
  else:
    print('Already have application_ids file')

def fix_data():
  if os.path.isfile('application_ids'):
    app_ids = []
    granted_apps = set(ast.literal_eval(open('application_ids', 'r').read()))
    for (app_id,) in app_session.query(App_Application.id):
      if app_id in granted_apps:
        app_ids.append(app_id)
    open('app_application_ids', 'a+').write(str(app_ids))

if __name__ == '__main__':
  gather_data()
  fix_data()

