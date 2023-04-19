import pygame as py
from math import *
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sinA = sin(ray_angle)
            cosA = cos(ray_angle)
            
            Yhor, dy = (y_map + 1,1) if sinA > 0 else (y_map - 1e-6, -1)
            
            depth_hor = (Yhor - oy) / sinA
            Xhor = ox + depth_hor * cosA
            
            delta_depth = dy / sinA
            dx = delta_depth * cosA
            
            for i in range(MAX_DEPTH):
                tile_hor = int(Xhor), int(Yhor)
                if tile_hor in self.game.map.world_map:
                    break
                Xhor += dx
                Yhor += dy 
                depth_hor += delta_depth   
            
            Xvert , dx = (x_map + 1, 1) if cosA > 0 else (x_map - 1e-6, -1)
            depth_vert = (Xvert - ox) / cosA
            Yvert = oy +  depth_vert * sinA
            
            delta_depth = dx / cosA
            dy = delta_depth * sinA            
            
            for i in range(MAX_DEPTH):
                tile_vert = int(Xvert), int(Yvert)
                if tile_vert in self.game.map.world_map:
                    break
                Xvert+=dx
                Yvert += dy
                depth_vert += delta_depth    
                
                
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor        
                     
            depth *= cos(self.game.player.angle - ray_angle)         
            proj_height = SCREEN_DIST / (depth + 0.0001)
            color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            py.draw.rect(self.game.screen, color, 
                         (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))            
            ray_angle += DELTA_ANGLE
    
    
    def update(self):
        self.ray_cast()    
        