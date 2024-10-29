from render import *
from Square import Hitbox
from vector import Vector
import math


mid_x, mid_y = 200, 200

class Arrow(Hitbox):
    def __init__(self, center, width, height, color, looking, arrow_angle_start):
        super().__init__(center, width, height, color)
        
        self.images = [img.convert_alpha() for img in arrow_images]
        self.arrow_velocity = 4
        self.arrow_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates arrow to point that direction
        self.arrow_angle_start = arrow_angle_start
        self.set_angle(self.arrow_angle) # sets the direction of all the vertices to face the right way
        self.spread = 1
        self.damage = 10 # 10
        self.to_render = Render(self.images, center, self.arrow_angle, self.spread)
        # self.direction = Vector((1, 0))

    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y

    def render(self, surface):
        self.to_render.render_stack(surface)


    def handle_rotation_arrow(self, rotation_input):
        if not rotation_input["reset"]: # have to do this because it interferes with the arrow rotation (might have to do it with everything else to make it cleaner)
            self.handle_rotation(rotation_input)



        if rotation_input["reset"]:
            if self.arrow_angle != self.arrow_angle_start:
                self.reset_arrow_rotation()
                self.arrow_angle = self.arrow_angle_start
            return # so no continuous rotation


        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.arrow_angle -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.arrow_angle += self.rotationspeed


    def reset_arrow_rotation(self):
        back = -(self.arrow_angle - self.arrow_angle_start)
        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(back) + (self.center.y - mid_y) * -math.sin(back) + mid_x, (self.center.x - mid_x) * math.sin(back) + (self.center.y - mid_y) * math.cos(back) + mid_y
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(back) + (self.vertices[i].y - mid_y) * -math.sin(back) + mid_x, (self.vertices[i].x - mid_x) * math.sin(back) + (self.vertices[i].y - mid_y) * math.cos(back) + mid_y
        
    def update(self, rotation_input, direction):
        self.move(direction * -1 * self.velocity) # have to multiply player velocity as well???
        self.translate(Vector(math.cos(self.arrow_angle), math.sin(self.arrow_angle)) * self.arrow_velocity * self.dt) # if i want to simulate shooting arrows, remove this * self.arrow_velocity and then put it into translate instead
        self.handle_rotation_arrow(rotation_input)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = -self.arrow_angle * 180 / math.pi


    def translate(self, direction):
        self.center += direction # * self.arrow_velocity // simulates pull back of arrows
        for i in range(len(self.vertices)):
            self.vertices[i] += direction # * self.arrow_velocity


    