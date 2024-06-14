from render import *
from Square import Hitbox
from vector import Vector
import math

class Arrow(Hitbox):
    def __init__(self, center, width, height, color):
        super().__init__(center, width, height, color)
        self.images = arrow_images
        self.arrow_velocity = 2
        self.arrow_angle = 0
        self.arrow_angle = 0
        self.spread = 1
        # self.direction = Vector((1, 0))
        self.to_render = Render(self.images, center, self.arrow_angle, 1)

    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y

    def render(self, surface):
        self.to_render.render_stack(surface)


    def handle_rotation_arrow(self, rotation_input):
        self.handle_rotation(rotation_input)

        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.arrow_angle -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.arrow_angle += self.rotationspeed





    def update(self, rotation_input, direction):
        self.to_render.loc = [self.center.x, self.center.y]
        self.handle_rotation_arrow(rotation_input)
        self.move(Vector((math.cos(self.arrow_angle), math.sin(self.arrow_angle))))
        self.move(direction * -1)
        self.to_render.angle = -self.arrow_angle * 180 / math.pi


