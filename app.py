from flask import Flask, g, render_template, request, redirect, session, Response, jsonify
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
    notes = db.relationship('Note', backref='user', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    note_markup = db.Column(db.String)
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

@app.route('/note', methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        note_markup = request.form['editordata']
        title = request.form['title']
        note_id = request.form['noteid']

        if note_id:
            note = Note.query.filter(Note.id == note_id).first()
            note.title = title
            note.note_markup = note_markup
            note.date_created = datetime.datetime.utcnow()
            db.session.commit()
        else:
            note = Note(user_id=session['user']['id'], note_markup=note_markup, title=title)
            db.session.add(note)
            db.session.commit()

        return redirect('/')
    else:
        notes = Note.query.filter(Note.user_id == session['user']['id']).order_by(Note.date_created.desc()).all()
        return jsonify(utils.list_objects_as_dict(notes))

@app.route('/get_note', methods=['GET'])
def get_note():
    note_id = request.args['id']
    note = Note.query.filter(Note.id == note_id, Note.user_id == session['user']['id']).first()
    return jsonify(utils.object_as_dict(note))

@app.route('/delete_note', methods=['GET'])
def delete_note():
    note_id = request.args['id']
    Note.query.filter(Note.id == note_id, Note.user_id == session['user']['id']).delete()
    db.session.commit()
    return Response(status=204)

#----------HELPERS----------
def get_user(session):
    user_id = session['user']['id']
    user = User.query.filter(User.id == user_id)
    return user
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
