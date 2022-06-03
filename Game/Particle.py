import pygame
import random

import pygame
from pygame.locals import *
from pygame.math import Vector2

from Game.constant import *

import random


'''
THis class createds the back ground particles 
'''
class Particle():
    def __init__(self):
        self.position = Vector2()
        self.position.x = random.randrange(0, 720)
        self.position.y = 0
        self.size = random.randrange(0, 10)
        self.red = random.randrange(200,255)
        self.green = random.randrange(200,255)
        self.blue = random.randrange(200,255)

        self.color = (self.red, self.green, self.blue)
        self.speed = random.randrange(20, 50)

    def move(self, dt):
        self.position.y += 0.01 * dt * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen,self.color,(self.position.x,self.position.y), self.size)
    
    def collision(self, particles):
        if(self.position.y > 390):
            particles.remove(self)