"""
Settings
Jake Rothacker
This file contains the Settings class which holds values that are static or change infrequently during the course of the game.
This code is a variation of sample code provided by Professor Gabriel Walters
7-25-2026
"""
from pathlib import Path
class Settings:

    def __init__(self):
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.difficulty_scale = 1.1

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_w = 40
        self.ship_h = 60
        


        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'

        self.ship_bullet_direction = 1
        self.fleet_bullet_direction = -1

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_h = 40
        self.alien_w = 40
        self.fleet_direction = 1
        
        self.button_w = 200
        self.button_h = 50
        self.button_color = (0,135,50)

        self.text_color = (255,255,255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

    def initialize_dynamic_settings(self):
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_speed = 7
        self.bullet_amount = 5
        self.bullet_w = 25
        self.bullet_h = 80
        self.fleet_fire_chance = 20 #this is a chance out of 1000 per frame that a random alien shoots

        self.fleet_speed = 2
        self.fleet_drop_speed = 40   
        self.alien.points = 50

    def increase_difficulty(self):
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale



