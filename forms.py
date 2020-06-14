from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,IntegerField,SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError







class CreateCustomerForm(FlaskForm):
    customer_ssn_id = StringField('Customer SSN Id',
                           validators=[DataRequired(), Length(min=6)])
    customer_name = StringField('customer Name',
                        validators=[DataRequired()])
    age = IntegerField('Age',
                        validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    state = SelectField('State', choices=['Maharashtra','Gujrat'])
    city = SelectField('City', choices=['Pune','Mumbai','Nashik'])
    submit = SubmitField('SignUp')







class DeleteCustomerForm(FlaskForm):
    customer_ssn_id = StringField('Customer SSN Id',
                           validators=[DataRequired(), Length(min=6)])
    customer_id = StringField('Customer Id',
                           validators=[DataRequired(), Length(min=6)])
    customer_name = StringField('customer Name',
                        validators=[DataRequired()])
    age = IntegerField('Age',
                        validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    
    submit = SubmitField('Delete')







class UpdateCustomerForm(FlaskForm):
    customer_ssn_id = StringField('Customer SSN Id',
                           validators=[DataRequired(), Length(min=6)])
    customer_id = StringField('Customer Id',
                           validators=[DataRequired(), Length(min=6)])
    old_customer_name = StringField('Old Customer Name',
                        validators=[DataRequired()])
    new_customer_name = StringField('New customer Name',
                        validators=[DataRequired()])
    old_address = TextAreaField('Old Address', validators=[DataRequired()])
    new_address = TextAreaField('New Address', validators=[DataRequired()])
    old_age = IntegerField('Old Age',
                        validators=[DataRequired()])
    new_age = IntegerField('New Age',
                        validators=[DataRequired()])
   
    submit = SubmitField('Update')







class CustomerSearchForm(FlaskForm):
    customer_ssn_id = StringField('Customer SSN Id',
                           validators=[DataRequired(), Length(min=6)])
    
    customer_id = StringField('Customer ID',
                           validators=[DataRequired(), Length(min=6)])
    
    
    submit = SubmitField('Search Customer')







class AccountSearchForm(FlaskForm):
    account_id = StringField('Account ID',
                           validators=[DataRequired(), Length(min=6)])
    
    customer_id = StringField('Customer ID',
                           validators=[DataRequired(), Length(min=6)])
    
    
    submit = SubmitField('Search Customer')







class CreateAccountForm(FlaskForm):
    customer_id = StringField('Customer ID',
                           validators=[DataRequired(), Length(min=6)])
    
    account_type = SelectField('Account Type', choices=['Savings Account','Current Account'])
    
    age = IntegerField('Age',
                        validators=[DataRequired()])
    
    submit = SubmitField('Create Account')







class DeleteAccountForm(FlaskForm):
    account_id = StringField('Account ID',
                           validators=[DataRequired(), Length(min=6)])
    
    account_type = SelectField('Account Type', choices=['Savings Account','Current Account'])
    
    
    
    submit = SubmitField('Delete Account')








class GetAccountStatementForm(FlaskForm):
    account_id = StringField('Account ID',
                           validators=[DataRequired(), Length(min=6)])
    
    start_date = DateField('Start Date',validators=[DataRequired()])
        
    end_date = DateField('End Date',validators=[DataRequired()])
      
    
    submit = SubmitField('Get Statement')







class DepositeMoneyForm(FlaskForm):
    customer_id = StringField('Customer ID',
                           validators=[DataRequired(), Length(min=6)])

    account_id = StringField('Account ID',
                           validators=[DataRequired(), Length(min=6)])
    
    account_type = StringField('Account Type',validators=[DataRequired(), Length(min=6)] )

    balance = IntegerField('Balance',validators=[DataRequired()])
    deposite_Amount = IntegerField('Deposite Amount',validators=[DataRequired()])
    submit = SubmitField('Deposite Amount')








class TrasferMoneyForm(FlaskForm):
    source_account_id = StringField('Source Account ID',
                           validators=[DataRequired(), Length(min=6)])

    target_account_id = StringField('Target Account ID',
                           validators=[DataRequired(), Length(min=6)])
    
    source_account_type = SelectField('Source Account Type', choices=['Savings Account','Current Account'])
    
    target_account_type = SelectField('Target Account Type', choices=['Savings Account','Current Account'])
    
    transfer_Amount = IntegerField('Transfer Amount',validators=[DataRequired()])
    submit = SubmitField('Transfer Amount')








class WithdrawMoneyForm(FlaskForm):
    customer_id = StringField('Customer ID',
                           validators=[DataRequired(), Length(min=6)])
    
    account_id = StringField('Account ID',
                           validators=[DataRequired(), Length(min=6)])
    
    account_type = StringField('Account Type',validators=[DataRequired(), Length(min=6)] )

    balance = StringField('Balance',validators=[DataRequired(), Length(min=6)] )

    withdraw_Amount = IntegerField('Withdraw Amount',validators=[DataRequired()])
    submit = SubmitField('Withdraw Amount')







class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

'''
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    '''