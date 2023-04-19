import pygame
import sys
from settings import *
from map import *
from player import *
from raycast import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new()
        
    def new(self):
        self.map = Map(self)
        self.player = Player(self)
        self.raycast = RayCasting(self)
    def update(self):
        self.player.update()
        self.raycast.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
    def draw(self):
        self.screen.fill('Black')
        #self.map.draw()
        #self.player.draw()
        
    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()            
            
if __name__ == '__main__':
    game = Game()
    game.run()
                