# import sqlalchemy
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base  # we need this to import base class
# engine = create_engine('mysql+mysqlconnector://root:Welcome_123@localhost:3306/sakila')
# # dump of all sql thats executed
from distutils.sysconfig import get_python_lib
import mysql.connector
cnx = mysql.connector.connect(user='root', password='Welcome_123',
                              host='127.0.0.1',
                              database='sakila')
cursor = cnx.cursor()
# connection = engine.connect()
# metadata = sqlalchemy.MetaData()
# actor = sqlalchemy.Table('actor', metadata, autoload=True, autoload_with=engine)

# # Write a script that stores the data returned from the Twitter API in a SQL database.
# # Then read that data from your database and use the code you wrote previously to analyze it.
# # And finally, also write the results to the database.
# # create schema twitter;


# Base = declarative_base()
#
# class Twitter(Base):
#     __tablename__ = "twitter"
#
#     id = Column('id', Integer, primary_key=True)
#     tweet = Column('Tweet', String)
#
#

sql_select_Query = "select * from actor"
cursor.execute(sql_select_Query)

for one in cursor:
  print(one)

cursor.close()
cnx.close()
