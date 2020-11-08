import pygame as pg
import random
import numpy as np
from scipy import stats
from math import floor

step = 10
wait = 20
world_size = 800
num_ants = 100
decay_rate = 0.01
penalty_away = 0.8
smoothness = 0.2

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
        self.velocity = (0, 0)
        self.status = status
        self.penalty = 1
    def update(self, foods, nests, pheromone_food, pheromone_nest, obstacles):
        def pheromone_affinity(possible_cord, pheromone, current):
            if pheromone.centroid:
                p = np.abs((possible_cord+current)-pheromone.centroid).sum(axis=1)
                p = p.max() - p
                return p
            else:
                return np.array([1]*8)
        pheromone_dict = {'finding': pheromone_food, 'found': pheromone_nest}
        '''encourage ants to move out of their nest'''
        possible_cord = []
        x, y = self.rect.center
        [possible_cord.append(cord) for i in map(lambda z: [(z, c) for c in (-1*step,0,step)], (-1*step,0,step)) for cord in i]
        possible_cord.remove((0, 0))
        possible_cord = np.array(possible_cord)
        weights = pheromone_affinity(possible_cord, pheromone_dict[self.status], np.array([x, y]))
        while weights.any()!=0:
            choice = random.choices(possible_cord, weights)
            index = np.where(possible_cord==choice)[0]
            c_x = 0.9*self.velocity[0]+smoothness*choice[0][0]
            c_y = 0.9*self.velocity[1]+smoothness*choice[0][1]
            self.velocity = (c_x, c_y)
            self.rect.center = (x+self.velocity[0], y+self.velocity[1])
            weights[index] = 0
            if not pg.sprite.spritecollideany(self, obstacles):
                break
        if self.rect.center[0]>=800 or self.rect.center[0]<0 or self.rect.center[1]>=800 or self.rect.center[1] < 0:
            self.kill()
            return
            
        self.penalty *= (1-penalty_away)

        if self.status == 'finding':
            for food in foods:
                if pg.sprite.collide_rect(self, food):
                    self.image = image.ant_with_food
                    self.status = 'found'
                    self.penalty = 1
                    self.velocity = (0, 0)
        elif self.status == 'found':
            for nest in nests:
                if pg.sprite.collide_rect(self, nest):
                    self.image = image.ant
                    self.status = 'finding'
                    self.penalty = 1
                    self.velocity = (0, 0)
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
    Object Obstable is a obstacle. Don't hit it!!
    '''
    def __init__(self, position, size):
        super().__init__()
        self.image = pg.transform.scale(image.obstacle, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.size = size

class Pheromone:
    def __init__(self):
        self.table = np.zeros((world_size, world_size))
        self.centroid = None
    def update(self, ants, status):
        def gaussian_kernel(size, sigma):
            x =np.linspace(-sigma, sigma, size+1)
            kernel1d = np.diff(stats.norm.cdf(x))
            kernel2d = np.outer(kernel1d, kernel1d)
            return kernel2d/kernel2d.sum()
        τ, ρ, sum = self.table, decay_rate, np.zeros((world_size, world_size))
        for ant in ants:
            if ant.status == status:
                x, y = ant.rect.center
                try:
                    k = 1
                    sum[x-(k//2)*step:x+(k//2+1)*step, y-(k//2)*step:y+(k//2+1)*step] += gaussian_kernel(k*step, 1)*ant.penalty
                except ValueError:
                    print('border')
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
