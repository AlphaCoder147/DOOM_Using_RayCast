import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_texture = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        
        
    def draw(self):
        self.draw_bg()
        self.render_game_objs()
    
    def player_damage(self):
        self.screen.blit(self.blood_screen, (0,0))
    
    def draw_bg(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_texture, (-self.sky_offset, 0))
        self.screen.blit(self.sky_texture, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))    
    def render_game_objs(self):
        list_objs = sorted(self.game.raycast.objs_to_render, key = lambda t: t[0], reverse = True)
        for depth, image, pos in list_objs:
            self.screen.blit(image, pos)
        
        
    @staticmethod
    def get_texture(path, res = (TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()       
        return pg.transform.scale(texture, res)        
    def load_wall_textures(self):
        return{
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),                        
        }
        