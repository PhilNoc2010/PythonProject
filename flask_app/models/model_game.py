from flask_app.config.mySQLconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import EMAIL_REGEX, CHAR_REGEX, PWD_REGEX
from flask import flash

class Game:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.game_name = data['game_name']
        self.steam_page = data['steam_page']
        self.steam_key_id = data['steam_key_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #C
    @classmethod
    def add_game(cls, data:dict) -> int:
        query = "INSERT INTO games (game_name, steam_page, steam_key_id) VALUES (%(game_name)s, %(steam_page)s, %(steam_key_id)s);"
        print(query)
        game_id = connectToMySQL(DATABASE).query_db(query, data)
        return game_id

    #R

    #U

    #D