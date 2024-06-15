from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
import math

class Watermelon(Hitbox):
    def __init__(self, center, width, height, color, health=5):
        super().__init__(center, width, height, color)
        self.images = watermelon_images
        self.spread = .4

        self.spinspeed_degrees = 1
        self.spin_speed = self.rotationspeed_degress * math.pi / 180

        self.melon_angle = 0
        self.accel = .01

        self.lift_height = .15
        self.lift_speed = .06
        self.lift_angle = 0
        self.melon_y = 5

        self.to_render = Render(self.images, center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)




    
    def render(self, surface):
        for i, img in enumerate(self.images):
            img.convert_alpha()
            rotated_img = pygame.transform.rotate(img, self.melon_angle)
            surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - self.melon_y - rotated_img.get_height() // 2 - i * self.spread))

    def self_spin(self):
        self.melon_angle -= self.spin_speed * 180 / math.pi

        # i have no idea how i did this LMAO
        self.lift_angle += self.lift_speed
        sin = math.sin(self.lift_angle)
        sub = sin * self.lift_height
        self.melon_y -= sub



        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.spin_speed) + (self.vertices[i].y - self.center.y) * -math.sin(self.spin_speed) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.spin_speed) + (self.vertices[i].y - self.center.y) * math.cos(self.spin_speed) + self.center.y

    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.self_spin()
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.melon_angle

