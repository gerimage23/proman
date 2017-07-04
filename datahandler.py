import json
import psycopg2


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


def main():
    pass

if __name__ == '__main__':
    main()