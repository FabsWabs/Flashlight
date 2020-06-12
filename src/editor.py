from pygame.locals import *
import pygame
import pygame_menu
import copy

from src.core.level import Level
from src.core.tile import *
from src.core.utils import resource_path

class Editor():
    """Class to build levels.

    Functions:
    update -- current state gets updated according to the most recent events
    render -- render the current state and output it on the screen
    """

    def __init__(self, grid_size):
        """Initialize all variables, pygame surfaces and menus."""
        self.grid_size = grid_size

        background_url = resource_path('assets/imgs/asphalt.jpg')
        self.background = pygame.image.load(background_url).convert()

        # -------------------------------------------------------------------------
        # Create Theme:
        # -------------------------------------------------------------------------
        pause_theme = pygame_menu.themes.THEME_DARK.copy()
        pause_theme.background_color=(20, 20, 20, 255)

        # -------------------------------------------------------------------------
        # Create Menu: Pause Menu
        # -------------------------------------------------------------------------

        self.pause_menu = pygame_menu.Menu(300, 400, 'Pause',
                                      theme=pause_theme)
        self.pause_menu.add_text_input('Name: ', onchange=self.store, maxchar=15, align=pygame_menu.locals.ALIGN_LEFT)
        self.pause_menu.add_button('Save', self.save)
        self.pause_menu.add_vertical_margin(30)
        self.pause_menu.add_button('Main Menu', self.main_menu)
        self.pause_menu.toggle()

        # -------------------------------------------------------------------------
        # Create Menu: Prompt
        # -------------------------------------------------------------------------

        self.prompt = pygame_menu.Menu(300, 400, 'Pause',
                                      theme=pygame_menu.themes.THEME_ORANGE)
        self.prompt.add_label('You need to at least')
        self.prompt.add_label('place a start and a goal!')
        self.prompt.add_button('Back', self.prompt.toggle)
        self.prompt.toggle()

        self.stored_name = ''
        self.new_level = None
        self.done = False

        self.level = Level()
        self.mouse_pos = (0,0)
        self.mouse_pressed = False
        self.d_pressed = False
        self.active = 1
        self.current_tile = Start(self.mouse_pos)
        self.first_placed = None

        occupied_url = resource_path('assets/imgs/red_cross.png')
        self.occupied_tile = pygame.image.load(occupied_url).convert_alpha()
        delete_url = resource_path('assets/imgs/delete_mask.png')
        self.delete_mask = pygame.image.load(delete_url).convert_alpha()

        self.moved_after_place = True

    def store(self, value):
        """Store the keyboard input from the user."""
        self.stored_name = value
    
    def save(self):
        """Save a finished level."""
        if self.level.is_valid():
            self.level.save(self.stored_name)
            self.new_level = self.stored_name
            self.done = True
        else:
            self.pause_menu.toggle()
            self.prompt.toggle()

    def main_menu(self):
        """Mark the editor instance as done."""
        self.done = True

    def render(self, screen):
        """Render the level in progress and output it on the screen."""
        screen.blit(self.background, (0,0))
        self.level.render(screen)
    
    def update(self, events, screen):
        """Update the editors state depending on the events."""
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.pause_menu.toggle()
                if self.pause_menu.is_enabled():
                    break
                if event.key == K_d:
                    self.active = 'd'
                elif event.key == K_1:
                    self.active = 1
                    self.current_tile = Start(self.mouse_pos)
                elif event.key == K_2:
                    self.active = 2
                    self.current_tile = End(self.mouse_pos)
                elif event.key == K_3:
                    self.active = 3
                    self.current_tile = Box(self.mouse_pos)
                elif event.key == K_4:
                    self.active = 4
                    self.current_tile = Blockage(self.mouse_pos)
                elif event.key == K_5:
                    self.active = 5
                    self.current_tile = Teleporter(self.mouse_pos)
                if self.first_placed is not None:
                    self.level.delete_object(self.first_placed)
                    self.first_placed = None

            if event.type == MOUSEMOTION:
                old = self.mouse_pos
                x, y = event.pos
                self.mouse_pos = x // self.grid_size, y // self.grid_size
                if not old == self.mouse_pos:
                    self.current_tile.change_pos(self.mouse_pos)
                    self.moved_after_place = True

            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                self.mouse_pos = x // self.grid_size, y // self.grid_size
                if event.button == 1:
                    self.mouse_pressed = True
                if event.button == 3:
                    if self.first_placed is not None:
                        type_of_obj = type(self.level.get_object(self.first_placed))
                        self.current_tile = type_of_obj(self.mouse_pos)
                        self.level.delete_object(self.first_placed)
                        self.first_placed = None

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False
                
        if self.pause_menu.is_enabled():
            self.pause_menu.draw(screen)
            self.pause_menu.update(events)
        elif self.prompt.is_enabled():
            self.prompt.draw(screen)
            self.prompt.update(events)
        else:
            if self.mouse_pressed:
                if self.level.is_free(self.mouse_pos):
                    if self.active == 1:
                        self.level.delete_object('Start')
                        self.level.add_object(Start(self.mouse_pos), self.mouse_pos)
                    if self.active == 2:
                        self.level.delete_object('End')
                        self.level.add_object(End(self.mouse_pos), self.mouse_pos)
                    if self.active == 3:
                        self.level.add_object(Box(self.mouse_pos), self.mouse_pos)
                    if self.active == 4:
                        if self.first_placed == None:
                            self.level.add_object(self.current_tile, self.current_tile.get_pos())
                            self.first_placed = self.current_tile.get_pos()
                            self.current_tile = Button(self.mouse_pos)
                        else:
                            self.level.get_objects()[self.first_placed].add_connection(self.mouse_pos)
                            self.current_tile.add_connection(self.first_placed)
                            self.level.add_object(self.current_tile, self.mouse_pos)
                            self.current_tile = Blockage(self.mouse_pos)
                            self.first_placed = None
                    if self.active == 5:
                        if self.first_placed == None:
                            self.level.add_object(self.current_tile, self.current_tile.get_pos())
                            self.first_placed = self.current_tile.get_pos()
                            self.current_tile = Teleporter(self.mouse_pos)
                        else:
                            self.level.get_objects()[self.first_placed].add_connection(self.mouse_pos)
                            self.current_tile.add_connection(self.first_placed)
                            self.level.add_object(self.current_tile, self.mouse_pos)
                            self.current_tile = Teleporter(self.mouse_pos)
                            self.first_placed = None
                    self.moved_after_place = False

                elif self.active == 'd':
                    connect = self.level.get_object(self.mouse_pos).get_connection()
                    self.level.delete_object(self.mouse_pos)
                    if connect is not None:
                        self.level.delete_object(connect)

            self.render(screen)
            if self.active == 'd':
                screen.blit(self.delete_mask, (self.mouse_pos[0] * self.grid_size, self.mouse_pos[1] * self.grid_size))
            else:
                if self.level.is_free(self.mouse_pos):
                    self.current_tile.show(screen)
                elif self.moved_after_place:
                    screen.blit(self.occupied_tile, (self.mouse_pos[0] * self.grid_size, self.mouse_pos[1] * self.grid_size))

        return self.done, self.new_level

