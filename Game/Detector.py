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
This is another Entity that when you coled with them you die
'''
class Detector(Entity):
    def __init__(self):
        self.speed = random.randrange(1, 5)
        self.position = Vector2()
        self.position.x = random.randrange(0, 720)
        self.position.y = 0

        self.initialiser((0, 220, 220),"Actor/Sound/ElectronOrDectetorHit.wav")

        self.tag = "enemy"

        self.radius = random.randrange(10, 30)