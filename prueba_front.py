# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask, abort, request, jsonify, g, url_for, render_template
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from datetime import datetime

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supermegasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['EXPIRATION'] = 30

# extensions
manager = Manager(app)
db = SQLAlchemy(app)
http_auth = HTTPBasicAuth()


@manager.command
def db_reset():
    '''Resetear BD'''
    db.drop_all()
    db.create_all()


@manager.command
def create_data():
    '''Agregar datos a BD'''
    db_reset()
    create_users()
    create_tickets()


def create_users():
    # rut, rutdv, name, is_admin, password, is_enabled, username=None
    User.create('6', 'K', 'Administrador', True, 'admin.passwd', True)
    User.create('1', '9', 'Usuario 1', False, 'usuario1.passwd', True)
    User.create('2', '7', 'Usuario 2', False, 'usuario2.passwd', True)


def create_tickets():
    Ticket.create('ticket 01', 1, u'descripción ticket 01')
    Ticket.create('ticket 02', 2, u'descripción ticket 02')
    Ticket.create('ticket 03', 3, u'descripción ticket 03')
    Ticket.create('ticket 04', 1, u'descripción ticket 04')
    Ticket.create('ticket 05', 2, u'descripción ticket 05')
    Ticket.create('ticket 06', 3, u'descripción ticket 06')
    Ticket.create('ticket 07', 1, u'descripción ticket 07')
    Ticket.create('ticket 08', 2, u'descripción ticket 08')
    Ticket.create('ticket 09', 3, u'descripción ticket 09')
    Ticket.create('ticket 10', 1, u'descripción ticket 10')
    Ticket.create('ticket 11', 2, u'descripción ticket 11')
    Ticket.create('ticket 12', 3, u'descripción ticket 12')


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @classmethod
    def create(cls, name, user_id, description=u""):
        try:
            ticket = Ticket(
                name=name,
                user_id=user_id,
                description=description
            )
            db.session.add(ticket)
            db.session.commit()
        except Exception as e:
            logging.exception(e)

    def serialize(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(64), nullable=False)
    rutdv = db.Column(db.String(1), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean)
    is_enabled = db.Column(db.Boolean)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)

    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=app.config['EXPIRATION']):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @classmethod
    def create(cls, rut, rutdv, name, is_admin, password, is_enabled, username=None):
        try:
            if not username:
                username = "{0}-{1}".format(rut, rutdv).upper()
            user = User(
                username=username,
                is_admin=is_admin,
                name=name,
                rut=rut,
                rutdv=rutdv,
                is_enabled=is_enabled
            )
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            logging.exception(e)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    def serialize(self):
        return {
            'id': self.id,
            'rut': self.rut,
            'rutdv': self.rutdv,
            'username': self.username,
            'name': self.name,
            'is_admin': self.is_admin,
            'is_enabled': self.is_enabled,
            'member_since': self.member_since,
        }


@http_auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/')
def get_main():
    return render_template('index.html')


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/token')
@http_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(app.config['EXPIRATION'])
    return jsonify({'token': token.decode('ascii'), 'duration': app.config['EXPIRATION']})


@app.route('/api/current')
@http_auth.login_required
def get_resource():
    return jsonify({'data': g.user.serialize()})


@app.route('/api/tickets')
@http_auth.login_required
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify({'data': [t.serialize() for t in tickets]})


if __name__ == '__main__':
    manager.run()


