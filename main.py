import pygame
from pygame.locals import *
from pygame.math import Vector2
from Game.constant import *
from Game.Bottom import *
from Game.Spawner import *
from Game.Player import *
from Game.Particle import *
import time
import math


game_state = 0
score = 0
score_int = 0
max_score = 0

entities_alive = []



'''
THis is the main class for the game
'''
class Main():
    global game_state
    previous_frame_time = 0
    dt = 0
    elapsed_time = 0
    time_between_spawns = 100
    
    def calculate_deltatime(self):
        self.dt = time.time() - self.previous_frame_time
        self.dt *= 60
        self.previous_frame_time = time.time()

    def difficulty(self):
        self.elapsed_time += self.dt
        if(self.elapsed_time > 1000):
            self.time_between_spawns /= 1.45
            self.elapsed_time = 0

    def handle_inputs(self, keys, event):
        if(event.type == pygame.KEYDOWN):
            if(event.key == K_a):
                keys[0] = True
            if(event.key == K_d):
                keys[1] = True
            if(event.key == K_w):
                keys[2] = True
        if(event.type == pygame.KEYUP):
            if(event.key == K_a):
                keys[0] = False
            if(event.key == K_d):
                keys[1] = False
            if(event.key == K_w):
                keys[2] = False
    
    def setup_pygame(self, title, width, height):
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        favicon = pygame.image.load("Actor/Favcon .png").convert_alpha()
        pygame.display.set_icon(favicon)
        pygame.init()
        return screen

    def update_score(self, screen, text):
        global score_int
        global score
        score += self.dt / 100
        score_int = int(score)
        score_text = text.render("Energy Level: " + str(score_int),True,(0,0,255))
        screen.blit(score_text, (10, 10))

    def draw_colliders(self, colliders, screen, color, width, height):
        for i in range(len(colliders)):
            colliders[i].draw(screen, color, width, height)

    def reset_state(self):
        self.previous_frame_time = 0
        self.dt = 0
        self.elapsed_time = 0
        self.time_between_spawns = 100
        self.score_int = 0
        

    def game(self, screen, font, WIDTH, HEIGHT):
        global game_state
        
        self.previous_frame_time = time.time()
        #       A      D      Space
        keys = [False, False, False]

        player = Player(40, 40, WIDTH, HEIGHT)

        colliders = []

        #Constant Sprites
        foreground = pygame.sprite.Sprite()
        foreground.image = pygame.image.load("Actor/Background2.png").convert_alpha()
        foreground.rect = foreground.image.get_rect()
        foreground.rect.topleft = 0, HEIGHT - 480
        foreground.image = pygame.transform.scale(foreground.image, (720, 480))
        foreground_collider = Box_Collider(WIDTH / 2, HEIGHT - 20, 720, 120, "environment")

        colliders.append(foreground_collider)

        spawner = Spawner(screen)

        particles = []

        time_elapsed = 0

        while(game_state == 1):
            screen.fill(WHITE)
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    game_state = 2
                self.handle_inputs(keys, event)
            self.difficulty()
            self.calculate_deltatime()

            screen.blit(foreground.image, foreground.rect)
            
            time_elapsed += self.dt
            
            if(time_elapsed > 10):
                part = Particle()
                particles.append(part)
                time_elapsed = 0
            for i in range(len(particles)):
                try:
                    particles[i].move(self.dt)
                    particles[i].draw(screen)
                    particles[i].collision(particles)
                except:
                    pass

            player.move(keys, self.dt)
            player.draw(screen, BLACK, self.dt, colliders)

            spawner.spawner()
            spawner.set_time_between_spawns(self.time_between_spawns)
            spawner.timer(self.dt)
            spawner.draw_enemies(self.dt)
            spawner.check_for_player(player, player.scalar)


            self.update_score(screen, font)

            pygame.display.update()

    def menu(self, screen, font, WIDTH, HEIGHT):
        global game_state

        sound = pygame.mixer.Sound("Actor/Sound/Start.wav")
        play_text = font.render("PLAY", True, (255,255,255))
        play_text_y_offset = 0

        score_text = font.render("HIGH SCORE: " + str(int(max_score)), True, (255,255,255))

        while game_state == 0:
            screen.fill(Tan)
            screen.blit(play_text, (WIDTH/2 - play_text.get_width() / 2, HEIGHT/2 - play_text.get_height() / 2 + play_text_y_offset))
            screen.blit(score_text, (WIDTH/2 - score_text.get_width() / 2, HEIGHT/2 - score_text.get_height() / 2 + 150))
            play_text_y_offset = math.sin(time.time() * 5) * 5 - 25
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    game_state = 2
                if(pygame.mouse.get_pos()[0] < WIDTH/2 + play_text.get_width() / 2 and pygame.mouse.get_pos()[0] > WIDTH/2 - play_text.get_width() / 2):
                    if(pygame.mouse.get_pos()[1] < HEIGHT/2 + play_text.get_height() / 2 + play_text_y_offset and pygame.mouse.get_pos()[1] > HEIGHT/2 - play_text.get_height() / 2 + play_text_y_offset):
                        if(event.type == pygame.MOUSEBUTTONDOWN):
                            game_state = 1
                            sound.play()
            pygame.display.update()
                       
    def __init__(self):
        global game_state
        global score 
        global score_int
        global entities_alive 
        
        while game_state != 2:

            screen = self.setup_pygame("Falling Particles", WIDTH, HEIGHT)
            font = pygame.font.Font("Actor/Inter.ttf", 32)
            
            if(game_state == 0):
                self.menu(screen, font, WIDTH, HEIGHT)
            if(game_state == 1):
                self.previous_frame_time = time.time()
                self.game(screen, font, WIDTH, HEIGHT)
            
            sound = pygame.mixer.Sound("Actor/Sound/Die.wav")
            sound.play()
            self.reset_state()
            score = 0
            score_int = 0
            entities_alive.clear()
            entities_alive = []
            
game = Main()