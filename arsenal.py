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
        """removes bullets that are right of the screen)
        """
        for bullet in self.arsenal.copy():
            if bullet.rect.left >= self.settings.screen_w :
                self.arsenal.remove(bullet)

    def draw(self):
        """draws each bullet in the arsenal
        """
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self):
        """adds a bullet to the sprte group if able to

        Returns:
            Bool: Returns true if a bullet was added, False otherwise
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False

