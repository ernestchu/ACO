import pygame as pg
import random
import numpy as np
from scipy.ndimage import center_of_mass

step = 10
wait = 80
world_size = 800
num_ants = 1000
decay_rate = 0.4

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
            def centroid(matrix):
                '''
                find the center of mass of the matrix
                return coordinate(x, y)
                '''
                x_mean = matrix.mean(axis=0)
                y_mean = matrix.mean(axis=1)
                if x_mean.sum() == 0:
                    return None
                x_range = np.arange(matrix.shape[0])
                y_range = np.arange(matrix.shape[1])
                c_x = np.average(x_range, weights=y_mean)
                c_y = np.average(y_range, weights=x_mean)
                return (c_x, c_y)
            if pheromone.table.all == 0:
                c = None
            else:
                c = center_of_mass(pheromone.table)
                print(c)


        if self.status == 'finding':
            '''encourage ants to move out of their nest'''
            possible_cord = []
            x, y = self.rect.center
            [possible_cord.append(cord) for i in map(lambda z: [(x+z, y+c) for c in (-1*step,0,step)], (-1*step,0,step)) for cord in i]
            possible_cord.remove((x, y))
            # x = [cord[0] for cord in possible_cord]
            # y = [cord[0] for cord in possible_cord]
            pheromone_affinity(possible_cord, pheromone)
            choice = random.choice(possible_cord)
            self.rect.center = choice
            self.route.append(self.rect.center)
            if self.rect.center[0]>=800 or self.rect.center[0]<0 or self.rect.center[1]>=800 or self.rect.center[1] < 0:
                self.kill()
                return
        elif self.status == 'found':
            try:
                self.rect.center = self.route.pop()
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
                sum[x-1:x+2, y-1:y+2] += 1/ant.tour_len*gaussian_kernel
        τ = (1-ρ)*τ + ρ*sum/num_ants
        self.table = τ
