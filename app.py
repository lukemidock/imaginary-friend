from flask import Flask, g, render_template, request, redirect, session
from config import Config
from passlib.hash import pbkdf2_sha256
from flask_sqlalchemy import SQLAlchemy
import datetime
from uuid import uuid4
import utils

#check to make sure unix on deployment env
app = Flask(__name__, static_folder='public', static_url_path='')
app.config.from_object(Config.DEFAULT_MODE)

db = SQLAlchemy(app)

#----------MODELS----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    encrypted_password = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


#----------ROUTES----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        if username and typed_password:
            user = User.query.filter(User.username == username).first()
            if user:
                if pbkdf2_sha256.verify(typed_password, user.encrypted_password):
                    session['user'] = utils.object_as_dict(user)
                    return redirect('/')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"

    return render_template('login.html', message=message)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        typed_password = request.form['password']
        if name and username and typed_password:
            encrypted_password = pbkdf2_sha256.encrypt(typed_password, rounds=200000, salt_size=16)
            user = User(name=name, username=username, encrypted_password=encrypted_password)
            db.session.add(user)
            db.session.commit()

            return redirect('/login')
    
    return render_template('create_account.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)