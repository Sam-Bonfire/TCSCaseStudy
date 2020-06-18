from datetime import datetime

from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import and_
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for

from forms import (AccountSearchForm, LoginForm, AccountForm, WithdrawMoneyForm, DepositMoneyForm, TransferMoneyForm,
                    GetAccountStatementForm,CreateCustomerForm)
from models import User, Customer, Account, Transaction ,Cities
from app import db
from random import randint
import os
import json

app = Blueprint('app', __name__)


@app.route("/")
@app.route("/home")
def index():
    if current_user.is_authenticated:
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
    if current_user.is_authenticated:
        flash('User already logged in', 'success')
        return redirect(url_for('app.index'))
    else:
        if request.method == 'GET':
            login_form = LoginForm()
            return render_template('employee_login.html', form=login_form)
        if request.method == 'POST':
            form = LoginForm(request.form)
            user_login = form.username.data
            password = form.password.data
            remember = True if form.remember.data else False

            user = User.query.filter_by(user_login=user_login).first()

            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('app.login'))

            user.timestamp = datetime.now()
            db.session.commit()
            login_user(user, remember=remember)
            flash('User logged in', 'success')
            return redirect(url_for('app.index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))


@app.route('/search_customer', methods=['GET', 'POST'])
@login_required
def search_customer():
    if request.method == 'GET':
        account_search = AccountSearchForm()
        return render_template('account_search.html', user=current_user.type, form=account_search)
    elif request.method == 'POST':
        account_search = AccountSearchForm(request.form)
        account = None
        if account_search.customer_id.data:
            account = Account.query.filter_by(ws_cust_id=int(account_search.customer_id.data)).first()
        elif account_search.account_id.data:
            account = Account.query.filter_by(act_id=int(account_search.account_id.data)).first()
        else:
            flash('Invalid customer')
        if account:
            selected_account = AccountForm()
            selected_account.customer_id.data = account.ws_cust_id
            selected_account.account_id.data = account.act_id
            selected_account.account_type.data = 'Savings' if account.ws_acct_type == 'S' else 'Current'
            selected_account.balance.data = account.ws_acct_balance
            return render_template('search_customer.html', form=selected_account)
        else:
            flash('Account does not exist', 'danger')
        flash('Please enter a value', 'warning')
        return redirect(url_for('app.search_customer'))


# @app.route('/cashier_withdraw', methods=['GET', 'POST'])
# @login_required
# def cashier_withdraw():
#     if request.method == 'GET':
#         return redirect(url_for('app.search_customer'))
#     else:
#         selected_account = WithdrawMoneyForm(request.form)
#         account = Account.query.filter_by(act_id=selected_account.account_id.data).first()
#         if withdraw_amount := selected_account.withdraw_amount.data:
#             if int(withdraw_amount) <= account.ws_acct_balance:
#                 account.ws_acct_balance -= int(withdraw_amount)
#                 transaction = Transaction(ws_cust_id=account.ws_cust_id,
#                                           ws_acct_type=account.ws_acct_type,
#                                           ws_amt=withdraw_amount,
#                                           ws_trxn_date=datetime.now(),
#                                           ws_src_typ=account.ws_acct_type,
#                                           ws_tgt_typ=account.ws_acct_type,
#                                           ws_trxn_type='W')
#                 db.session.add(transaction)
#                 db.session.commit()
#                 selected_account.balance.data = account.ws_acct_balance
#                 selected_account.withdraw_amount.data = ''
#                 flash('Amount Withdrawn', 'success')
#                 return render_template('withdraw_money.html', form=selected_account, user=current_user.type)
#             else:
#                 flash('Balance Insufficient', 'danger')
#                 return render_template('withdraw_money.html', form=selected_account, user=current_user.type)
#         else:
#             return render_template('withdraw_money.html', form=selected_account, user=current_user.type)
#

# @app.route('/cashier_deposit', methods=['GET', 'POST'])
# @login_required
# def cashier_deposit():
#     if request.method == 'GET':
#         return redirect(url_for('app.search_customer'))
#     else:
#         selected_account = DepositMoneyForm(request.form)
#         account = Account.query.filter_by(act_id=selected_account.account_id.data).first()
#         if deposit_amount := selected_account.deposit_amount.data:
#             account.ws_acct_balance += int(deposit_amount)
#             transaction = Transaction(ws_cust_id=account.ws_cust_id,
#                                       ws_acct_type=account.ws_acct_type,
#                                       ws_amt=deposit_amount,
#                                       ws_trxn_date=datetime.now(),
#                                       ws_src_typ=account.ws_acct_type,
#                                       ws_tgt_typ=account.ws_acct_type,
#                                       ws_trxn_type='D')
#             db.session.add(transaction)
#             db.session.commit()
#             selected_account.balance.data = account.ws_acct_balance
#             selected_account.deposit_amount.data = ''
#             flash('Amount Deposited', 'success')
#             return render_template('deposit_money.html', form=selected_account, user=current_user.type)
#
#         return render_template('deposit_money.html', form=selected_account, user=current_user.type)

#
# @app.route('/cashier_transfer', methods=['GET', 'POST'])
# @login_required
# def cashier_transfer():
#     if request.method == 'GET':
#         return redirect(url_for('app.search_customer'))
#     else:
#         transaction_details = TransferMoneyForm(request.form)
#         source_account = Account.query.filter_by(act_id=transaction_details.source_account_id.data).first()
#         target_account = Account.query.filter_by(act_id=transaction_details.target_account_id.data).first()
#         if withdraw_amount := transaction_details.transfer_Amount.data:
#             if target_account:
#                 if source_account.ws_acct_type == (
#                         'S' if transaction_details.source_account_type.data == 'Savings Account' else 'C'):
#                     if target_account.ws_acct_type == (
#                             'S' if transaction_details.target_account_type.data == 'Savings Account' else 'C'):
#                         if int(withdraw_amount) <= source_account.ws_acct_balance:
#                             source_account.ws_acct_balance -= int(withdraw_amount)
#                             target_account.ws_acct_balance += int(withdraw_amount)
#                             transaction = Transaction(ws_cust_id=source_account.ws_cust_id,
#                                                       ws_acct_type=source_account.ws_acct_type,
#                                                       ws_amt=withdraw_amount,
#                                                       ws_trxn_date=datetime.now(),
#                                                       ws_src_typ=source_account.ws_acct_type,
#                                                       ws_tgt_typ=target_account.ws_acct_type,
#                                                       ws_trxn_type='T')
#                             db.session.add(transaction)
#                             db.session.commit()
#                             flash('Amount Withdrawn and Deposited Successfully', 'success')
#                         else:
#                             flash('Balance Insufficient', 'danger')
#                     else:
#                         flash('Please check the target account type', 'error')
#                 else:
#                     flash('Please check the source account type', 'error')
#             else:
#                 flash('Please check the target account details', 'error')
#         return render_template('transfer_money.html', form=transaction_details, user=current_user.type)


@app.route("/create_user")
def create_user():
    states = [ data.state for data in Cities.query(Cities.state).distinct()]
    form=CreateCustomerForm()
    form.states.choices=states
    return render_template("create_user.html",form=form,states=states)


def randome_customer_id():
    return randint(100000000, 999999999)


@app.route("/create_user_validate", methods=['GET', 'POST'])
def create_user_validate():
    try:
        if request.method == 'POST':
            id = request.form.get('id')
            name = request.form.get('name')
            age = request.form.get('age')
            address = request.form.get('address')
            state = request.form.get('state')
            city = request.form.get('city')
            address = address + " " + " " + state + " " + " " + city
            customer_id = Customer.query.order_by(Customer.ws_cust_id).all()
            customer_id = [i.ws_cust_id for i in customer_id[:]]

            while True:
                temp_cust_id = randome_customer_id()
                if randome_customer_id() not in customer_id:
                    break
            print(customer_id)
            customer = Customer(ws_ssn=int(id), ws_cust_id=temp_cust_id, ws_name=name, ws_adrs=address, ws_age=int(age))
            db.session.query()
            db.session.add(customer)
            db.session.commit()
            # print(Customer.query.get(1))

            flash('Create User Successful')
    except Exception as e:
        print(e)
        flash('User Already Exists')
    return render_template("create_user.html")


@app.route("/delete_customer")
def delete_customer():
    return render_template('delete_customer.html')


@app.route("/delete_customer_validation", methods=['GET', 'POST'])
def delete_customer_validation():
    if request.method == 'POST':
        id = request.form.get('id')
        cid = request.form.get('cid')
        name = request.form.get('name')
        age = request.form.get('age')
        address = request.form.get('address')

        data = Customer.query.filter_by(ws_ssn=id).first()
        if data.ws_ssn == int(id):
            if data.ws_cust_id == int(cid):
                if data.ws_name == name:
                    if data.ws_age == int(age):
                        if data.ws_adrs == address:
                            Customer.query.filter_by(ws_ssn=id).delete()
                            db.session.commit()
                            flash("Customer Delete Sucessfully")
                        else:
                            flash("Address Is Incorrect")
                    else:
                        flash("Age Is Incorrect")
                else:
                    flash("Name Not Found")
            else:
                flash("Customer Id Not Found")
        else:
            flash("Id Not Found")

        return render_template('delete_customer_temp.html')


@app.route("/account_statement", methods=['GET', 'POST'])
def account_statement():
    if request.method == 'GET':
        form = GetAccountStatementForm()
        return render_template('account_statement.html', form=form)
    elif request.method == 'POST':
        form = GetAccountStatementForm(request.form)
        account = Account.query.filter_by(act_id=form.account_id.data).first()
        # transactions = Transaction.query.filter_by(ws_cust_id=account.ws_cust_id).all()
        transactions = Transaction.query.filter(and_(Transaction.ws_cust_id == account.ws_cust_id,
                                                     Transaction.ws_trxn_date.between(form.start_date.data,
                                                                                      form.end_date.data))).all()
        print(transactions)
        return render_template('account_statement.html', account_statement=transactions, form=form,
                               user=current_user.user_login)


@app.route('/city/<string:state>')
def getCity(state):
    city_options = [{'id':data.city,'city':data.city} for data in 
                    Cities.query.filter(Cities.state.is_(state)).all()]
    return jsonify({'cities':city_options})