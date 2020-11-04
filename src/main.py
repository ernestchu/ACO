import sys
import objects
import pygame as pg
import random
from pygame.locals import QUIT

def initialize(num_ant, *args):
    '''
    num_ant: int
    args: pg.sprite.Group[]
    '''
    for i in range(num_ant):
        args[0].add(objects.Ant((random.randrange(0, 800), random.randrange(0, 800)), "scout"))
    args[1].add(objects.Food((random.randrange(0, 800), random.randrange(0, 800)), 50))
    args[2].add(objects.Nest((random.randrange(0, 800), random.randrange(0, 800)), 50))


pg.init()
surface = pg.display.set_mode((800, 800))
pg.display.set_caption('ACO Simulator')
background = objects.image.bkg
background.convert()
surface.blit(background, (0, 0))
pg.display.update()


ants = pg.sprite.Group()
foods = pg.sprite.Group()
nests = pg.sprite.Group()
initialize(100, ants, foods, nests)
ants.draw(surface)
foods.draw(surface)
nests.draw(surface)
pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    ants.update()
    ants.clear(surface, background)
    ants.draw(surface)
    foods.draw(surface)
    nests.draw(surface)
    pg.display.update()
