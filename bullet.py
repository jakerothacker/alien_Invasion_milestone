"""
Bullet
Jake Rothacker
This file contains the Bullet class which makes the bullets that are a part of the arsenal
This code is a variation of sample code provided by Professor Gabriel Walters
7-25-2026
"""
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Bullet(Sprite):
    """A class that represents bullets and inherites from the sprite class

    Args:
        Sprite (class): simple base class for visible objects
    """
    def __init__(self, game:'AlienInvasion'):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_w,self.settings.bullet_h))
        self.image = pygame.transform.rotate(self.image,270)

        self.rect = self.image.get_rect()
        self.rect.midright = game.ship.rect.midright
        self.x = float(self.rect.x)

    def update(self):
        """moves the bullet based off of the speed in settings
        """
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """draws the bullet on the screen
        """
        self.screen.blit(self.image, self.rect)
