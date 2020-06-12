from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for

from models import User
from app import db

app = Blueprint('app', __name__)


@app.route("/")
@app.route("/home")
def index():
    return render_template("base.html", index=True)


@app.route("/index")
@login_required
def ind():
    return current_user.user_login


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        user_login = request.form.get('login')
        password = request.form.get('password')

        user = User.query.filter_by(user_login=user_login).first()

        if user:
            return redirect(url_for('app.signup'))

        new_user = User(user_login=user_login, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('app.login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user_login = request.form.get('login')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(user_login=user_login).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('app.login'))

        login_user(user, remember=remember)
        return redirect(url_for('app.index'))
