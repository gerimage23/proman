import json
import psycopg2
from werkzeug import security
from datetime import datetime


def execute_sql_statement(sql_statement, values=tuple()):
    # setup connection string, not the most secure way
 
    with open('static/connection.json') as data_file:   
        data = json.load(data_file)

    dbname = data["connection"]["database"]
    user = data["connection"]["user"]
    host = data["connection"]["host"]
    password = data["connection"]["password"]
    connect_str = "dbname="+dbname+" user="+user+" host="+host+" password="+password
    conn = None
    try:
        conn = psycopg2.connect(connect_str)
    except psycopg2.DatabaseError as e:  # TODO don't use this, remember: "raise PythonicError("Errors should never go silently.")
        print(e)
        return [[e]]
    else:
        conn.autocommit = True
        cursor = conn.cursor()
        try:
            cursor.execute(sql_statement, values)
        except psycopg2.ProgrammingError as e:
            print(e)
            return [[e]]
        else:
            if sql_statement.split(' ')[0].lower() == 'select':
                rows = list(cursor.fetchall())
                return rows
    finally:
        if conn:
            # conn.commit() leaving it here for future testing to see how it works
            conn.close()


def insert_user(username, password):
    '''
    Inserts a username-password pair into the database after hashing the password.
    '''
    password = security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    lastlog_time = datetime.now().replace(microsecond=0)

    try:
        execute_sql_statement('''INSERT INTO users (username, password, lastlog_time)
                          VALUES (%s,%s, %s);''', (username, password, lastlog_time))
        return True
    except psycopg2.DatabaseError as e:
        print(e)
        return False


def check_user(username, password):
        try:
            results = execute_sql_statement("""SELECT username, password
                                               FROM users
                                               WHERE username=%s;""", (username,))

            if len(results) > 0:
                return security.check_password_hash(results[0][1], password)
            else:
                return False

        except Exception as e:
            print(e)
            return False
