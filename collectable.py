from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
import math

class Collectable(Hitbox):
    def __init__(self, center, width, height, color, images):
        super().__init__(center, width, height, color)
        self.images = images
        self.spread = .4

        self.spinspeed_degrees = 1
        self.spin_speed = self.spinspeed_degrees * math.pi / 180

        self.item_angle = 0
        self.accel = .01

        self.lift_height = .15
        self.lift_speed = .06
        self.lift_angle = 0
        self.start_y = 5

        self.to_render = Render(self.images, center, self.angle, self.spread)


        self.follow_player = False
        self.follow_speed = 0.02



    def render(self, surface):
        for i, img in enumerate(self.images):
            img.convert_alpha()
            rotated_img = pygame.transform.rotate(img, self.item_angle)
            surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - self.start_y - rotated_img.get_height() // 2 - i * self.spread))

    def self_spin(self):
        self.item_angle -= self.spin_speed * 180 / math.pi

        # i have no idea how i did this LMAO
        self.lift_angle += self.lift_speed
        sin = math.sin(self.lift_angle)
        sub = sin * self.lift_height
        self.start_y -= sub


        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.spin_speed) + (self.vertices[i].y - self.center.y) * -math.sin(self.spin_speed) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.spin_speed) + (self.vertices[i].y - self.center.y) * math.cos(self.spin_speed) + self.center.y

    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.self_spin()
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.item_angle

