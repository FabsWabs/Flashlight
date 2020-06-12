import pygame
from pygame.locals import *
import pygame_menu
import time

from src.game import Game
from src.editor import Editor
from src.core.level import Level
from src.core.utils import resource_path

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
H_SIZE = 480
W_SIZE = 640

class Runner():
    """A Runner Instance can be used to start the game.

    Functions:
    run -- start and run the game
    """

    def __init__(self):
        """Initialize all variables needed to run the game. """
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((W_SIZE, H_SIZE), 0, 32)
        pygame.display.set_caption("Flashlight 0.1")

        pygame.font.init()

        music_url = resource_path('assets/sound/Keep Searching.mp3')
        self.music = True
        pygame.mixer.music.load(music_url)
        pygame.mixer.music.play(loops=-1)
        self.sfx = True
        
        self.clock = pygame.time.Clock()
        
        background_url = resource_path('assets/imgs/menu_background.jpg')
        self.menu_background = pygame.image.load(background_url).convert()

        self.grid_size = 40
        self.bound = W_SIZE / self.grid_size, H_SIZE / self.grid_size

        self.state = None
        self.game = None
        self.editor = None

        self.delete_field = None
        self.change_delete_menu = False

        self.level = Level()
        self.level_list = self.level.get_all_levels()
    
    def start_level(self, level):
        """Set the state to 'game' and start a level."""
        self.state = 'game'
        self.game = Game(level, self.bound, self.sfx)
        self.main_menu.toggle()
        self.main_menu.full_reset()

    def start_editor(self):
        """Set the state to 'edit' and open the editor."""
        self.state = 'edit'
        self.editor = Editor(self.grid_size)
        self.main_menu.toggle()
        self.main_menu.full_reset()

    def text_input(self, value):
        """Save the data in the delete_menu's input field."""
        self.delete_field = value
    
    def delete(self, level):
        """Delete a level and update the menu accordingly."""
        self.label_widget.set_background_color((255,0,0))
        if level in self.level_list:
            self.level.delete_level(level)
            self.label_widget.set_title(f"'{level}' removed               ")
            self.fill_play_menu(new_level=level)
        else:
            self.label_widget.set_title(f"No Level called '{level}'       ")
        
        self.change_delete_menu = True

    def update_delete_menu(self):
        """Update the delete_menu."""
        self.delete_menu.remove_widget(self.delete_menu.get_widget('label'))
        self.delete_menu.remove_widget(self.delete_menu.get_widget(self.v_margin.get_id()))
        self.delete_menu.remove_widget(self.delete_menu.get_widget('back'))

        self.label_widget = self.delete_menu.add_label("Press 'Enter' to delete", align=pygame_menu.locals.ALIGN_LEFT, label_id='label')
        self.v_margin = self.delete_menu.add_vertical_margin(30)
        self.delete_menu.add_button('Back', pygame_menu.events.RESET, button_id='back')

        self.change_delete_menu = False

    def fill_play_menu(self, new_level=None):
        """Remove all widgets and then fill the play_menu with existing levels."""
        initial = False
        old = False
        new = False
        if new_level == 1:
            initial = True
        elif new_level in self.level_list:
            old = True
        else:
            new = True
        
        # Remove existing buttons
        if not initial:
            for level in self.level_list:
                self.play_menu.remove_widget(self.play_menu.get_widget(level))
            self.play_menu.remove_widget(self.play_menu.get_widget('back'))

        # Update Level List
        if old:
            self.level_list.remove(new_level)
        elif new:
            self.level_list.append(new_level)
            self.level_list = sorted(self.level_list, key=str.lower)
        
        # Add new buttons
        for level in self.level_list:
            self.play_menu.add_button(level, self.start_level, level, button_id=level)
        self.play_menu.add_button('Back', pygame_menu.events.RESET, button_id='back')

    def change_music(self, value, music):
        """Enable or Disable background music."""
        self.music = music
        if self.music:  
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()

    def change_sfx(self, value, sfx):
        """Enable or Disable SFX."""
        self.sfx = sfx

    def run(self):
        """Run the game."""

        # -------------------------------------------------------------------------
        # Create Theme:
        # -------------------------------------------------------------------------
        mytheme = pygame_menu.themes.THEME_DARK.copy()
        mytheme.background_color=(0, 0, 0, 0)


        # -------------------------------------------------------------------------
        # Create menus: Choose Level
        # -------------------------------------------------------------------------

        self.play_menu = pygame_menu.Menu(480, 640, 'Chose Level',
                                     theme=mytheme)
        self.fill_play_menu(new_level=1)

        # -------------------------------------------------------------------------
        # Create menus: Delete Level
        # -------------------------------------------------------------------------

        self.delete_menu = pygame_menu.Menu(480, 640, 'Delete Level',
                                       theme=mytheme)
        self.delete_menu.add_text_input('Level: ', onchange=self.text_input, onreturn=self.delete, maxchar=15, align=pygame_menu.locals.ALIGN_LEFT)
        self.label_widget = self.delete_menu.add_label("Press 'Enter' to delete", align=pygame_menu.locals.ALIGN_LEFT, label_id='label')
        self.v_margin = self.delete_menu.add_vertical_margin(30)
        self.delete_menu.add_button('Back', pygame_menu.events.RESET, button_id='back')

        # -------------------------------------------------------------------------
        # Create menus: Editor Help
        # -------------------------------------------------------------------------

        editorhelp_menu = pygame_menu.Menu(480, 640, 'Editor Help',
                                       theme=mytheme)
        editorhelp_menu.add_label('Left-click for placing a box')
        editorhelp_menu.add_label('Middle-click for placing start')
        editorhelp_menu.add_label('Right-click for placing end')
        editorhelp_menu.add_label('Hold \'d\' for deleting objects')
        editorhelp_menu.add_vertical_margin(30)
        editorhelp_menu.add_button('Back', editorhelp_menu.reset, 1)

        # -------------------------------------------------------------------------
        # Create menus: Editor
        # -------------------------------------------------------------------------

        editor_menu = pygame_menu.Menu(480, 640, 'Editor',
                                       theme=mytheme)
        editor_menu.add_button('New Level', self.start_editor)
        editor_menu.add_button('Delete Level', self.delete_menu)
        editor_menu.add_button('Help', editorhelp_menu)
        editor_menu.add_button('Back', pygame_menu.events.RESET)

        # -------------------------------------------------------------------------
        # Create menus: Help
        # -------------------------------------------------------------------------

        help_menu = pygame_menu.Menu(480, 640, 'Help',
                                     theme=mytheme)
        help_menu.add_label('To finish a level you must reach the goal:')
        im_url = resource_path('assets/imgs/goal_help.png')
        help_menu.add_image(im_url)
        help_menu.add_label('Move with the arrow keys')
        help_menu.add_label('Pause the game with \'ESC\'')
        help_menu.add_vertical_margin(30)
        help_menu.add_label('Build your own levels in the editor')
        help_menu.add_vertical_margin(30)
        help_menu.add_button('Back', pygame_menu.events.RESET, align=pygame_menu.locals.ALIGN_CENTER)

        # -------------------------------------------------------------------------
        # Create menus: Settings Menu
        # -------------------------------------------------------------------------

        settings_menu = pygame_menu.Menu(480, 640, 'Settings',
                                         theme=mytheme)
        settings_menu.add_selector('Music ',
                                   [('ON', True),
                                    ('OFF', False)],
                                    onchange=self.change_music)
        settings_menu.add_selector('Sound FX ',
                                   [('ON', True),
                                    ('OFF', False)],
                                    onchange=self.change_sfx)
        settings_menu.add_button('Back', pygame_menu.events.RESET)

        # -------------------------------------------------------------------------
        # Create menus: Main Menu
        # -------------------------------------------------------------------------

        self.main_menu = pygame_menu.Menu(480, 640, 'Main Menu',
                                     theme=mytheme)

        self.main_menu.add_button('Play', self.play_menu)
        self.main_menu.add_button('Help', help_menu)
        self.main_menu.add_button('Settings', settings_menu)
        self.main_menu.add_button('Editor', editor_menu)
        self.main_menu.add_button('Quit', pygame_menu.events.EXIT)
        
        while True:

            self.clock.tick(FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            
            if self.main_menu.is_enabled():
                self.screen.blit(self.menu_background, (0,0))
                self.main_menu.draw(self.screen)
                self.main_menu.update(events)
                if self.change_delete_menu:
                    self.main_menu.draw(self.screen)
                    pygame.display.flip()
                    time.sleep(1.0)
                    self.update_delete_menu()

            elif self.state == 'game':
                done = self.game.update(events, self.screen)
                if done:
                    self.state = None
                    self.main_menu.toggle()
            elif self.state == 'edit':
                done, new_level = self.editor.update(events, self.screen)
                if done:
                    self.state = None
                    self.main_menu.toggle()
                    if new_level is not None:
                        self.fill_play_menu(new_level)

            pygame.display.flip()