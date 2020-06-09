import pygame
from pygame.locals import *
import numpy as np
import os
import pygame_menu
import time

from src.core.level import Level
from src.core.tile import *
from src.core.utils import resource_path


class Game():
    def __init__(self, level, bound, sfx):
        self.level = Level(name=level)
        self.player = Player(self.level.get_start_tuple())
        background_url = resource_path('assets/imgs/asphalt.jpg')
        self.background = pygame.image.load(background_url).convert()
        mask_url = resource_path('assets/imgs/mask.png')
        self.mask = pygame.image.load(mask_url).convert_alpha()
        letter_t_url = resource_path('assets/imgs/letter_t.png')
        self.letter_t = pygame.image.load(letter_t_url).convert_alpha()
        self.bound = bound
        self.sfx = sfx

        self._sound_library = {}

        self.goal_reached = False
        self.done = False
        self.direction_pressed = 0

        # -------------------------------------------------------------------------
        # Create Theme:
        # -------------------------------------------------------------------------
        pause_theme = pygame_menu.themes.THEME_DARK.copy()
        pause_theme.background_color=(20, 20, 20, 255)

        self.pause_menu = pygame_menu.Menu(300, 400, 'Pause',
                                      theme=pause_theme)
        self.pause_menu.add_button('Continue', self.cont)
        self.pause_menu.add_vertical_margin(30)
        self.pause_menu.add_button('Main Menu', self.main_menu)
        self.pause_menu.toggle()

    def cont(self):
        self.pause_menu.toggle()

    def play_sound(self, path):
        path = os.path.join('assets/sound/SFX/', path)
        path = resource_path(path)
        sound = self._sound_library.get(path)
        if sound == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound = pygame.mixer.Sound(canonicalized_path)
            self._sound_library[path] = sound
        if self.sfx:
            sound.play()

    def main_menu(self):
        self.done = True

    def goal_animation(self, screen):
        dt = 0.3
        dif_w = 40
        dif_h = 30
        size = (600, 450)
        pos = (20, 15)
        pygame.draw.rect(screen, (0, 0, 255), Rect(pos, size))
        pygame.display.flip()

        size = (size[0] - 2 * dif_w, size[1] - 2 * dif_h)
        pos = (pos[0] + dif_w, pos[1] + dif_h)
        time.sleep(dt)
        pygame.draw.rect(screen, (0, 255, 0), Rect(pos, size))
        pygame.display.flip()

        size = (size[0] - 2 * dif_w, size[1] - 2 * dif_h)
        pos = (pos[0] + dif_w, pos[1] + dif_h)
        time.sleep(dt)
        pygame.draw.rect(screen, (255, 255, 0), Rect(pos, size))
        pygame.display.flip()

        size = (size[0] - 2 * dif_w, size[1] - 2 * dif_h)
        pos = (pos[0] + dif_w, pos[1] + dif_h)
        time.sleep(dt)
        pygame.draw.rect(screen, (255, 140, 0), Rect(pos, size))
        pygame.display.flip()

        size = (size[0] - 2 * dif_w, size[1] - 2 * dif_h)
        pos = (pos[0] + dif_w, pos[1] + dif_h)
        time.sleep(dt)
        pygame.draw.rect(screen, (255, 0, 0), Rect(pos, size))
        pygame.display.flip()

        self.play_sound('yeah.wav')
        myfont = pygame.font.SysFont('Comic Sans MS', 60, bold=True)
        text = myfont.render('YEAH!', True, (0, 0, 0))
        text_rect = text.get_rect(center=(640/2, 480/2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)

    def check_if_in_bounds(self, next_pos):
        flag = True
        next_i, next_j = next_pos
        if not 0 < next_i < self.bound[0] or not 0 < next_j < self.bound[1]:
            flag = False
        return flag 

    def teleport(self, screen, loc):
        self.play_sound('teleport.wav')
        transition_speed = 1.1
        alpha = 1
        while alpha <= 720:
            alpha = int(np.ceil(alpha * transition_speed))
            self.render(screen, alpha)
            pygame.display.flip()
        self.player.change_pos(loc)
        while alpha >= 1:
            alpha = int(alpha/transition_speed)
            self.render(screen, alpha)
            pygame.display.flip()
        
    def move(self, screen):
        direction = self.player.get_direction()
        prog = 0
        while prog < 1:
            self.render(screen, trans=direction + prog)
            pygame.display.flip()
            prog += 0.04
        self.player.move(direction)

    def render(self, screen, alpha=0, trans=0.0):
        screen.blit(self.background, (0,0))
        self.level.render(screen)
        self.player.show(screen, alpha, trans)
        screen.blit(pygame.transform.rotate(self.mask, 360 - self.player.get_direction() * 90), self.player.get_coords(trans))
        if type(self.level.get_object(self.player.get_pos())) == Teleporter:
            coords_i, coords_j = self.player.get_pos()
            coords_i, coords_j = coords_i * 40 - 10 , coords_j * 40 - 10
            # calculate offsets
            direction = self.player.get_direction()
            if direction == 1:
                coords_i -= 60
            elif direction == 2:
                coords_j -= 60
            elif direction == 3:
                coords_i += 60
            elif direction == 4:
                coords_j += 60

            coords = coords_i, coords_j
            screen.blit(self.letter_t, coords)

    def update(self, events, screen):
        for event in events:
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_DOWN or event.key == K_LEFT or event.key == K_UP:
                    self.direction_pressed = 0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.pause_menu.toggle()
                    break
                if not self.pause_menu.is_enabled():
                    cur_obj = self.level.get_object(self.player.get_pos())

                    if event.key == K_RIGHT:
                        self.direction_pressed = 1
                    elif event.key == K_LEFT:
                        self.direction_pressed = 3
                    elif event.key == K_UP:
                        self.direction_pressed = 4
                    elif event.key == K_DOWN:
                        self.direction_pressed = 2
                    elif event.key == K_t and type(cur_obj) == Teleporter:
                        self.teleport(screen, cur_obj.get_connection())
                        break

        if not self.direction_pressed == 0:
            self.player.set_direction(self.direction_pressed)

            next_pos = self.player.get_pos(self.direction_pressed)
            next_obj = self.level.get_object(next_pos)

            if not (type(next_obj) is Box or (type(next_obj) is Blockage and not next_obj.get_open())) and self.check_if_in_bounds(next_pos):
                if type(next_obj) is Button and next_obj.activate():
                    self.play_sound('button.wav')
                    self.level.get_object(next_obj.get_connection()).activate()
                else:
                    self.play_sound('footstep.wav')
                self.move(screen)
            else:
                self.play_sound('knock.wav')
            
        if self.player.get_pos() == self.level.get_end_tuple():
            self.goal_animation(screen)
            self.done = True
        if self.pause_menu.is_enabled():
            self.pause_menu.draw(screen)
            self.pause_menu.update(events)
        else:
            self.render(screen)
        return self.done