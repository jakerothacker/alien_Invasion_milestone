"""
Alien Invasion
Jake Rothacker
This file contains the AlienInvasion class which organizes and runs the game. Also if this file is run as __main__ the game will start
This code is a variation of sample code provided by Professor Gabriel Walters
7-29-2026
"""
import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien import Alien
from alien_fleet import AlienFleet
from game_stats import GameStats
from time import sleep
from button import Button

class AlienInvasion:
    """A class that contains the Alien Invasion game
    """
    def __init__(self):
        
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        self.game_stats = GameStats(self)

        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,(self.settings.screen_w,self.settings.screen_h))
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)


        self.ship = Ship(self,Arsenal(self))
        self.alien_fleet = AlienFleet(self, Arsenal(self))
        self.alien_fleet.create_fleet()
        self.play_button = Button(self,"Play")
        self.game_active = False

    def run_game(self):
        """runs the Alien Invasion game (Turn on button)
        """
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
            """A method that checks if the ship and an alien collide, the ship is hit by an alien lazer,
               if an alien hits the left, an alien is hit by a lazer, or if all aliens are destroyed
            """
            if self.ship.check_collisions(self.alien_fleet.fleet):
                self._check_game_status()
            if self.ship.check_collisions(self.alien_fleet.arsenal.arsenal):
                self._check_game_status()

            if self.alien_fleet.check_fleet_left():
                self._check_game_status()

            collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
            if collisions:
                self.impact_sound.play()
                self.impact_sound.fadeout(500)
                self.game_stats.update(collisions)

            if self.alien_fleet.check_destroyed_status():
                self._reset_level()
                self.settings.increase_difficulty()
                self.game_stats.update_level()

    def _check_game_status(self):
        """checks if there are any lives left then removes one life and restarts the level if there 
            is a life left otherwise it sets self.game_active to false
        """
        if self.game_stats.ships_left >0:
            self.game_stats.ships_left -=1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

            
    def _reset_level(self):
        """removes old bullets and aliens and make a new alien fleet
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.arsenal.arsenal.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self):
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        #update Hud
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """draws the objects on the screen and flips
        """
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)
        pygame.display.flip()

    def _check_events(self):
        """Checks for player input
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
             self.restart_game()

    def _check_keydown_events(self, event):
        """checks if the player pressed any keys down
        
        Args:
            event: any player input that pygame can recognise
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)

    def _check_keyup_events(self, event):
        
        """checks if the player releaes any keys

        Args:
            event: any player input that pygame can recognise
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()