from src.core.tile import *
import pygame

pygame.init()
H_SIZE = 480
W_SIZE = 640
screen = pygame.display.set_mode((W_SIZE, H_SIZE), 0, 32)
pygame.display.set_caption("Flashlight 0.1")

start = Start(0,1)
start.show(screen)

end = End(4,5)
end.show(screen)

box = Box(10,2)
box.show(screen)

player = Player(8,6)
player.show(screen)

pygame.display.update()
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            exit()