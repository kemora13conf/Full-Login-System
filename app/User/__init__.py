from flask import Blueprint

users = Blueprint('users', __name__, url_prefix='/')

from . import routes