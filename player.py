from settings import *
import pygame as py
from math import *
 
class Player:
    def __init__(self,game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANG
        
    def move(self):
        sinA = sin(self.angle)
        cosA = cos(self.angle)
        dx, dy, = 0,0
        speed = PLAYER_SP * self.game.delta_time
        speedSin = speed * sinA
        speedCos = speed * cosA
        
        keys = py.key.get_pressed()
        if keys[py.K_w]:
            dx += speedCos
            dy += speedSin          
        if keys[py.K_s]:
            dx += -speedCos
            dy += -speedSin  
        if keys[py.K_a]:
            dx += -speedCos
            dy += speedSin  
        if keys[py.K_d]:
            dx += speedCos
            dy += -speedSin
            
        self.check_wall_collision(dx, dy)
        if keys[py.K_LEFT]:
            self.angle -= PLAYER_ROT * self.game.delta_time
        if keys[py.K_RIGHT]:
            self.angle += PLAYER_ROT * self.game.delta_time
        self.angle %= tau    
          
    def check_walls(self, x, y):
        return(x,y) not in self.game.map.world_map
    def check_wall_collision(self, dx, dy):
        if self.check_walls(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_walls(int(self.x),int(self.y + dy)):
            self.y += dy      
    def draw(self):
        #py.draw.line(self.game.screen, 'red', (self.x * 75, self.y * 75),
         #            (self.x * 75 + WIDTH * cos(self.angle),
          #            self.y * 75 + WIDTH * sin(self.angle)),2)
        py.draw.circle(self.game.screen, 'green', (self.x * 75, self.y * 75),15)
    
    def update(self):
        self.move()
    
    @property
    def pos(self):
        return self.x, self.y
    @property
    def map_pos(self):
        return int(self.x), int(self.y)        
         