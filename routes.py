from datetime import datetime

from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for

from models import User, Customer, Account
from app import db

app = Blueprint('app', __name__)


@app.route("/")
@app.route("/home")
def index():
    if current_user:
        return render_template("base.html", index=True, user=current_user.type)
    else:
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
        user_type = request.form.get('type')

        user = User.query.filter_by(user_login=user_login).first()

        if user:
            flash('Login already exists, please try a different one', 'warning')
            return redirect(url_for('app.signup'))

        new_user = User(user_login=user_login,
                        password=generate_password_hash(password, method='sha256'),
                        type=user_type)

        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully', 'success')

        return redirect(url_for('app.login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user:
        flash('User already logged in', 'success')
        return redirect(url_for('app.ind'))
    else:
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

            user.timestamp = datetime.now()
            db.session.commit()
            login_user(user, remember=remember)
            flash('User logged in', 'success')
            return redirect(url_for('app.ind'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))


@app.route('/search_customer', methods=['GET', 'POST'])
@login_required
def search_customer():
    if request.method == 'GET':
        return render_template('search_customer.html', user=current_user.type)
    elif request.method == 'POST':
        account_id = request.form.get('account_id')
        customer_id = request.form.get('customer_id')
        account = None
        if customer_id:
            account = Account.query.filter_by(ws_cust_id=int(customer_id)).first()
        elif account_id:
            account = Account.query.filter_by(act_id=int(account_id)).first()
        else:
            flash('Invalid customer')
        if account:
            return render_template('search_customer.html', account=account)
        else:
            flash('Account does not exist', 'error')
        flash('Please enter a value', 'warning')
        return redirect(url_for('app.search_customer'))


@app.route('/cashier_withdraw', methods=['GET', 'POST'])
@login_required
def cashier_withdraw():
    if request.method == 'GET':
        return redirect(url_for('app.search_customer'))
    else:
        account_id = request.form.get('account_id')
        account = Account.query.filter_by(act_id=account_id).first()
        withdraw_amount = request.form.get('withdraw_amount')
        if withdraw_amount:
            if int(withdraw_amount) <= account.ws_acct_balance:
                account.ws_acct_balance -= int(withdraw_amount)
                db.session.commit()
                flash('Amount Withdrawn', 'success')
                return render_template('cashier_withdraw.html', account=account, user=current_user.type)
            else:
                flash('Balance Insufficient', 'error')
                return render_template('cashier_withdraw.html', account=account, user=current_user.type)
        else:
            return render_template('cashier_withdraw.html', account=account, user=current_user.type)
