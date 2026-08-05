"""
Button
Jake Rothacker
This file contains the Button class which has a message and can tell if it gets clicked.
This code is a variation of sample code provided by Professor Gabriel Walters
8-5-2026
"""
import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Button:
    """class that creates a button for the player to press
    """
    def __init__(self, game : "AlienInvasion", msg):
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings =  game.settings

        self.font = pygame.font.Font(self.settings.font_file,
                    self.settings.button_font_size)
        self.rect = pygame.Rect(0,0,self.settings.button_w,self.settings.button_h)
        self.rect.center = self.boundaries.center
        self.prep_msg(msg)

    def prep_msg(self,msg):
        """takes the msg and gets it ready to be drawn

        Args:
            msg (str): what the button should say
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color,None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """draws the button and msg (msg on top)
        """
        self.screen.fill(self.settings.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """checks if the mouse is on the button (only use afte a click has occured)

        Args:
            mouse_pos (tuple): the screen courdinates of the mouse

        Returns:
            bool: True if the mouse is on the button
        """
        return self.rect.collidepoint(mouse_pos)