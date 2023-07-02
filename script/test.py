from dotenv import load_dotenv
load_dotenv()
import os

import mysql.connector
from mysql.connector import errorcode

config={
    'host':os.environ["HOSTNAME"],
    'user':os.environ["USER"],
    'password':os.environ["PASSWORD"],
    'database':os.environ["DATABASE"]
}

try:
    cnx = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor = cnx.cursor()

cursor.execute("DROP TABLE IF EXISTS api_key")
cursor.execute("DROP TABLE IF EXISTS auth")
cursor.execute("CREATE TABLE IF NOT EXISTS auth(username VARCHAR(15) PRIMARY KEY, password TEXT, email VARCHAR(50), isNewUser TINYINT(1) DEFAULT 1)")
cursor.execute("CREATE TABLE IF NOT EXISTS api_key(username VARCHAR(15),apikey TEXT, FOREIGN KEY (username) REFERENCES auth(username))")

QUERY = ('INSERT INTO {coll_name} '
                 '(username, password, email) '
                 'VALUES '
                 '(%s, %s, %s)').format(coll_name="auth")

testlist=[("test3","test3","test2@test.com"),("test1","test1","test1@test1.com")]
cursor.executemany(QUERY, testlist)

QUERY = ('SELECT {cols} FROM {table_name} WHERE email="test2@test.com"').format(cols="*", table_name="auth")
cursor.execute(QUERY)
for i in cursor.fetchall():
    print(i)


cnx.commit()
# from jose import jwt
# print(jwt.encode("bruhh"))
