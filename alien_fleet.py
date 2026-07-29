import pygame
from typing import TYPE_CHECKING
from alien import Alien
import random
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


class AlienFleet:

    def __init__(self, game:'AlienInvasion', arsenal :'Arsenal'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        #self.create_fleet() #REMOVE THIS LATER I THINK IT IS THE REASON FOR THE 2X HEALTH ALIENS
        self.arsenal = arsenal

    def create_fleet(self):
        alien_w = self.settings.alien_h #h and w are switched due to rotation
        alien_h = self.settings.alien_w #since alien is currently square not a big deal
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_h,fleet_w = self.calculate_fleet_size(alien_h, screen_h , alien_w, screen_w)

        half_screen = screen_w // 2
        y_offset, x_offset = self.calc_offset(alien_w, alien_h, screen_h, fleet_h, fleet_w, half_screen)
       
        self._create_rectangle_fleet(alien_w, alien_h, fleet_h, fleet_w, half_screen, y_offset, x_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_h, fleet_w, half_screen, y_offset, x_offset):
        for col in range(fleet_w):
            for row in range(fleet_h):
                current_y = alien_h *row + y_offset
                current_x = alien_w *col + x_offset + half_screen
                if row % 2 ==0 or col%2 == 0:
                    continue
                self._create_alien(current_x , current_y)

    def calc_offset(self, alien_w, alien_h, screen_h, fleet_h, fleet_w, half_screen):
        fleet_vertical_space = fleet_h * alien_h
        fleet_horizontal_space = fleet_w * alien_w
        y_offset = int((screen_h-fleet_vertical_space)//2)
        x_offset = int((half_screen-fleet_horizontal_space)//2)
        return y_offset,x_offset

    def calculate_fleet_size(self, alien_h, screen_h, alien_w, screen_w):

        fleet_h = (screen_h//alien_h)
        fleet_w = ((screen_w//2)//alien_w)

        if fleet_h %2 == 0:
            fleet_h -= 1
        else:
            fleet_h -=2

        if fleet_w %2==0:
            fleet_w -= 1
        else:
            fleet_w -=2

        return fleet_h,fleet_w


    def _create_alien(self, current_x:int , current_y:int):

        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
                
    def _drop_alien_fleet(self):
        for alien in self.fleet:
            alien.x -= self.fleet_drop_speed

    def update_fleet(self):
        self._check_fleet_edges()
        self.fleet.update()
        self.arsenal.update_arsenal()
        self.aliens_fire()

    def draw(self):
        alien: Alien
        for alien in self.fleet:
            alien.draw_alien()
        self.arsenal.draw()

    def check_collisions(self, other_group):
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_left(self):
        alien:Alien
        for alien in self.fleet:
            if alien.rect.left <= 0:
                return True
        return False

    def check_destroyed_status(self):
        return not self.fleet

    def aliens_fire(self):
        if random.randint(1,100) == 1:
            random_alien = random.choice(self.fleet.sprites())
            random_alien_midleft = random_alien.rect.midleft
           
            self.arsenal.fire_bullet(random_alien_midleft,self.settings.fleet_bullet_direction)