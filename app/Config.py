DB_NAME = 'database.db'
class config:
    SECRET_KEY = '27dc5748286b98b37a4afdf6dad69a4d'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'abdomouak48@gmail.com'
    MAIL_PASSWORD = 'Mygmailaccount!abdo@mouak#2003'
    MAIL_DEFAULT_SENDER = 'abdomouak48@gmail.com'
    MAIL_DEBUG = True