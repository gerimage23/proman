import psycopg2
from werkzeug import security
import os
import urllib

CONNECTION_STRING = "dbname=url.path[1:] user=url.username host=url.hostname password=url.password"


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
