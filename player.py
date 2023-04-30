from settings import *
import pygame as pg
from math import *
 
class Player:
    def __init__(self,game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANG
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
    
    def get_damage(self, damage):
        self.health -= damage
        self.game.obj_render.player_damage()
        self.game.sound.player_pain.play()    
    
    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True
                
        
    def move(self):
        sinA = sin(self.angle)
        cosA = cos(self.angle)
        dx, dy, = 0,0
        speed = PLAYER_SP * self.game.delta_time
        speedSin = speed * sinA
        speedCos = speed * cosA
        
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speedCos
            dy += speedSin          
        if keys[pg.K_s]:
            dx += -speedCos
            dy += -speedSin  
        if keys[pg.K_a]:
            dx += speedSin
            dy += -speedCos  
        if keys[pg.K_d]:
            dx += -speedSin
            dy += speedCos
            
        self.check_wall_collision(dx, dy)
        #if keys[pg.K_LEFT]:
         #   self.angle -= PLAYER_ROT * self.game.delta_time
        #if keys[pg.K_RIGHT]:
        #    self.angle += PLAYER_ROT * self.game.delta_time
        self.angle %= tau    
          
    def check_walls(self, x, y):
        return(x,y) not in self.game.map.world_map
    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        
        if self.check_walls(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_walls(int(self.x),int(self.y + dy * scale)):
            self.y += dy      
    def draw(self):
        #py.draw.line(self.game.screen, 'red', (self.x * 75, self.y * 75),
         #            (self.x * 75 + WIDTH * cos(self.angle),
          #            self.y * 75 + WIDTH * sin(self.angle)),2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 75, self.y * 75),15)
    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENS * self.game.delta_time    
    
    def update(self):
        self.move()
        self.mouse_control()
    
    @property
    def pos(self):
        return self.x, self.y
    @property
    def map_pos(self):
        return int(self.x), int(self.y)        
         