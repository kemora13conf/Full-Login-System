from . import main
from flask_login import login_required
from flask import redirect, url_for, request

@main.route('/')
@main.route('/Home')
@login_required
def home():
    return f"""
    <h1> Welcome Home </h1>
    <a href='{ url_for('users.logout') }'> logout </a>
    """

@main.route('/Posts')
@login_required
def posts():
    return "<h1> Welcome p </h1>"