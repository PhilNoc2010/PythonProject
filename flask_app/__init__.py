from flask import Flask
from flask_mail import Mail, Message
from cryptography.fernet import Fernet   ## <-- moved from server.py
app = Flask(__name__)
app.secret_key = "Your Princess is in another castle"
import re
import datetime
import os

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nocerini@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('gmail_pwd_demo')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

DATABASE = "steam_exchange_db"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CHAR_REGEX = re.compile(r'^[a-zA-Z]+$')
NUM_REGEX = re.compile(r'^[0-9]+$')
PWD_REGEX = re.compile(r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9]).{8,}$')
STEAM_KEY_REGEX = re.compile(r'^[a-zA-Z0-9]{5}[-][a-zA-Z0-9]{5}[-][a-zA-Z0-9]{5}$')

key_file_name = "key.key"
enc_key = ""

def write_key():
    enc_key = Fernet.generate_key()
    with open(key_file_name, "wb") as key_file:
        key_file.write(key_file_name)

def load_key():
    return open(key_file_name, "rb").read()

try:
    with open(key_file_name, "rb") as key_file:
        enc_key = load_key()
except:
    print("can't find the keyfile")
    # write_key()
    # enc_key = load_key()

CurrentDate = datetime.datetime.today()
print (CurrentDate)