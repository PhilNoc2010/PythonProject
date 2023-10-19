from flask_app.config.mySQLconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import EMAIL_REGEX, CHAR_REGEX, PWD_REGEX
from flask import flash
from flask_app import mail, Message


class User:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.steam_name = data['steam_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #C
    @classmethod
    def add_user(cls, data:dict) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password, steam_name) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(steam_name)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id

    #R
    @classmethod
    def get_user_by_email(cls, data:dict) -> dict:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        instance = results[0]
        user = cls(instance)
        return user


    #U

    #D

    ### Validation Methods
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First Name must be longer than 2 characters")
            is_valid = False
        if not CHAR_REGEX.match(user['first_name']):
            flash("First Name must contain only alphabetic characters")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be longer than 2 characters")
            is_valid = False
        if not CHAR_REGEX.match(user['last_name']):
            flash("Last Name must contain only alphabetic characters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("email is not in a valid format")
            is_valid = False
        else:
            potential_user = User.get_user_by_email({'email' : user['email']})
            if potential_user:
                flash("This email is already registered")
                is_valid = False
        if len(user['password']) < 9:
            flash("Password must be longer than 8 characters")
            is_valid = False
        if not PWD_REGEX.match(user['password']):
            flash("Password contain an Upper Case letter, lower case letter, and 1 numeric character")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Both password fields must match")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        print(user)
        if not EMAIL_REGEX.match(user['login_email']):
            flash("email is not in a valid format")
            is_valid = False
        if len(user['login_pwd']) < 9:
            flash("Password must be longer than 8 characters")
            is_valid = False
        return is_valid

    @staticmethod
    def send_email_verify(user):
        msg = Message()
        email_address = [user['email']]
        email_body = f"Please validate your email address in order to receive keys in the future.  Please check your email at {user['email']} and complete the verification process."
        print(email_body)
        msg.subject = "Subject Line"
        msg.recipients = email_address
        msg.sender = 'nocerini@gmail.com'
        msg.body = email_body
        msg.reply_to = 'noreply@demo.com'
        # mail.send(msg)
        return None

