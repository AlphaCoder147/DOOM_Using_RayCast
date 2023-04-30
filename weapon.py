from sprite_obj import *
class weapon(AnimatedSprite):
    def __init__(self, game, path = 'resources/sprites/weapon/shotgun/0.png', scale = 0.36, animation_time = 110):
        super().__init__(game = game, path = path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_imgs = len(self.images)
        self.framecntr = 0
        self.damage = 50
    
    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.framecntr += 1
                if self.framecntr == self.num_imgs:
                    self.reloading = False
                    self.framecntr = 0
                    
        
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
    
    def update(self):
        self.check_animation_time()
        self.animate_shot()
                