import imp
import shelve
from mics import Session
import xlrd
from databases import ChannelPopular

book = xlrd.open_workbook("data.xls")
sh = book.sheet_by_index(0)

session = Session()
for rx in range(sh.nrows):
    print(sh.row(rx)[0].value)
    # [5:-1]
    new_channel = ChannelPopular(name=sh.row(rx)[0].value)
    session.add(new_channel)
    session.commit()
session.close()
"""
with shelve.open('Products','c') as Products:
    Products['Анимашки'] = {}
#    Products['Смайлики'] = {'test': Product(20,1),'test2':Product(20,1)}

with shelve.open('Admins','c') as Admins:
    Admins['categs_price'] = {}

with shelve.open('Users','c') as Users:
    user = Users['1274864704']
    user.balance += 50000 
    user.role.name = 'admin'
    user.role.get_admin = True
    Users['1274864704'] = user
"""
