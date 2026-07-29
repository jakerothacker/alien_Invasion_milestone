"""
Arsenal
Jake Rothacker
This file contains the Arsenal class which organizes the bullets into a pygame sprite group
This code is a variation of sample code provided by Professor Gabriel Walters
7-29-2026
"""
import pygame
from typing import TYPE_CHECKING
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """Class containtin all the firepower expened by the ship
    """
    def __init__(self, game:'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """updates all sprites in the arsenal sprite group
        """
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """removes bullets that are right or left of the screen)
        """
        for bullet in self.arsenal.copy():
            if bullet.rect.left >= self.settings.screen_w or bullet.rect.right<=0:
                self.arsenal.remove(bullet)

    def draw(self):
        """draws each bullet in the arsenal
        """
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self,location,direction):
        """adds a bullet to the sprite group if able to

        Args:
            location (tuple): x and y coordinate of where the bullet originates
            direction (Int): 1 or -1 so the bullet moves in the right direction

        Returns:
            Bool: Returns true if a bullet was added, False otherwise
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game,location,direction)
            self.arsenal.add(new_bullet)
            return True
        return False

