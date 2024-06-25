from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar

class Tile(Hitbox):
    def __init__(self, center, width, height, color, images, type="land"):
        super().__init__(center, width, height, color)
        self.type = type
        if type == "water":
            self.images = [img.convert_alpha() for img in images]
        else:
            self.images = images.convert_alpha()
        self.to_render = Render(self.images, center, self.angle)

    def render(self, surf):
        self.to_render.render_single(surf)


    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

