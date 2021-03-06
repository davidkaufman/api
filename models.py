from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import settings

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@localhost/{}'.format(
    settings.USER, settings.PASSWD, settings.DATABASE)

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Node(db.Model):
    __tablename__ = 'node'
    node_key = db.Column(db.String(34), primary_key=True)
    ip = db.Column(db.String(45))
    connection_config = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, node_key):
        self.node_key = node_key
        self.created_at = datetime.utcnow()

    def get_status(self):
        # TODO: implement status checking
        return 'active'


class Session(db.Model):
    __tablename__ = 'session'

    session_key = db.Column(db.String(34), primary_key=True)
    node_key = db.Column(db.String(34))
    created_at = db.Column(db.DateTime)
    node_updated_at = db.Column(db.DateTime)
    client_updated_at = db.Column(db.DateTime)
    node_bytes_sent = db.Column(db.BigInteger)
    node_bytes_received = db.Column(db.BigInteger)
    client_bytes_sent = db.Column(db.BigInteger)
    client_bytes_received = db.Column(db.BigInteger)
    client_ip = db.Column(db.String(45))
    established = db.Column(db.Boolean)

    def __init__(self, session_key):
        self.session_key = session_key
        self.created_at = datetime.utcnow()
        self.established = False
        self.node_bytes_sent = 0
        self.node_bytes_received = 0
        self.client_bytes_sent = 0
        self.client_bytes_received = 0


class NodeAvailability(db.Model):
    __tablename__ = 'node_availability'
    #id = db.Column(db.String(34), primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    node_key = db.Column(db.String(34))
    date = db.Column(db.DateTime)

    def __init__(self, node_key):
        self.node_key = node_key
        self.date = datetime.utcnow()
        #self.id = self.node_key + self.date.strftime('%Y%m%d%H%M%S')


class RegisteredParticipant(db.Model):
    __tablename__ = 'registered_participant'
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #node_ip = db.Column(db.String(45), primary_key=True)
    node_key = db.Column(db.String(34), primary_key=True)
    node_ip = db.Column(db.String(45), unique=True)
    eth_address = db.Column(db.String(45))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)

    def __init__(self, node_key, node_ip, eth_address, email=None):
        self.node_key = node_key
        self.node_ip = node_ip
        self.eth_address = eth_address
        self.email = email
        self.created_at = datetime.utcnow()
