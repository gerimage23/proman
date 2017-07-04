import psycopg2
from werkzeug import security
import os
import urllib

CONNECTION_STRING = "dbname=proman_testdb user=aakeeka host=localhost password=postgresql"


def init_db_connection(connection_string=CONNECTION_STRING):

    try:

        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))

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

    cursor = init_db_connection()
    try:
        cursor.execute('''INSERT INTO users (username, password) VALUES (%s,%s) ;''', (username, password))
        return True
    except psycopg2.DatabaseError as e:
        print(e)
        return False
