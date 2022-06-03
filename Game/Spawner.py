from html import entities
from pygame.locals import *
from pygame.math import Vector2
from pygame import mixer
from Game.constant import *
from Game.Positron import *
from Game.Electron import *
from Game.Detector import *
import random
#from main import entities_alive,game_state

'''
This class deals with spaning entity
'''
class Spawner():
    
    total_enemies_spawned = 0
    time_elapsed = 0
    screen = 0
    time_between_spawns = 100
    concurrent_enemys = 0

    sound = 0

    def __init__(self, screen):
        self.screen = screen
        self.sound = mixer.Sound("Actor/Sound/Background_music.wav")

    def check_for_player(self, player, scalar):
        global game_state
        global score_int
        global score
        global max_score
        global entities_alive
        for i in range(len(entities_alive)):
            try:
                if(entities_alive[i].bottom > 380 + 50 - scalar):
                    if(entities_alive[i].position.x > player.position.x - player.scale.x and entities_alive[i].position.x < player.position.x + player.scale.x):
                        if(entities_alive[i].tag == "enemy"):
                            game_state = 0
                            if(score > max_score):
                                max_score = score
                           
                        else:
                            score += 5
                            player.scalar = 50
                            self.sound.play()
                            entities_alive.remove(entities_alive[i])
            except:
                pass
                        

        
    def set_time_between_spawns(self, time_between_spawns):
        self.time_between_spawns = time_between_spawns
    
    def draw_enemies(self, dt):
        for i in range(len(entities_alive)):
            try:
                entities_alive[i].draw(self.screen)
                entities_alive[i].move(dt)
                entities_alive[i].collisions(entities_alive)
            except:
                pass

    def timer(self, dt):
        self.time_elapsed += dt
    
    def spawner(self):
        if(self.time_elapsed >= self.time_between_spawns):
            random_int = random.randint(0, 4)
            if(random_int == 0 and self.concurrent_enemys < 3):
                entity = Electron()
                self.concurrent_enemys += 1
            elif(random_int == 1 and self.concurrent_enemys < 3):
                entity = Detector()
                self.concurrent_enemys += 1
            else:
                entity = Positron()
                self.concurrent_enemys = 0
            entities_alive.append(entity)

            self.time_elapsed = 0