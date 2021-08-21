from flask import Flask, g, render_template
from config import Config
from db import Database

#check to make sure unix on deployment env
app = Flask(__name__, static_folder='public', static_url_path='')
app.config.from_object(Config.DEFAULT_MODE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database(app.config["SQLALCHEMY_DATABASE_URI"])
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    """if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        if username and typed_password:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(typed_password, user['encrypted_password']):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"
    """
    return render_template('login.html', message=message)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)