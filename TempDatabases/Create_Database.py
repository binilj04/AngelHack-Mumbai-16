#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","codio","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS RefTable")

# Create table as per requirement
sql = """CREATE TABLE RefTable (
         user  VARCHAR(20) NOT NULL,
         file  VARCHAR(50),
         ref VARCHAR(50) )"""

cursor.execute(sql)

# disconnect from server
db.close()