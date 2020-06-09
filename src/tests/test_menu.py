import pygame
from pygame.locals import *
import pygame_menu

pygame.init()
SCREEN = pygame.display.set_mode((600, 400))
button_list = ['Option1', 'Option2']

def placeholder():
    '''placeholder method'''

def delete_widget():
    SUBMENU.remove_widget(SUBMENU.get_widget('Option1'))

SUBMENU = pygame_menu.Menu(300, 400, 'Submenu',
                        theme=pygame_menu.themes.THEME_BLUE)
for button in button_list:
    SUBMENU.add_button(button, placeholder, button_id=button)
SUBMENU.add_button('Back', pygame_menu.events.RESET)


MENU = pygame_menu.Menu(300, 400, 'Welcome',
                        theme=pygame_menu.themes.THEME_BLUE)
MENU.add_button('Submenu', SUBMENU)
MENU.add_button('Delete Widget', delete_widget)
MENU.add_button('Quit', pygame_menu.events.EXIT)

while True:
    MENU.mainloop(SCREEN)

