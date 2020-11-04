import sys
import objects
import pygame as pg
import random
from pygame.locals import QUIT

def initialize(ants, num_ant=100):
    '''
    ants: pg.sprite.Group
    num_ant: int
    '''
    for i in range(num_ant):
        ants.add(objects.Ant((random.randrange(0, 800), random.randrange(0, 800)), "scout"))



pg.init()
surface = pg.display.set_mode((800, 800))
pg.display.set_caption('ACO Simulator')
background = objects.image.bkg
background.convert()
surface.blit(background, (0, 0))
pg.display.update()


ants = pg.sprite.Group()
initialize(ants)
ants.draw(surface)
pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    ants.update()
    ants.clear(surface, background)
    ants.draw(surface)
    pg.display.update()
