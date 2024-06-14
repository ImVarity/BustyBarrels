from render import *
from Square import Hitbox
from vector import Vector
import math

class Barrel(Hitbox):
    def __init__(self, center, width, height, color):
        super().__init__(center, width, height, color)
        self.images = barrel_images
        self.spread = 1
        self.to_render = Render(self.images, center, self.angle, 1.2)
    
    def render(self, surface):
        self.to_render.render_stack(surface)


    def update(self, rotation_input, direction):
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle
        self.handle_rotation(rotation_input)
        self.move(direction * -1)