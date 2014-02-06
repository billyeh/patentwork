#!/bin/python

import sqlalchemy as sa
import os.path
import ast
from schema import *

grant_engine = sa.create_engine('mysql://root:330Ablumhall@169.229.7.251:3306/usptofixed')
Session = sa.orm.sessionmaker(bind=grant_engine, _enable_transaction_accounting=False)
grant_session = Session()

app_engine = sa.create_engine('mysql://root:330Ablumhall@169.229.7.251:3306/application')
Session = sa.orm.sessionmaker(bind=app_engine, _enable_transaction_accounting=False)
app_session = Session()

def gather_data():
  if not os.path.isfile('application_ids'):
    application_ids = []
    for app_id, date in grant_session.query(Application.id, Application.date):
      if date:
        application_ids.append(str(date.year) + '/' + str(app_id))
    open('application_ids', 'a+').write(str(application_ids))
  else:
    print('Already have application_ids file')

def fix_data():
  if os.path.isfile('application_ids'):
    application_ids = ast.literal_eval(open('application_ids', 'r').read())
    for app_id in filter(lambda x: x.split('/')[0] == '2002', application_ids):
      print(app_id)
      app = app_session.query(App_Application).filter(App_Application.id == app_id).first()
      if app:
        app.granted = 1
    app_session.commit()

if __name__ == '__main__':
  gather_data()
  fix_data()
