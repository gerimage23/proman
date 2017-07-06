import json
import psycopg2
from werkzeug import security
from datetime import datetime


def execute_sql_statement(sql_statement, values=tuple()):
    '''
    Function handling quer requests to the database.
    '''
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
    except psycopg2.DatabaseError as e:
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
    '''
    Checks matching of the username and password got from the user.
    '''
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


def add_new_card_to_db(card_title, board_id):
    execute_sql_statement("""
                          INSERT INTO cards(title, status, card_order, board_id)
                          VALUES (%s,'new', 99, %s);
                          """,
                          (card_title, board_id))


def add_new_board_to_db(board_title, user_id):
    execute_sql_statement("""
                          INSERT INTO boards(title,state,user_id)
                          VALUES (%s,'NEW',%s);
                          """,
                          (board_title, user_id))


def get_user_id_from_db(username):
    user_id = execute_sql_statement("""
                                    SELECT id
                                    FROM users
                                    WHERE username=%s;
                                    """,
                                    (username,))[0][0]
    return user_id


def save_boards_to_db(boards):
    for board in boards:
        board_id = board['id']
        board_title = board['title']
        board_state = board['state']
        board_userid = board['user_id']
        board_cards = board['cards']

        for card in _cards:
            card_id = card['id']
            card_title = card['title']
            card_status = card['status']
            card_order = card['order']
            card_board_id = card['board_id']

            execute_sql_statement("""
                                  UPDATE cards
                                  SET title=%s, status=%s, card_order=%s, board_id=%s
                                  WHERE id = %s;
                                  """,
                                  (card_title, card_status, card_order, card_board_id, card_id))

        execute_sql_statement("""
                              UPDATE boards
                              SET title=%s, state=%s, user_id=%s
                              WHERE id = %s;
                              """,
                              (board_title, board_state, board_userid, board_id))


def get_boards_from_db(user_id):
    user_boards = execute_sql_statement("""
                                        SELECT id, title, state, user_id
                                        FROM boards
                                        WHERE user_id=%s
                                        """,
                                        (user_id,))
    user_data_container = {'boards': []}
    for i in range(len(user_boards)):
        user_board_details = {}
        user_board_details['id'] = user_boards[i][0]
        user_board_details['title'] = user_boards[i][1]
        user_board_details['state'] = user_boards[i][2]
        user_board_details['user_id'] = user_boards[i][3]
        user_board_details['cards'] = []
        user_cards = execute_sql_statement("""
                                           SELECT id, title, status, card_order, board_id
                                           FROM cards
                                           WHERE board_id=%s
                                           """,
                                           (str(user_boards[i][0]),))
        for j in range(len(user_cards)):
            user_card_details = {}
            user_card_details['id'] = user_cards[j][0]
            user_card_details['title'] = user_cards[j][1]
            user_card_details['status'] = user_cards[j][2]
            user_card_details['order'] = user_cards[j][3]
            user_card_details['board_id'] = user_cards[j][4]
            user_board_details['cards'].append(user_card_details)
        user_data_container['boards'].append(user_board_details)
    return user_data_container


def get_all_user_detail():
    all_user_details = execute_sql_statement("""
                                         SELECT id, username, password, lastlog_time
                                         FROM users order by id
                                         """)
    return prepare_all_users_detail(all_user_details)


def prepare_all_users_detail(all_user_details):
    users_detail = {'users': []}
    for i in range(len(user_details)):
        single_user_details_collector = {}
        single_user_details_collector['id'] = all_user_details[i][0]
        single_user_details_collector['username'] = all_user_details[i][1]
        single_user_details_collector['password'] = all_user_details[i][2]
        single_user_details_collector['lastlog_time'] = all_user_details[i][3]
        users_detail['users'].append(single_user_details_collector)
    return users_detail
