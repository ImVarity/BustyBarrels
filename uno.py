from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
from arrow import Arrow
import math

mid_x = 200
mid_y = 200


class Uno(Hitbox):
    def __init__(self, center, width, height, color, health=1000):
        super().__init__(center, width, height, color)
        self.images = barrel_images
        self.spread = 1.3
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, (0, 0, 0))

        self.boss_angle_radians = 0

        self.shoot_angle_degrees = 45
        self.shoot_angle_radians = 0

        self.start_shoot_angle = 10

        self.turn_angle_degrees = 1

        self.delete_radius = 200




        self.shurikens = []

    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)


    def update(self, rotation_input, direction):
        self.handle_rotation_boss(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

    
    def attack_one(self, player_looking_angle):
        
        print(self.center)
        for i in range(8):
            # print(self.shoot_angle_radians * 180 / math.pi)
            shuri = Shuriken((self.center.x, self.center.y), 16, 16, self.color, Vector((math.cos(self.shoot_angle_radians + self.boss_angle_radians), math.sin(self.shoot_angle_radians + self.boss_angle_radians))))
            # shuri.shuriken_angle_start = player_looking_angle
            self.shurikens.append(shuri)
            self.shoot_angle_radians += self.shoot_angle_degrees * math.pi / 180
        
        # give different start
        self.shoot_angle_radians = self.start_shoot_angle * math.pi / 180
        self.start_shoot_angle += 10

        print()


    
    def handle_rotation_boss(self, rotation_input):

        self.handle_rotation(rotation_input)
        

        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.boss_angle_radians -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.boss_angle_radians += self.rotationspeed


class Shuriken(Hitbox):
    def __init__(self, center, width, height, color, looking):
        super().__init__(center, width, height, color)
        self.images = shuriken_img
        self.shuriken_velocity = 2
        self.shuriken_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates shuriken to point that direction
        self.shuriken_angle_start = self.shuriken_angle
        # self.set_angle(self.shuriken_angle) # sets the direction of all the vertices to face the right way
        self.damage = 5
        self.to_render = Render(self.images, center, self.shuriken_angle)

        self.rotation_angle = 0
        self.spin_speed_degrees = 2
        self.spin_speed = self.spin_speed_degrees * math.pi / 180

        self.distance_from_boss = 0

        self.og_center = center
        

    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y


    def render(self, surface):
        self.to_render.render_single(surface)



    def handle_rotation_shuriken(self, rotation_input):
        if not rotation_input["reset"]:
            self.handle_rotation(rotation_input)

        if rotation_input["reset"]:
            if self.shuriken_angle != self.shuriken_angle_start:
                self.reset_rotation_shuriken()
                self.shuriken_angle = self.shuriken_angle_start
            return

        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.shuriken_angle -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.shuriken_angle += self.rotationspeed

    def reset_rotation_shuriken(self):
        back = -(self.shuriken_angle - self.shuriken_angle_start)
        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(back) + (self.center.y - mid_y) * -math.sin(back) + mid_x, (self.center.x - mid_x) * math.sin(back) + (self.center.y - mid_y) * math.cos(back) + mid_y
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(back) + (self.vertices[i].y - mid_y) * -math.sin(back) + mid_x, (self.vertices[i].x - mid_x) * math.sin(back) + (self.vertices[i].y - mid_y) * math.cos(back) + mid_y
        
    def self_spin(self):
        self.rotation_angle -= self.spin_speed_degrees

        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.spin_speed) + (self.vertices[i].y - self.center.y) * -math.sin(self.spin_speed) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.spin_speed) + (self.vertices[i].y - self.center.y) * math.cos(self.spin_speed) + self.center.y


    def update(self, rotation_input, direction):
        self.self_spin()
        self.handle_rotation_shuriken(rotation_input)
        self.translate(Vector((math.cos(self.shuriken_angle), math.sin(self.shuriken_angle))) * self.shuriken_velocity) # if i want to simulate shooting shurikens, remove this * self.shuriken_velocity and then put it into translate instead
        self.translate(direction * -1 * self.velocity) # have to multiply player velocity as well???
        self.to_render.angle = self.rotation_angle
        self.to_render.loc = [self.center.x, self.center.y]


    def translate(self, direction):
        self.center += direction # * self.shuriken_velocity // simulates pull back of shurikens
        for i in range(len(self.vertices)):
            self.vertices[i] += direction # * self.shuriken_velocity

