import pygame
import pygame_menu

file = 'sound/Keep Searching.mp3'

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
SCREEN = pygame.display.set_mode((600, 400))

button_list = ['Talk', 'Listen']

def set_difficulty(value, difficulty):
    '''Sets difficulty.'''
    print(value, difficulty)

def start_the_game():
    '''Starts the game.'''

def delete_widget():
    global button_list
    button_list.remove('Talk')
    create_menu()
    #print(SUBMENU.get_widget('Talk'))

def create_menu():
    global MENU, SUBMENU, button_list
    SUBMENU = pygame_menu.Menu(300, 400, 'Welcome',
                           theme=pygame_menu.themes.THEME_BLUE)
    for button in button_list:
        SUBMENU.add_button(button, start_the_game, button_id=button)
    SUBMENU.add_button('Back', pygame_menu.events.RESET)


    MENU = pygame_menu.Menu(300, 400, 'Welcome',
                            theme=pygame_menu.themes.THEME_BLUE)

    MENU.add_text_input('Name :', default='John Doe')
    MENU.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    MENU.add_button('Submenu', SUBMENU)
    MENU.add_button('Delete Widget', delete_widget)
    MENU.add_button('Quit', pygame_menu.events.EXIT)

MENU = None
SUBMENU = None
create_menu()
while True:
    MENU.mainloop(SCREEN)

print('done')

