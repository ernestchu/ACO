import pygame as pg
import random

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
    def __init__(self, position, role):
        super().__init__()
        self.image = image.ant
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.role = role
        self.route = []
    def update(self):
        '''encourage ants to move out of their nest'''
        step = 7
        possible_cord = []
        [possible_cord.append(cord) for i in map(lambda x: [(x, c) for c in (-1*step,0,step)], (-1*step,0,step)) for cord in i]
        possible_cord.remove((0, 0))
        x, y = self.rect.center
        choice = random.choice(possible_cord)
        x += choice[0]
        y += choice[1]
        self.rect.center = (x, y)

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
