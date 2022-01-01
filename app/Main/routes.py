from . import main
from flask_login import login_required
from flask import render_template, redirect, url_for, request

@main.route('/')
@main.route('/Home')
@login_required
def home():
    return render_template("Main/MainBase.html", title="Home")

@main.route('/Posts')
@login_required
def posts():
    return "<h1> Welcome p </h1>"