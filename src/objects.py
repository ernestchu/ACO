import pygame as pg
import random
import numpy as np

step = 10
wait = 0
world_size = 800
num_ants = 1000
decay_rate = 0.05
penalty_away_food = 100000

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
        self.tour_len = 1e10
    def update(self, foods, pheromone):
        def pheromone_affinity(possible_cord, pheromone):
            if pheromone.centroid:
                p = np.array(possible_cord)
                return 1/np.abs(p-pheromone.centroid).sum(axis=1)
            else:
                return [1]*8
        if self.status == 'finding':
            '''encourage ants to move out of their nest'''
            possible_cord = []
            x, y = self.rect.center
            [possible_cord.append(cord) for i in map(lambda z: [(x+z, y+c) for c in (-1*step,0,step)], (-1*step,0,step)) for cord in i]
            possible_cord.remove((x, y))
            choice = random.choices(possible_cord, weights=pheromone_affinity(possible_cord, pheromone))
            self.rect.center = choice[0]
            self.route.append(self.rect.center)
            if self.rect.center[0]>=800 or self.rect.center[0]<0 or self.rect.center[1]>=800 or self.rect.center[1] < 0:
                self.kill()
                return
        elif self.status == 'found':
            try:
                self.rect.center = self.route.pop()
                self.tour_len += (1/self.tour_len)*penalty_away_food
            except IndexError: #returned nest
                self.image = image.ant
                self.status == 'finding'
                self.tour_len = 1e10

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
        self.centroid = None
    def update(self, ants):
        τ, ρ, sum = self.table, decay_rate, np.zeros((world_size, world_size))
        gaussian_kernel = np.array([
        [0.045, 0.122, 0.045],
        [0.122, 0.332, 0.122],
        [0.045, 0.122, 0.045]
        ])
        for ant in ants:
            if ant.status == 'found':
                x, y = ant.rect.center
                # sum[x-1:x+2, y-1:y+2] += 1/ant.tour_len*gaussian_kernel
                sum[x, y] += 1/ant.tour_len
        τ = (1-ρ)*τ + ρ*sum/num_ants
        self.table = τ
        self.update_centroid()
    def update_centroid(self):
        '''
        find the center of mass of the table
        '''
        x_mean = self.table.mean(axis=0)
        y_mean = self.table.mean(axis=1)
        if x_mean.sum() == 0:
            return None
        x_range = np.arange(self.table.shape[0])
        y_range = np.arange(self.table.shape[1])
        c_x = np.average(x_range, weights=y_mean)
        c_y = np.average(y_range, weights=x_mean)
        self.centroid = (c_x, c_y)
