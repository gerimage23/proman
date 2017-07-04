from flask import Flask, render_template, request, redirect, url_for, session, escape, jsonify
import requests
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datahandler import execute_sql_statement

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'ad76ad987ad98aud98adu9qeqeqadqew'


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


@app.route("/board", methods=['GET'])
def board():
    stat = execute_sql_statement("SELECT id, title, state, user_id FROM boards")
    vote_json = []
    main_tupl = {'boards': []}
    for i in range(len(stat)):
        temp_tupl = {}
        temp_tupl['id'] = stat[i][0]
        temp_tupl['title'] = stat[i][1]
        temp_tupl['state'] = stat[i][2]
        temp_tupl['user_id'] = stat[i][3]
        temp_tupl['cards'] = []
        cards = execute_sql_statement("SELECT id, title, status, card_order FROM cards WHERE board_id=" + str(stat[i][0]))
        print(cards)
        for j in range(len(cards)):
            temp_cards_tupl = {}
            temp_cards_tupl['id'] = cards[j][0]
            temp_cards_tupl['title'] = cards[j][1]
            temp_cards_tupl['status'] = cards[j][2]
            temp_cards_tupl['card_order'] = cards[j][3]
            temp_tupl['cards'].append(temp_cards_tupl)
    main_tupl['boards'].append(temp_tupl)
    #vote_json.append(temp_tupl)
    return jsonify(main_tupl)


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
