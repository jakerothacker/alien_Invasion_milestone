"""
Alien Fleet
Jake Rothacker
This file contains the AlienFleet class which controls the creation and movement of the alien enemies.
This code is a variation of sample code provided by Professor Gabriel Walters
7-29-2026
"""
import pygame
from typing import TYPE_CHECKING
from alien import Alien
import random
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


class AlienFleet:
    """A class operating the fleet of aliens as a group
    """
    def __init__(self, game:'AlienInvasion', arsenal :'Arsenal'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        #self.create_fleet() #REMOVE THIS LATER I THINK IT IS THE REASON FOR THE 2X HEALTH ALIENS
        self.arsenal = arsenal

    def create_fleet(self):
        """contains multiple methods that builds the group of enemy aliens
        """
        alien_w = self.settings.alien_h #h and w are switched due to rotation
        alien_h = self.settings.alien_w #since alien is currently square not a big deal
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_h,fleet_w = self.calculate_fleet_size(alien_h, screen_h , alien_w, screen_w)

        half_screen = screen_w // 2
        y_offset, x_offset = self.calc_offset(alien_w, alien_h, screen_h, fleet_h, fleet_w, half_screen)
       
        self._create_rectangle_fleet(alien_w, alien_h, fleet_h, fleet_w, half_screen, y_offset, x_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_h, fleet_w, half_screen, y_offset, x_offset):
        """creates aliens in a rectangular formation with one alien gap horizontal and vertical between each

        Args:
            alien_w (Int): how wide the alien sprite is
            alien_h (Int): how tall the alien sprite is
            fleet_h (Int): how many aliens tall the fleet is
            fleet_w (Int): how many aliens wide the fleet is
            half_screen (Int): half the horizontal distance of the screen
            y_offset (Int): offset in the vertical direction on each side of the fleet
            x_offset (Int): offset in the horizontal direction on each side of the fleet
        """
        for col in range(fleet_w):
            for row in range(fleet_h):
                current_y = alien_h *row + y_offset
                current_x = alien_w *col + x_offset + half_screen
                if row % 2 ==0 or col%2 == 0:
                    continue
                self._create_alien(current_x , current_y)

    def calc_offset(self, alien_w, alien_h, screen_h, fleet_h, fleet_w, half_screen):
        """calculates the offset required to horizontaly center the fleet and verticaly in the right half of the screen.

        Args:
            alien_w (Int): how wide the alien sprite is
            alien_h (Int): how tall the alien sprite is
            screen_h (Int): how tall the screen is
            fleet_h (Int): how many aliens tall the fleet is
            screen_w (Int): how wide the screen is
            fleet_w (Int): how many aliens wide the fleet is
            half_screen (Int): half the horizontal distance of the screen

        Returns:
            Tuple: The x and y offset required for the fleet to be centered in the right half of screen
        """
        fleet_vertical_space = fleet_h * alien_h
        fleet_horizontal_space = fleet_w * alien_w
        y_offset = int((screen_h-fleet_vertical_space)//2)
        x_offset = int((half_screen-fleet_horizontal_space)//2)
        return y_offset,x_offset

    def calculate_fleet_size(self, alien_h, screen_h, alien_w, screen_w):
        """finds dimensions of the fleet in terms of the number of aliens 

        Args:
            alien_h (int): how tall the alien sprite is
            screen_h (int): how tall the screen is
            alien_w (int): how wide the alien sprite is
            screen_w (int): how wide the screen is
            
        Returns:
            tuple: (the number of aliens tall the fleet can be, the number of aliens wide the fleet can be)
        """
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
        """creates an alien and adds it to the fleet at a given location

        Args:
            current_x (int): distance from the left of the screen
            current_y (int): distance from the top of the screen
        """

        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """moves the fleet left and changes direction if at least one alien is at the edge of the screen
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
                
    def _drop_alien_fleet(self):
        """drops the alien fleet to the left
        """
        for alien in self.fleet:
            alien.x -= self.fleet_drop_speed

    def update_fleet(self):
        """updates the fleet by checking for one on the edge and then moves every alien
        """
        self._check_fleet_edges()
        self.fleet.update()
        self.arsenal.update_arsenal()
        self.aliens_fire()

    def draw(self):
        """draws all aliens in the fleet
        """
        alien: Alien
        for alien in self.fleet:
            alien.draw_alien()
        self.arsenal.draw()

    def check_collisions(self, other_group):
        """checks if any member of the fleet is colliding with sprite from a different group and deletes both

        Args:
            other_group (group): the group of sprites that is colliding with the aliens

        Returns:
            dictionary: returns all the sprites colided and were destroyed
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_left(self):
        """checks if the fleet has reached the left of the screen

        Returns:
            Bool: True if at least one alien is at the left of the screen
        """
        alien:Alien
        for alien in self.fleet:
            if alien.rect.left <= 0:
                return True
        return False

    def check_destroyed_status(self):
        """checks if there are any aliens left in the fleet

        Returns:
            Bool: True if there are zero aliens left, false otherwise 
        """
        return not self.fleet

    def aliens_fire(self):
        """checks if the aliens try to shoot a bullet, then fire if they are able to
        """
        min_x = self.settings.screen_w
        for alien in self.fleet:
            x_pos = alien.x
            if x_pos < min_x:
                min_x = x_pos
        distance_modifier = min_x*(100/self.settings.fleet_fire_ave)/self.settings.screen_w

        if random.randint(1,1000) <= self.settings.fleet_fire_chance *(distance_modifier**self.settings.fleet_fire_power_factor):
            random_alien = random.choice(self.fleet.sprites())
            if random_alien.rect.left >= self.settings.fleet_fire_min_distance*self.settings.screen_w/100:
                random_alien_midleft = random_alien.rect.midleft
                self.arsenal.fire_bullet(random_alien_midleft,self.settings.fleet_bullet_direction)