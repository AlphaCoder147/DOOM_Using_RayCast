from sprite_obj import *
from random import randint, random, choice
from math import *

class NPC(AnimatedSprite):
    def __init__(
        self, game, path='resources/sprites/npc/soldier/0.png', pos =(10.5, 5.5),scale = 0.6, 
        shift = 0.38, animation_time = 180
    ):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_imgs = self.get_images(self.path + '/attack')
        self.death_imgs = self.get_images(self.path + '/death')
        self.idle_imgs = self.get_images(self.path + '/idle')
        self.pain_imgs = self.get_images(self.path + '/pain')
        self.walk_imgs = self.get_images(self.path + '/walk')
        
        self.attack_dist = randint(3,6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.atrack_dmg = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_cnt = 0
        self.player_search_trigger = False
        
    def update(self):
        self.check_animation_time()
        self.get_sprite()   
        self.run_logic()
        #self.draw_raycast()
        
    def check_walls(self, x, y):
        return(x,y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):     
        if self.check_walls(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_walls(int(self.x),int(self.y + dy * self.size)):
            self.y += dy      
    
    def move_npc(self):
        next_pos = self.game.pathfinder.get_path(self.map_pos, self.game.player.map_pos)
        nextX, nextY = next_pos
        #pg.draw.rect(self.game.screen, 'blue', (100 * nextX, 100 * nextY, 100))
        if next_pos not in self.game.obj_handler.npc_positions:
            angle = atan2(nextY + 0.5 - self.y, nextX + 0.5 - self.x)
            dx = cos(angle) * self.speed
            dy = sin(angle) * self.speed
            self.check_wall_collision(dx, dy)
    
    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()    
            
    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_cnt < len(self.death_imgs) - 1:
                self.death_imgs.rotate(-1)
                self.image = self.death_imgs[0]
                self.frame_cnt += 1
    
    def animate_pain(self):
        self.animate(self.pain_imgs)
        if self.animation_trigger:
            self.pain = False
            
    def check_npc_hit(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()
    
    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()            
        
    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_npc_hit()
            
            if self.pain:
                self.animate_pain()
            elif self.ray_cast_value:
                self.player_search_trigger = True
                if self.dist < self.attack_dist:
                    self.animate(self.attack_imgs)
                    self.attack()
                else:
                    self.animate(self.walk_imgs)
                    self.move_npc 
            elif self.player_search_trigger:
                self.animate(self.walk_imgs)
                self.move_npc        
            else:    
                self.animate(self.idle_imgs)
        else:
            self.animate_death()        
                
                
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def ray_cast_player_npc(self):
        if self.player.map_pos == self.map_pos:
            return True
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle =self.theta
        
        sinA = sin(ray_angle)
        cosA = cos(ray_angle)
        
        Yhor, dy = (y_map + 1,1) if sinA > 0 else (y_map - 1e-6, -1)
        
        depth_hor = (Yhor - oy) / sinA
        Xhor = ox + depth_hor * cosA
        
        delta_depth = dy / sinA
        dx = delta_depth * cosA
        
        for i in range(MAX_DEPTH):
            tile_hor = int(Xhor), int(Yhor)
            if tile_hor == self.map_pos:
                player_dist_h == depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
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
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            Xvert+=dx
            Yvert += dy
            depth_vert += delta_depth 
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_h, wall_dist_v)    
        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def draw_raycast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)
        
        