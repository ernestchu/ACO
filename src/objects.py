import pygame as pg
import random

step = 15
wait = 80
world_size = 800
num_ants = 100

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
            except IndexError:
                self.status == 'finding'

        for food in foods:
            if pg.sprite.collide_rect(self, food):
                self.image = image.ant_with_food
                self.status = 'found'


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
        self.table = [[0]*world_size for _ in range(world_size)]
        self.table[500][500] = 5
