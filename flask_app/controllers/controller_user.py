from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/login/create', methods=['POST'])
def login_create():
    if not User.validate_user(request.form):
        return redirect('/')

    ## generate a password hash that will be stored in the database
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    ## make a copy of the incoming request data and replace the password
    ## with the password hash.  This is the data that will be passed to the
    ## INSERT query

    data = {** request.form}
    data['password'] = pw_hash
    id = User.add_user(data)

    session['user_email'] = data['email']
    session['user_id'] = id
    session['user_name'] = data['first_name'] + " " +  data['last_name']
    User.send_email_verify(data)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user_in_db = User.get_user_by_email({'email': request.form['login_email']})
    if not user_in_db:
        flash("Invalid Email/Password")
        session.clear
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_pwd']):
        flash("Invalid Email/Password")
        session.clear
        return redirect('/')
    session['user_email'] = user_in_db.email
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.first_name + " " + user_in_db.last_name

    return redirect('/dashboard')

@app.route('/verify_user',methods=['POST'])
def verify():
    User.send_email_verify({'email': request.form['login_email']})
    flash(f"Verification Email sent to {request.form['login_email']}")
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ("/")