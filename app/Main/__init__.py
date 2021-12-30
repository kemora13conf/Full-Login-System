from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='/')

from . import routes