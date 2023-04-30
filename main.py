import pygame
import sys
from settings import *
from map import *
from player import *
from raycast import *
from obj_render import *
from sprite_obj import *
from obj_handler import *
from weapon import *
from sound import *
from pathfinder import *

class Game:
    def __init__(self):  
        pygame.init()
        pg.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new()
        
    def new(self):
        self.map = Map(self)
        self.player = Player(self)
        self.obj_render = ObjectRenderer(self)
        self.raycast = RayCasting(self)
        self.Objhandler = Objhandler(self)
        self.weapon = weapon(self)
        self.sound = Sound(self)
        self.pathfinder = Pathfinder(self)
        
    def update(self):
        self.player.update()
        self.raycast.update()
        self.Objhandler.update()
        self.weapon.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
    def draw(self):
        #self.screen.fill('black')
        self.obj_render.draw()
        self.weapon.draw()
        #self.map.draw()
        #self.player.draw()
        
    def check_event(self):
        self.global_trigger = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
                    
            self.player.single_fire_event(event)
    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()            
            
if __name__ == '__main__':
    game = Game()
    game.run()
                