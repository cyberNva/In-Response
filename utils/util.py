import os
import time

import mysql.connector
import streamlit as st
from mysql.connector import Error

# @st.cache_resource 
def create_db_connection():
    connection = None
    try:
        # connection = mysql.connector.connect(
        #     host=host_name,
        #     user=user_name,
        #     passwd=user_password,
        #     database=db_name
        # )
        connection = mysql.connector.connect(**st.secrets["mysql"])
        return connection
        print("MySQL Database connection successful")
    except Error as err:
        os.system('service mysql start')
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = None
    try:
        cursor = connection.cursor()
    except Exception:
        os.system('service mysql start')
        time.sleep(2)
        cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = None
    try:
        cursor = connection.cursor()
        result = None
    except Exception:
        st.info("Starting MySQL Server....")
        os.system('service mysql start')
        time.sleep(5)
        cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def __Create_Tabels(connection):
    create_table = """
    CREATE TABLE users (
    id INT AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
    );
    """
    execute_query(connection,create_table)

def call_users():
    usernameQ = """ SELECT username FROM users """
    nameQ =  """ SELECT name FROM users """
    passQ = """ SELECT password FROM users """

    r1 = read_query(c,usernameQ)
    r2 = read_query(c,nameQ)
    r3 = read_query(c,passQ)
    usernames = []
    names = []
    passwords = []

    for row in r1:
        row  = ''.join(letter for letter in row if letter.isalnum())
        usernames.append(row)
        
    for row in r2:
        # row  = ''.join(letter for letter in row if letter.isalnum())
        names.append(row)
    for row in r3:
        row  = ''.join(letter for letter in row if letter.isalnum())
        passwords.append(row)

    return usernames,names,passwords

c = create_db_connection()
# __Create_Tabels(c)
q0 = """
"INSERT INTO users (username, password, name, email)
 VALUES (%s, %s, %s, %s)"
"""
q1 = """ SELECT * FROM users """
q2 = """ 
INSERT INTO users ( username, password, name , email) VALUES ('amal', SHA2('amal', 256),'amal ali', 'amal@gmail.com');
"""
delQ= """ DELETE FROM users WHERE id=8;"""

# execute_query(c,delQ)

# r = read_query(c,q1)

# for row in r:
#     print(row)


