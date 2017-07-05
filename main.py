from flask import Flask, render_template, request, redirect, url_for, session, escape, jsonify
import requests
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datahandler import execute_sql_statement

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'ad76ad987ad98aud98adu9qeqeqadqew'


@app.route("/register")
def render_form_page():
    return render_template('form.html', act="Register")


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
    return redirect(url_for('hello'))


@app.route("/login-user", methods=["POST"])
def user_login():
    username = request.form['username']
    password = request.form['password']
    if datahandler.check_user(username, password):
        session['username'] = username
        return render_template('index.html', username=username)
    return render_template('form.html', act="Login",
                           errormsg="Invalid Username/Password combination provided.")


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/users", methods=['GET'])
def users():
    stat = execute_sql_statement("SELECT id, username, password, lastlog_time FROM users order by id")
    vote_json = []
    main_tupl = {'users': []}
    for i in range(len(stat)):
        temp_tupl = {}
        temp_tupl['id'] = stat[i][0]
        temp_tupl['username'] = stat[i][1]
        temp_tupl['password'] = stat[i][2]
        temp_tupl['lastlog_time'] = stat[i][3]
        main_tupl['users'].append(temp_tupl)
    #vote_json.append(temp_tupl)
    return jsonify(main_tupl)


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
