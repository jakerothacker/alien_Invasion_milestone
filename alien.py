"""
Alien
Jake Rothacker
This file contains the Alien class which is responsible for creating, moving, and drawing individual aliens.
This code is a variation of sample code provided by Professor Gabriel Walters
7-29-2026
"""
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """A class that alien enemies and inherites from the sprite class

    Args:
        Sprite (class): simple base class for visible objects
    """
    def __init__(self, fleet:'AlienFleet', x:float,y:float):
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_w,self.settings.alien_h))
        self.image = pygame.transform.rotate(self.image, 270)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)



    def update(self):
        """updates the alien enemy
        """
        temp_speed = self.settings.fleet_speed

        self.y += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y


    def check_edges(self):
        """checks if this alien is on the edge of the screen

        Returns:
            bool: True if at the edge of screen
        """
        return (self.rect.bottom >= self.boundaries.bottom or self.rect.top <= self.boundaries.top)

    def draw_alien(self):
        """draws the alien on the screen
        """
        self.screen.blit(self.image, self.rect)

