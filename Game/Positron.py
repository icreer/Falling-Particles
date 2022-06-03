import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame import mixer
from Game.constant import *
from Game.Entity import *
import time
import random
import math

'''
    This is the Class that deals with the Possitrion that help you grow
'''
class Positron(Entity):
    def __init__(self):
        self.speed = random.randrange(1, 5)
        self.position = Vector2()
        self.position.x = random.randrange(0, 720)
        self.position.y = 0
        self.initialiser((255, 255, 0),"Actor/Sound/Protron_hit.wav")
        self.tag = "positron"

        self.radius = random.randrange(10, 30)