import psycopg2
from werkzeug import security
import os
import urllib
from datetime import datetime

CONNECTION_STRING = "dbname=proman_testdb user=aakeeka host=localhost password=postgresql"
CONNECTION_URL = "postgres://sbcjqryaikuvtq:64ea9d49945ec0b2ba2838400f964055dc138b9334ad3117b258914dc11d6b7b@ec2-54-75-229-201.eu-west-1.compute.amazonaws.com:5432/d1vmbir57f49qf"


def init_db_connection(connection_string=CONNECTION_STRING):

    try:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(CONNECTION_URL)  # os.environ.get('DATABASE_URL') IF ON HEROKU

        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        connection.autocommit = True

        cursor = connection.cursor()

    except psycopg2.DatabaseError as e:
        print(e)
        return [[e]]

    return cursor


def insert_user(username, password):
    '''
    Inserts a username-password pair into the database after hashing the password.
    '''
    password = security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    lastlog_time = datetime.now().replace(microsecond=0)

    cursor = init_db_connection()
    try:
        cursor.execute('''INSERT INTO users (username, password, lastlog_time)
                          VALUES (%s,%s, %s);''', (username, password, lastlog_time))
        return True
    except psycopg2.DatabaseError as e:
        print(e)
        return False
