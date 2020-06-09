import pygame
from pygame.locals import *

from src.core.utils import resource_path

grid_size = 40

class Tile:
    def __init__(self, pos):
        self.i, self.j = pos
        self.grid_size = grid_size
        self.connection_key = None
        self.add_surf()

    def add_surf(self):
        self.surf = None
    
    def del_surf(self):
        self.surf = None

    def show(self, screen):        
        screen.blit(self.surf, (self.i * self.grid_size, self.j * self.grid_size))

    def __str__(self):
        return "i = " + str(self.i) + "  |  j = " + str(self.j) + "  |  size = " + str(self.grid_size)

    def get_pos(self, action=None):
        if action == 1:
            return self.i + 1, self.j
        elif action == 2:
            return self.i, self.j + 1
        elif action == 3:
            return self.i - 1, self.j
        elif action == 4:
            return self.i, self.j - 1
        else:
            return self.i, self.j

    def change_pos(self, pos):
        self.i, self.j = pos

    def add_connection(self, connection_key):
        self.connection_key = connection_key

    def get_connection(self):
        return self.connection_key

class Box(Tile):
    Type = "BOX"

    def add_surf(self):
        surf_url = resource_path('assets/imgs/box.png')
        self.surf = pygame.image.load(surf_url).convert_alpha()
    
class Start(Tile):
    Type = "START"

    def add_surf(self):
        surf_url = resource_path('assets/imgs/start.png')
        self.surf = pygame.image.load(surf_url).convert_alpha()


class End(Tile):
    Type = "END"

    def add_surf(self):
        surf_url = resource_path('assets/imgs/goal.png')
        self.surf = pygame.image.load(surf_url).convert_alpha()
    
class Button(Tile):
    def __init__(self, pos):
        self.i, self.j = pos
        self.grid_size = grid_size
        self.connection_key = None
        self.pressed = False
        self.add_surf()

    def add_surf(self):
        surf_url = resource_path('assets/imgs/red_button.png')
        self.surf = pygame.image.load(surf_url).convert_alpha()
    
    def activate(self):
        if self.pressed:
            return False
        else:
            self.pressed = True
            surf_url = resource_path('assets/imgs/green_button.png')
            self.surf = pygame.image.load(surf_url).convert_alpha()
            return True

class Blockage(Tile):
    def __init__(self, pos):
        self.i, self.j = pos
        self.grid_size = grid_size
        self.connection_key = None
        self.open = False
        self.add_surf()
    
    def add_surf(self):
        surf_url = resource_path('assets/imgs/red_block.png')
        self.surf = pygame.image.load(surf_url).convert_alpha()

    def get_open(self):
        return self.open
        
    def activate(self):
        self.open = True
        surf_url = resource_path('assets/imgs/green_block.png')
        self.surf = pygame.image.load(surf_url).convert_alpha()

class Teleporter(Tile):

    def add_surf(self):
        surf_url = resource_path('assets/imgs/teleporter.png')
        self.surf = pygame.image.load(surf_url).convert_alpha()

class Player(Tile):
    Type = "PLAYER"
    def __init__(self, pos):
        self.i, self.j = pos
        #       4
        #   3       1
        #       2
        self.direction = 1
        self.grid_size = grid_size
        self.add_surf()

    def add_surf(self):
        surf_url = resource_path('assets/imgs/player.png')
        self.surf = pygame.image.load(surf_url).convert_alpha()

    def show(self, screen, alpha=0, trans=0.0):
        trans_i, trans_j = 0.0, 0.0
        if int(trans) == 1:
            trans_i = trans % 1
        elif int(trans) == 2:
            trans_j = trans % 1
        elif int(trans) == 3:
            trans_i = - (trans % 1)
        elif int(trans) == 4:
            trans_j = - (trans % 1)

        screen.blit(pygame.transform.rotate(self.surf, 360 - self.direction * 90 + alpha), ((self.i + trans_i) * self.grid_size, (self.j + trans_j) * self.grid_size))

    def get_coords(self, trans=0.0):
        trans_i, trans_j = 0.0, 0.0
        if int(trans) == 1:
            trans_i = trans % 1
        elif int(trans) == 2:
            trans_j = trans % 1
        elif int(trans) == 3:
            trans_i = - (trans % 1)
        elif int(trans) == 4:
            trans_j = - (trans % 1)

        di_c, dj_c = 20, 20
        dif_i, dif_j = 640 - di_c, 640 - dj_c
        return self.grid_size * (self.i + trans_i) - dif_i, self.grid_size * (self.j + trans_j) - dif_j
    
    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def move(self, direction):
        if direction == 1:
            self.i += 1
        elif direction == 2:
            self.j += 1
        elif direction == 3:
            self.i -= 1
        elif direction == 4:
            self.j -= 1
