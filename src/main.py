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
    nest_x, nest_y = random.randrange(0, 800), random.randrange(0, 800)
    for i in range(num_ant):
        args[0].add(objects.Ant((nest_x, nest_y), "scout"))
    args[1].add(objects.Food((random.randrange(0, 800), random.randrange(0, 800)), 50))
    args[2].add(objects.Nest((nest_x, nest_y), 50))


pg.init()
start = True
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
        elif event.type == pg.KEYDOWN: #press blankspace to start/pause
            if event.key == pg.K_SPACE:
                 start = not start
    if start:
        ants.update()
        ants.clear(surface, background)
        ants.draw(surface)
        foods.draw(surface)
        nests.draw(surface)
        pg.display.update()
