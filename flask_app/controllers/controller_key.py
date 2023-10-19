from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.model_key import Key
from flask_app.models.model_game import Game
from flask_app import enc_key
from cryptography.fernet import Fernet

@app.route('/submit_key', methods=["POST"])
def submit_key():
    if not Key.validate_key(request.form):
            return redirect('/dashboard')

    ## encode the key to bytes before attempting to encrypt it
    encoded = (request.form['submitted_key']).encode()
    ## encrypt the submitted key before storing it in the database
    f = Fernet(enc_key)
    encrypted_key = f.encrypt(encoded)
    data = {
        'key' : encrypted_key,
        'user_id' : session['user_id']
    }
    key_id = Key.add_key(data)

    ## add the game data to the database to the games table
    game_data = {
        'game_name' : request.form['game_name'],
        'steam_page' : request.form['steam_page'],
        'steam_key_id' : key_id
    }
    game_id = Game.add_game(game_data)


    # print(request.form['submitted_key'])
    # print(encrypted_key)
    # print(len(encrypted_key))

    # decrypted_key = f.decrypt(encrypted_key)
    # print(decrypted_key)
    # print(str(decrypted_key))

    return redirect('/dashboard')





