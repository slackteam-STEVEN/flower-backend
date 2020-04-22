# -*- coding: utf-8 -*-

import MySQLdb
from datetime import datetime
def conn_f():
    con = MySQLdb.connect(
        user    = 'root',       # 'your username',
        passwd  = 'Flower0112', # 'your password',
        host    = '10.0.1.10',  # 'localhost',
        port    = 3306,
        db      = 'flower',       # 
        charset = 'utf8'
    ) 
    return con
