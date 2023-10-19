from flask_app.config.mySQLconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import STEAM_KEY_REGEX
from flask import flash
from flask_app.models import model_game
from flask_app import enc_key
from cryptography.fernet import Fernet


class Key:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.steam_key = data['steam_key']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #C
    @classmethod
    def add_key(cls, data:dict) -> int:
        query = "INSERT INTO steam_keys (steam_key, user_id) VALUES (%(key)s, %(user_id)s);"
        key_id = connectToMySQL(DATABASE).query_db(query, data)
        return key_id


    #R
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM steam_keys JOIN games ON steam_keys.id = games.steam_key_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if not results:
            return False
        key_list = []
        for dict in results:
            steam_key = cls(dict)
            #extract Game Data
            game_data = {
                ** dict,
                'id': dict['games.id'],
                'created_at' : dict['games.created_at'],
                'updated_at' : dict['games.updated_at']
            }
            #create game instance
            game_instance = model_game.Game(game_data)
            # attach to key instance
            steam_key.game = game_instance

            #decrypt the steam key before showing it to the user
            f = Fernet(enc_key)
            decrypted_key = f.decrypt(steam_key.steam_key)
            steam_key.steam_key = decrypted_key

            key_list.append(steam_key)
        return key_list

    @classmethod
    def get_available(cls, data:dict):
        query = "SELECT * FROM steam_keys JOIN games ON steam_keys.id = games.steam_key_id  WHERE user_id <> %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        key_list = []
        for dict in results:
            steam_key = cls(dict)
            #extract Game Data
            game_data = {
                ** dict,
                'id': dict['games.id'],
                'created_at' : dict['games.created_at'],
                'updated_at' : dict['games.updated_at']
            }
            #create game instance
            game_instance = model_game.Game(game_data)
            # attach to key instance
            steam_key.game = game_instance

            #decrypt the steam key before showing it to the user
            f = Fernet(enc_key)
            decrypted_key = f.decrypt(steam_key.steam_key)
            steam_key.steam_key = decrypted_key

            key_list.append(steam_key)
        return key_list

    #U

    #D

    #Validation Methods
    @staticmethod
    def validate_key(key):
        is_valid=True
        if len(key['submitted_key']) <16:
            flash("Please ensure your key is of the proper length")
            is_valid = False
        if not STEAM_KEY_REGEX.match(key['submitted_key']):
            flash("this key is not in the proper format.  Please double check and re-submit.")
            print(key['submitted_key'])
            is_valid = False
        return is_valid