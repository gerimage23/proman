from flask import Flask, render_template, request, redirect, url_for, session, escape, jsonify
import requests
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
import datahandler

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'ad76ad987ad98aud98adu9qeqeqadqew'


@app.route('/create_card', methods=["POST"])
def create_card():
    boardId = request.form["boardId"]
    cardTitle = request.form["cardTitle"]
    datahandler.execute_sql_statement('''INSERT INTO cards(title, status, card_order, board_id)
                                      VALUES (%s,'new', 99, %s);''',
                                      (cardTitle, boardId))
    return "yeaa mothafucka"


@app.route("/register")
def render_form_page():
    return render_template('form.html', act="Register")


@app.route('/create_board', methods=["POST"])
def create_board():
    boardTitle = request.form["boardTitle"]
    username = "troll"
    userid = datahandler.execute_sql_statement('''SELECT id FROM users WHERE username=%s;''', (username,))[0][0]
    
    datahandler.execute_sql_statement('''INSERT INTO boards(title,state,user_id) VALUES (%s,'NEW',%s);''', (boardTitle, userid))
    return "yeaa mothafucka"


@app.route("/register-user", methods=["POST"])
def register_user():
    username = request.form["username"]
    password = request.form["password"]
    if datahandler.insert_user(username, password):
        session['username'] = username
        return render_template('index.html', username=username)
    else:
        return render_template('form.html', act="Register", errormsg="Username already exists!")


@app.route("/login")
def login_page():
    return render_template('form.html', act="Login")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('root'))


@app.route("/login-user", methods=["POST"])
def user_login():
    username = request.form['username']
    password = request.form['password']
    if datahandler.check_user(username, password):
        session['username'] = username
        return render_template('index.html', username=username)
    return render_template('form.html', act="Login",
                           errormsg="Invalid Username/Password combination provided.")


@app.route("/save_boards", methods=['POST'])
def save_boards():
    boards = request.get_json()
    
    # board: title, state, userid
    for board in boards:
        _id = board['id']
        _title = board['title']
        _state = board['state']
        _userid = board['user_id']
        _cards = board['cards']

        # card: title, status, order, board_id
        for card in _cards:
            _cardid = card['id']
            _cardtitle = card['title']
            _status = card['status']
            _order = card['order']
            _boardid = card['board_id']

            datahandler.execute_sql_statement('''
                                              UPDATE cards SET title=%s, status=%s, card_order=%s, board_id=%s
                                              WHERE id = %s;''',
                                              (_cardtitle, _status, _order, _boardid, _cardid))
        
        datahandler.execute_sql_statement('''
                                          UPDATE boards SET title=%s, state=%s, user_id=%s
                                          WHERE id = %s;''', (_title, _state, _userid, _id))

    response = {'message': 'succes'}
    return jsonify(response)


@app.route("/load_boards", methods=['GET'])
def load_boards():
    stat = datahandler.execute_sql_statement("SELECT id, title, state, user_id FROM boards")
    vote_json = []
    main_tupl = {'boards': []}
    for i in range(len(stat)):
        temp_tupl = {}
        temp_tupl['id'] = stat[i][0]
        temp_tupl['title'] = stat[i][1]
        temp_tupl['state'] = stat[i][2]
        temp_tupl['user_id'] = stat[i][3]
        temp_tupl['cards'] = []
        cards = datahandler.execute_sql_statement("SELECT id, title, status, card_order, board_id FROM cards WHERE board_id=" + str(stat[i][0]))
        for j in range(len(cards)):
            temp_cards_tupl = {}
            temp_cards_tupl['id'] = cards[j][0]
            temp_cards_tupl['title'] = cards[j][1]
            temp_cards_tupl['status'] = cards[j][2]
            temp_cards_tupl['order'] = cards[j][3]
            temp_cards_tupl['board_id'] = cards[j][4]
            temp_tupl['cards'].append(temp_cards_tupl)
        main_tupl['boards'].append(temp_tupl)
    # vote_json.append(temp_tupl)
    return jsonify(main_tupl)


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/users", methods=['GET'])
def users():
    stat = datahandler.execute_sql_statement("SELECT id, username, password, lastlog_time FROM users order by id")
    vote_json = []
    main_tupl = {'users': []}
    for i in range(len(stat)):
        temp_tupl = {}
        temp_tupl['id'] = stat[i][0]
        temp_tupl['username'] = stat[i][1]
        temp_tupl['password'] = stat[i][2]
        temp_tupl['lastlog_time'] = stat[i][3]
        main_tupl['users'].append(temp_tupl)
    # vote_json.append(temp_tupl)
    return jsonify(main_tupl)


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()