from flask import Flask, render_template, request, session, redirect, url_for
import datahandler


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/register")
def render_form_page():
    return render_template('form.html')


@app.route("/register-user", methods=["POST"])
def register_user():
    username = request.form["username"]
    password = request.form["password"]
    if datahandler.insert_user(username, password):
        session['username'] = username
        return redirect(url_for('hello'))
    else:
        return render_template('form.html', errormsg="Username already exists!")


@app.route("/")
def hello():
    return render_template('index.html')


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
