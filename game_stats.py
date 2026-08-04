"""
Game Stats
Jake Rothacker
This file contains the GameStats class which holds informtion that changes during the game like score and lives
This code is a sample code provided by Professor Gabriel Walters
7-29-2026
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats():
    """holds all game information that is constanlty changing during the course of the game (scores,lives,level)
    """
    def __init__(self, game:'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.reset_stats() 

    def reset_stats(self):
        self.score = 0
        self.ships_left = self.settings.starting_ship_count
        self.level = 1

    def update(self,collisions):
        #update score
        self._update_score(collisions)
        self._update_max_score()

    def _update_max_score(self):
        if self.score>self.max_score:
            self.max_score = self.score
        #print(f'max:{self.max_score}')

    def _update_score(self, collisions):
        for alien in collisions.values():
            self.score += self.settings.alien_points
        #print(f'basic: {self.score}')

        #update high

    def update_level(self):
        self.level += 1
        #print(self.level)

        
        