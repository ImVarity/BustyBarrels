from render import *
from Square import Hitbox
from vector import Vector
import math

class Player(Hitbox):
    def __init__(self, center, width, height, color):
        super().__init__(center, width, height, color)
        self.images = player_images
        self.spread = 1
        # self.direction = Vector((0, 0))
        self.to_render = Render(self.images, center, self.angle, self.spread)


    def render(self, surface):
        self.to_render.render_stack(surface)


    def update(self, rotation_input): # order matters here so images dont move first
        self.handle_rotation(rotation_input, player=True)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle