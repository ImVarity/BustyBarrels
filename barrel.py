from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
import math

class Barrel(Hitbox):
    def __init__(self, center, width, height, color, health=5):
        super().__init__(center, width, height, color)
        self.images = barrel_images
        self.spread = 1.2
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)
    
    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)



    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

