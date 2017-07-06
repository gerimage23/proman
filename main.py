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
    user_id = get_user_id_from_db(username)
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
        user_id = get_user_id_from_db(username)
        user_data_container = get_boards_from_db(user_id)
        return jsonify(user_data_container)
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
    app.run()

if __name__ == '__main__':
    main()
