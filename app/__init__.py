from flask import Flask
from flask_login import LoginManager, login_manager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from os import path
from .Config import config




# variable
DB_NAME = 'database.db'
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
lg_manager = LoginManager()
lg_manager.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialise the extentions
    db.init_app(app)
    lg_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    # Register the blueprints.
    from .User import users
    from .Main import main
    from .Post import posts

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)

    create_db(app)
    return app

def create_db(app):
    # db.drop_all(app=app)
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Database creates successfuly')

