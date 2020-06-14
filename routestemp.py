
from flask import Flask, render_template, request, redirect, url_for, send_file, flash


from forms import (LoginForm,CreateCustomerForm,UpdateCustomerForm,DeleteCustomerForm,
					CreateAccountForm,DeleteAccountForm,CustomerSearchForm,AccountSearchForm,DepositeMoneyForm,
					WithdrawMoneyForm,TrasferMoneyForm,GetAccountStatementForm)
