"""
Ship
Jake Rothacker
This file contains the Ship class which organizes the ship and its armaments. 
This code is a variation of sample code provided by Professor Gabriel Walters
7-25-2026
"""
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    """class controling the player ship and other things (bullets) connected to it
    """

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_w,self.settings.ship_h))
        self.image = pygame.transform.rotate(self.image, 270)

        self.rect = self.image.get_rect()
        
        self.moving_up = False
        self.moving_down = False
        self._center_ship()

        self.arsenal = arsenal

    def _center_ship(self):
        self.rect.midleft = self.boundaries.midleft
        self.y = self.rect.y

    def update(self):
        """Updates movement of ship and arsenal
        """
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Updates movement of ship
        """
        temp_speed = self.settings.ship_speed
        if self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= temp_speed
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed

        self.rect.y = self.y

    def draw(self):
        """draws the ship and arsnal on the screen
        """
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        """Tries to fire a bullet

        Returns:
            Bool: True if a bullet can be fired, False if not
        """
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group):
        if pygame.sprite.spritecollideany(self,other_group):
            self._center_ship()
            return True
        return False