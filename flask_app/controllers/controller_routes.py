from flask import render_template, session, redirect, flash
from flask_app import app
# from flask_app.models.model_user import User
from flask_app.models.model_key import Key
# from flask_app.models import model_key

@app.route('/')
def index():
    return render_template("index.html")

##dashboard
@app.route('/dashboard')
def dashboard():
    if "user_id" in session:
        ## gets the steam keys that the user may receive
        ## by default, these are keys that were submitted by any others
        ## other than the logged in user
        # steam_keys = Key.get_all()
        steam_keys = Key.get_available({'user_id': session['user_id']})
        return render_template("dashboard.html", steam_keys=steam_keys)
    flash ("you must be logged in to view that page.")
    return redirect ('/')

#404
@app.route("/<path:path>")
def default_route(path):
    return f"you tried to go to {path} but there's nothing here yet"