import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame import mixer
from Game.constant import *
import time
import random
import math

'''
This class handles the player any most things invlived the the player
'''
class Player():
   
    #Transform
    position = pygame.Vector2()
    scale = pygame.Vector2()

    #Physics
    velocity_y = 0
    gravity_scale = 2000
    jump_force = 5000
    speed = 400
    is_grounded = False

    #Graphics
    player_sprite = 0
    rotation = 0
    rot_speed = 400
    scale_speed = 3
    player_collider = 0

    def __init__(self, desired_scale_x, desired_scale_y, Width, Height):
        self.scale.x = desired_scale_x
        self.scale.y = desired_scale_y

        self.scalar = 100

        self.player_sprite = pygame.sprite.Sprite()
        self.player_sprite.image = pygame.image.load("Actor/Position.png").convert_alpha()
        self.player_sprite.rect = self.player_sprite.image.get_rect()
        self.player_sprite.image = pygame.transform.scale(self.player_sprite.image, (int(self.scale.x), int(self.scale.y)))

        self.position.x = Width / 2
        self.position.y = Height / 2 

        self.scalar = self.scale.x

    def move(self, keys, dt):

        if(keys[0]):
            self.position.x -= 0.01 * dt * self.speed
            self.rotation += 0.01 * dt * self.rot_speed
        if(keys[1]):
            self.position.x += 0.01 * dt * self.speed
            self.rotation -= 0.01 * dt * self.rot_speed
        if(keys[2] and self.is_grounded):
            self.velocity_y -= 0.01 * dt * self.jump_force

        self.velocity_y += 0.00001 * dt * self.gravity_scale

        self.position.y += self.velocity_y * dt

        self.player_sprite.rect.topleft = self.position.x, self.position.y

    def draw(self, screen, color, dt, colliders):
        img_copy = pygame.transform.scale(self.player_sprite.image, (int(self.scalar), int(self.scalar)))
        img_copy = pygame.transform.rotate(img_copy, self.rotation)
        self.collisions(colliders, img_copy.get_height())
        screen.blit(img_copy, (self.position.x - int(img_copy.get_width() / 2), self.position.y - int(img_copy.get_height() / 2)))
        
    def collisions(self, colliders, scale):
        #Top of box
        self.is_grounded = False
        for i in range(len(colliders)):
            if(self.position.y - int(scale / 2) >= colliders[i].top - scale and colliders[i].typeof == "environment"):
                self.is_grounded = True
                self.position.y = colliders[i].top - int(scale / 2) + 5
                self.velocity_y  = 0
            if(self.position.x + int(self.player_sprite.image.get_width() / 2) >= 720):
                self.position.x = 720 - int(self.player_sprite.image.get_width() / 2)
            if(self.position.x - int(self.player_sprite.image.get_width() / 2) <= 0):
                self.position.x = 0 + int(self.player_sprite.image.get_width() / 2)
