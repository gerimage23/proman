from flask import Flask, render_template, request, redirect, url_for, session, escape, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datahandler import *


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'ad76ad987ad98aud98adu9qeqeqadqew'


# Root
@app.route("/")
def root():
    '''
    Simply just serving the main page for the user.
    '''
    if 'username' in session:
        username = session['username']
        return render_template('index.html',
                               username=username)
    return render_template('index.html')


# Registration
@app.route("/register")
def render_form_page():
    '''
    Renders the registration page for the user.
    '''
    return render_template('form.html',
                           act="Register")


@app.route("/register-user", methods=["POST"])
def register_user():
    '''
    Endpoint handling the registration process.
    '''
    username = request.form["username"]
    password = request.form["password"]
    check_password = request.form["password-confirm"]
    if password != check_password:
        return render_template('form.html',
                               act="Register",
                               errormsg="Passwords don't match!")
    if insert_user(username, password):
        session['username'] = username
        return render_template('index.html', username=username)
    return render_template('form.html',
                           act="Register",
                           errormsg="Username already exists!")


# Login
@app.route("/login")
def login_page():
    '''
    Renders a page for user login.
    '''
    return render_template('form.html', act="Login")


@app.route("/login-user", methods=["POST"])
def user_login():
    '''
    Endpoint handling the login process for the user.
    '''
    username = request.form['username']
    password = request.form['password']
    if check_user(username, password):
        if 'username' in session and session['username'] == username:
            return render_template('form.html',
                                   act='Login',
                                   errormsg="That user is already signed in!")
        session['username'] = username
        return redirect(url_for('root'))
    return render_template('form.html',
                           act="Login",
                           errormsg="Invalid Username/Password combination provided.")


# Logout
@app.route('/logout')
def logout():
    '''
    When the corresponding button is hit redirects the user to root.
    '''
    session.pop('username', None)
    return redirect(url_for('root'))


# Create Card
@app.route('/create_card', methods=["POST"])
def create_card():
    '''
    Endpoint creating a new card in the cards table
    partly based on information it gets from the user.
    '''
    board_id = request.form["boardId"]
    card_title = request.form["cardTitle"]
    add_new_card_to_db(card_title, board_id)
    response = {'message': 'succes'}
    return jsonify(response)


# Create Board
@app.route('/create_board', methods=["POST"])
def create_board():
    '''
    Endpoint creating a new board in the boards table
    partly based information it gets from the user.
    '''
    boardTitle = request.form["boardTitle"]
    username = session["username"]
    user_id = execute_sql_statement('''SELECT id FROM users WHERE username=%s;''', (username,))[0][0]
    add_new_board_to_db(boardTitle, user_id)
    response = {'message': 'succes'}
    return jsonify(response)


# Save Boards
@app.route("/save_boards", methods=['POST'])
def save_boards():
    '''
    Endpoint saving changes in the boards to database during user sessions.
    '''
    boards = request.get_json()
    save_boards_to_db(boards)
    response = {'message': 'succes'}
    return jsonify(response)


# Load Boards
@app.route("/load_boards", methods=['GET'])
def load_boards():
    '''
    Endpoint handling the load of boards to the specific user.
    '''
    if 'username' in session:
        username = session['username']
        user_id = execute_sql_statement('''SELECT id FROM users WHERE username=%s;''', (username,))[0][0]
        stat = execute_sql_statement("SELECT id, title, state, user_id FROM boards WHERE user_id=%s", (user_id,))
        vote_json = []
        main_tupl = {'boards': []}
        for i in range(len(stat)):
            temp_tupl = {}
            temp_tupl['id'] = stat[i][0]
            temp_tupl['title'] = stat[i][1]
            temp_tupl['state'] = stat[i][2]
            temp_tupl['user_id'] = stat[i][3]
            temp_tupl['cards'] = []
            cards = execute_sql_statement("SELECT id, title, status, card_order, board_id FROM cards WHERE board_id=" + str(stat[i][0]))
            for j in range(len(cards)):
                temp_cards_tupl = {}
                temp_cards_tupl['id'] = cards[j][0]
                temp_cards_tupl['title'] = cards[j][1]
                temp_cards_tupl['status'] = cards[j][2]
                temp_cards_tupl['order'] = cards[j][3]
                temp_cards_tupl['board_id'] = cards[j][4]
                temp_tupl['cards'].append(temp_cards_tupl)
            main_tupl['boards'].append(temp_tupl)
        return jsonify(main_tupl)
    return redirect(url_for('root'))


# Users
@app.route("/users", methods=['GET'])
def users():
    '''
    Simple page showing all the users in the database.
    '''
    all_user_details = get_all_user_detail()
    return jsonify(all_users_detail)


def main():
    app.run(port=3000)

if __name__ == '__main__':
    main()
