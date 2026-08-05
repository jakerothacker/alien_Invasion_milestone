"""
Game Stats
Jake Rothacker
This file contains the GameStats class which holds informtion that changes during the game like score and lives
This code is a sample code provided by Professor Gabriel Walters
8-5-2026
"""
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats():
    """holds all game information that is constanlty changing during the course of the game (scores,lives,level)
    """
    def __init__(self, game:'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats() 

    def init_saved_scores(self):
        """either takes the stored hi-score form a json file or saves a file with score of 0
        """
        self.path = self.settings.scores_file
        try:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi-score',0)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as err:
            self.hi_score = 0
            self.save_scores()
            print(f"{err} when checking HighScore")

    def save_scores(self):
        """saves current hi-score to json save file
        """
        scores = {
            'hi-score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found {e}')


    def reset_stats(self):
        """resets the stats to start a new game (lives, reg score,level)
        """
        self.score = 0
        self.ships_left = self.settings.starting_ship_count
        self.level = 1

    def update(self,collisions):
        """updates the scores based off of bullets coliding with aliens

        Args:
            collisions (dict): a dicitonary showing all the aliens coliding with a bullet
        """
        self._update_score(collisions)
        self._update_max_score()
        self._update_hi_score()

    def _update_max_score(self):
        """update the max score if it is surpassed
        """
        if self.score>self.max_score:
            self.max_score = self.score

    def _update_hi_score(self):
        """update the hi score if it is surpassed
        """
        if self.score>self.hi_score:
            self.hi_score = self.score

    def _update_score(self, collisions):
        """updates the regular score based off of bullets coliding with aliens

        Args:
            collisions (dict): a dicitonary showing all the aliens coliding with a bullet
        """
        for alien in collisions.values():
            self.score += self.settings.alien_points
        

    def update_level(self):
        """increases the level by one
        """
        self.level += 1
        

        
        