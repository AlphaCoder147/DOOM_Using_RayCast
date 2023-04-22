import pygame as py
from math import *
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.object_to_render = []
        self.textures = self.game.obj_render.wall_textures
    
    def get_objects_to_render(self):
        self.objs_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                wall_column = py.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset*(TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = py.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)
                
            self.objs_to_render.append((depth, wall_column, wall_pos))
                 
    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        texture_vert, texture_hor = 1 , 1
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
                    texture_hor = self.game.map.world_map[tile_hor]
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
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                Xvert+=dx
                Yvert += dy
                depth_vert += delta_depth    
                
                
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                Yvert %= 1
                offset = Yvert if cosA > 1 else(1-Yvert)
            else:
                depth, texture = depth_hor, texture_hor   
                Xhor %= 1
                offset = (1 - Xhor) if sinA > 0 else Xhor     
                     
            depth *= cos(self.game.player.angle - ray_angle)         
            proj_height = SCREEN_DIST / (depth + 0.0001)
            self.ray_casting_result.append((depth, proj_height, texture, offset))            
            ray_angle += DELTA_ANGLE
    
    
    def update(self):
        self.ray_cast()    
        self.get_objects_to_render()