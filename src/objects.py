import pygame as pg
import random
import numpy as np

step = 15
wait = 80
world_size = 800
num_ants = 1000
decay_rate = 0.8

class image:
    ant = pg.transform.scale(pg.image.load('images/ant.png'), (20, 20))
    ant_with_food = pg.transform.scale(pg.image.load('images/ant_with_food.png'), (20, 20))
    food = pg.image.load('images/food.png')
    nest = pg.image.load('images/nest.png')
    obstacle = pg.image.load('images/obstacle.png')
    bkg = pg.transform.scale(pg.image.load('images/bkg.png'), (800, 800))

class Ant(pg.sprite.Sprite):
    '''
    Object Ant is an ant.
    '''
    def __init__(self, position, status):
        super().__init__()
        self.image = image.ant
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.status = status
        self.route = [self.rect.center]
        self.tour_len = 0
    def update(self, foods):
        if self.status == 'finding':
            '''encourage ants to move out of their nest'''
            possible_cord = []
            [possible_cord.append(cord) for i in map(lambda x: [(x, c) for c in (-1*step,0,step)], (-1*step,0,step)) for cord in i]
            possible_cord.remove((0, 0))
            x, y = self.rect.center
            choice = random.choice(possible_cord)
            x += choice[0]
            y += choice[1]
            self.rect.center = (x, y)
            self.route.append(self.rect.center)
        elif self.status == 'found':
            try:
                self.rect.center = self.route.pop()
            except IndexError: #returned nest
                self.status == 'finding'
                self.tour_len = 0

        for food in foods:
            if pg.sprite.collide_rect(self, food):
                self.image = image.ant_with_food
                self.status = 'found'
                self.tour_len = len(self.route)

class Food(pg.sprite.Sprite):
    '''
    Object Food is food with different amount and size(based on amount).
    '''
    def __init__(self, position, size):
        super().__init__()
        self.image = pg.transform.scale(image.food, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.size = size



class Nest(pg.sprite.Sprite):
    '''
    Object Nest is a nest of ants'. Nest if full of food?
    '''
    def __init__(self, position, size):
        super().__init__()
        self.image = pg.transform.scale(image.nest, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.size = size

class Obstacle(pg.sprite.Sprite):
    '''
    Object Obstable is a obstable. Don't hit it!!
    '''
    def __init__(self, position, size):
        super().__init__()
        self.image = obstacle.ant
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.size = size

class Pheromone:
    def __init__(self):
        self.table = np.zeros((world_size, world_size))
    def update(self, ants):
        τ, ρ, sum = self.table, decay_rate, np.zeros((world_size, world_size))
        for ant in ants:
            if ant.status == 'found':
                x, y = ant.rect.center
                sum[x][y] += 1/ant.tour_len
        τ = (1-ρ)*τ + ρ*sum/num_ants
        self.table = τ
        # for x in range(world_size):
        #     for y in range(world_size):
        #         τ, ρ, sum = self.table[x][y], decay_rate, 0
        #         # for ant in ants:
        #         #     if ant.rect.center == (x, y) and ant.status == 'found':
        #         #         sum += 1/ant.tour_len
        #         #     else:
        #         #         continue
        #         τ = (1-ρ)*τ + ρ*sum
        #         ###Pheromone Decay Formula###
        #         self.table[x][y] = τ
        #         #############################


        # x, y = ant.rect.center
        # try:
        #     τ, ρ = self.table[x][y], decay_rate
        # except IndexError: #ant ran out of the world
        #     ant.kill()
        #     return
        # try: #found
        #     L = 1/ant.tour_len
        # except ZeroDivisionError: #still finding
        #     L = 0
        # ###########Pheromone Decay Formula##############
        # τ = (1-ρ)*τ + ρ*(L)/num_ants
        # ################################################
        # self.table[x][y] = τ
        # if self.table[x][y] > 255:
        #     self.table[x][y] = 255
