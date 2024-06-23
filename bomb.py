from render import *
from Square import Hitbox
from vector import Vector
import math
# Bomb class uses a lot of arrow functionality, did not wanna code again

mid_x, mid_y = 200, 200

#
class Bomb(Hitbox):
    def __init__(self, center, width, height, color, looking, velocity=2):
        super().__init__(center, width, height, color)
        self.images = bomb_images
        self.bomb_velocity = velocity
        self.bomb_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates bomb to point that direction
        self.bomb_angle_start = 0
        self.set_angle(self.bomb_angle) # sets the direction of all the vertices to face the right way
        self.spread = .4
        self.to_render = Render(self.images, center, self.bomb_angle, self.spread)

        self.bomb_height = 0
        self.time = 0

        self.gravity = .1
        self.speed = 2.2

        self.damage = 50
        self.distance = 50


        self.landing = False

    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y

    def render(self, surface):
        for i, img in enumerate(self.images):
            img.convert_alpha()
            rotated_img = pygame.transform.rotate(img, self.bomb_angle)
            surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - self.bomb_height - rotated_img.get_height() // 2 - i * self.spread))


    def rise(self):
        self.bomb_height += self.speed
        self.speed -= self.gravity
        if self.bomb_height < -3:
            self.landing = True


    def handle_rotation_bomb(self, rotation_input):
        if not rotation_input["reset"]: # have to do this because it interferes with the bomb rotation (might have to do it with everything else to make it cleaner)
            self.handle_rotation(rotation_input)


        if rotation_input["reset"]:
            if self.bomb_angle != self.bomb_angle_start:
                self.reset_bomb_rotation()
                self.bomb_angle = self.bomb_angle_start
            return # so no continuous rotation


        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.bomb_angle -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.bomb_angle += self.rotationspeed


    def reset_bomb_rotation(self):
        back = -(self.bomb_angle - self.bomb_angle_start)
        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(back) + (self.center.y - mid_y) * -math.sin(back) + mid_x, (self.center.x - mid_x) * math.sin(back) + (self.center.y - mid_y) * math.cos(back) + mid_y
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(back) + (self.vertices[i].y - mid_y) * -math.sin(back) + mid_x, (self.vertices[i].x - mid_x) * math.sin(back) + (self.vertices[i].y - mid_y) * math.cos(back) + mid_y
        
    def update(self, rotation_input, direction):
        self.move(direction * -1 * self.velocity) # have to multiply player velocity as well???
        self.translate(Vector((math.cos(self.bomb_angle), math.sin(self.bomb_angle))) * self.bomb_velocity)
        self.handle_rotation_bomb(rotation_input)
        self.rise()
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = -self.bomb_angle * 180 / math.pi


    def translate(self, direction):
        self.center += direction 
        for i in range(len(self.vertices)):
            self.vertices[i] += direction 


    