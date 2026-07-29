"""
Game Stats
Jake Rothacker
This file contains the GameStats class which holds informtion that changes during the game like score and lives
This code is a sample code provided by Professor Gabriel Walters
7-29-2026
"""
class GameStats():
    """holds all game information that is constanlty changing during the course of the game (scores,lives,level)
    """
    def __init__(self, ships_left):
        self.ships_left = ships_left