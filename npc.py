from sprite_obj import *
from random import randint, random, choice

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
        
    def update(self):
        self.check_animation_time()
        self.get_sprite()   