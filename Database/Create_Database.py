#__author__ = 'mohan08p'
#To change this template use Tools | Templates.
#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","codio","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS MainTable")

# Create table as per requirement
sql = """CREATE TABLE MainTable (
         jobid  VARCHAR(20) NOT NULL,
         filepath  VARCHAR(50),
         touch INT,
         url VARCHAR(50),
         refid VARCHAR(50),
         jobstat INT,
         ref VARCHAR(50) )"""

cursor.execute(sql)

# disconnect from server
db.close()