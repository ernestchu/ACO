import sys
import numpy as np
import objects
import pygame as pg
import random
from pygame.locals import QUIT

def initialize(num_ant, *args):
    '''
    num_ant: int
    args: pg.sprite.Group[]
    '''
    nest_x, nest_y = objects.world_size/2, objects.world_size/2
    for i in range(num_ant):
        args[0].add(objects.Ant((nest_x, nest_y), "finding"))
    args[1].add(objects.Food((random.randrange(0, objects.world_size), random.randrange(0, objects.world_size)), 50))
    args[2].add(objects.Nest((nest_x, nest_y), 50))

def draw_pheromone(pheromone, surface, color):
    table = pheromone.table
    #normalizing
    intensity = (table-table.min())/table.max()-table.min()
    intensity = intensity*255
    #choose only half of them to draw
    x, y = np.where(intensity >= 127.5)
    for i, j in zip(x, y):
        #expand from (128-255) to (0-255)
        opacity = intensity[i, j]*2-255
        sub_surf = pg.Surface(pg.Rect(i, j, objects.step, objects.step).size, pg.SRCALPHA)
        r, g, b = color
        pg.draw.rect(sub_surf, (r, g, b, opacity), sub_surf.get_rect())
        # surface.blit(sub_surf, (i, j, objects.step, objects.step))
        surface.blit(sub_surf, (i, j, objects.step, objects.step))

pg.init()
start = True
surface = pg.display.set_mode((objects.world_size, objects.world_size))
pg.display.set_caption('ACO Simulator')
background = objects.image.bkg
background.convert()
surface.blit(background, (0, 0))
pg.display.update()


ants = pg.sprite.Group()
foods = pg.sprite.Group()
nests = pg.sprite.Group()
obstacles = pg.sprite.Group()
pheromone_food = objects.Pheromone()
pheromone_nest = objects.Pheromone()
initialize(objects.num_ants, ants, foods, nests)
foods.draw(surface)
ants.draw(surface)
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
        elif event.type == pg.MOUSEBUTTONDOWN:
            obstacles.add(objects.Obstacle(event.pos, 50))
        elif event.type == pg.MOUSEMOTION:
            if event.buttons[0] == 1:
                obstacles.add(objects.Obstacle(event.pos, 50))
    if start:
        surface.blit(background, (0, 0))
        ants.update(foods, nests, pheromone_food, pheromone_nest, obstacles)
        pheromone_food.update(ants, 'found')
        pheromone_nest.update(ants, 'finding')
        ants.clear(surface, background)
        draw_pheromone(pheromone_food, surface, (0, 255, 0))
        draw_pheromone(pheromone_nest, surface, (255, 0, 0))
        foods.draw(surface)
        ants.draw(surface)
        nests.draw(surface)
        obstacles.draw(surface)
        pg.display.update()
        pg.time.wait(objects.wait)
