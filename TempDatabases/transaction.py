#__author__ = 'mohan08p'
#To change this template use Tools | Templates.
#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","codio","TESTDB" )

sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()