from render import *
from Square import Hitbox
from vector import Vector
import math

class Arrow(Hitbox):
    def __init__(self, center, width, height, color, looking):
        super().__init__(center, width, height, color)
        self.images = arrow_images
        self.arrow_velocity = 4
        self.arrow_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates arrow to point that direction
        self.set_angle(self.arrow_angle) # sets the direction of all the vertices to face the right way
        self.spread = 1
        self.to_render = Render(self.images, center, self.arrow_angle, self.spread)
        # self.direction = Vector((1, 0))

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
        self.translate(Vector((math.cos(self.arrow_angle), math.sin(self.arrow_angle))) * self.arrow_velocity) # if i want to simulate shooting arrows, remove this * self.arrow_velocity and then put it into translate instead
        self.translate(direction * -1)
        self.to_render.angle = -self.arrow_angle * 180 / math.pi


    def translate(self, direction):
        self.center += direction # * self.arrow_velocity // simulates pull back of arrows
        for i in range(len(self.vertices)):
            self.vertices[i] += direction # * self.arrow_velocity


    