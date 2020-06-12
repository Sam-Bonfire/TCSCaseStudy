import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or  "secret_key"
    #key generated using - py -c "import os; print(os.urandom(16))" command

    #MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }