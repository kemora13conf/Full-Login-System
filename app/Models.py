from . import db, lg_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@lg_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)

class Users(db.Model, UserMixin):
    '''
    This object represent a the user table in the database
    '''
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    picture = db.Column(db.String(60), nullable=False, default='default.jpg')
    password = db.Column(db.String(50), nullable=False)

    '''
    here we create a one-to-many relationship
    between the users and the posts
    so one user can have many posts
    '''
    posts = db.relationship('Posts', backref='author', lazy=True)

    # The methods
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=1800)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)


class Posts(db.Model):
    '''
    This object represent a posts table in the database
    '''
    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.Text(1000), nullable=False, default='None')
    picture = db.Column(db.String(60), nullable=False, default='None')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
