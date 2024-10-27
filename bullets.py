from render import *
from Square import Hitbox
from vector import Vector
import particles as particles
import random
import math




class SwordShot(Hitbox):
    def __init__(self, center, width, height, color, looking, sword_angle_start):
        super().__init__(center, width, height, color)
        
        self.images = swordshot_image_black.convert_alpha()
        self.sword_velocity = 10
        self.sword_velocity_og = 2
        self.sword_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates sword to point that direction

        self.sword_angle_start = sword_angle_start
        self.set_angle(self.sword_angle) # sets the direction of all the vertices to face the right way
        self.spread = 1
        self.damage = 5
        self.to_render = Render(self.images, center, self.sword_angle, self.spread)
        # for the spinning of the sword
        self.rotation_angle = 0
        self.spin_speed_degrees = 4
        self.spin_speed = self.spin_speed_degrees * math.pi / 180



        self.particles = []


    def add_particles(self, loc):
        for i in range(2):
            v_x = random.randint(-100, 400) / 500 * self.direction.x * -2 * 2
            v_y = random.randint(0, 400) / 500 * self.direction.y * -1 * 2
            p = particles.Particle([loc[0], loc[1] + 4], [v_x, v_y], random.randint(3, 5), "dust")
            p.gravity = -.02
            p.shrink_rate = .08
            self.particles.append(p)

    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y


    def render(self, surface):
        self.to_render.render_single(surface)

    def self_spin(self):
        self.rotation_angle -= self.spin_speed_degrees

        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.spin_speed * self.dt) + (self.vertices[i].y - self.center.y) * -math.sin(self.spin_speed * self.dt) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.spin_speed * self.dt) + (self.vertices[i].y - self.center.y) * math.cos(self.spin_speed * self.dt) + self.center.y


    def handle_rotation_sword(self, rotation_input):
        if not rotation_input["reset"]: # have to do this because it interferes with the sword rotation (might have to do it with everything else to make it cleaner)
            self.handle_rotation(rotation_input)

        if rotation_input["reset"]:
            # print(self.sword_angle, self.sword_angle_start)
            if self.sword_angle != self.sword_angle_start:
                self.reset_sword_rotation()
                self.sword_angle = self.sword_angle_start
            return # so no continuous rotation


        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.sword_angle -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.sword_angle += self.rotationspeed


    



    def reset_sword_rotation(self):
        back = -(self.sword_angle - self.sword_angle_start)
        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(back) + (self.center.y - mid_y) * -math.sin(back) + mid_x, (self.center.x - mid_x) * math.sin(back) + (self.center.y - mid_y) * math.cos(back) + mid_y
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(back) + (self.vertices[i].y - mid_y) * -math.sin(back) + mid_x, (self.vertices[i].x - mid_x) * math.sin(back) + (self.vertices[i].y - mid_y) * math.cos(back) + mid_y
        
    def update(self, rotation_input, direction):
        self.move(direction * -1 * self.velocity) # have to multiply player velocity as well???
        self.translate(Vector(math.cos(self.sword_angle), math.sin(self.sword_angle)) * self.sword_velocity * self.dt) # if i want to simulate shooting swords, remove this * self.sword_velocity and then put it into translate instead
        self.handle_rotation_sword(rotation_input)
        # self.add_particles([self.center.x, self.center.y])
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = -self.sword_angle * 180 / math.pi

    def update_particles(self, display):
        for particle in self.particles:
            particle.all(display)



    def translate(self, direction):
        self.center += direction # * self.sword_velocity // simulates pull back of swords
        for i in range(len(self.vertices)):
            self.vertices[i] += direction # * self.sword_velocity
            
    def change_images(self, imgs):
        self.images = imgs.convert_alpha()
        self.to_render.images = self.images
    

    

class Shuriken(Hitbox):
    def __init__(self, center, width, height, color, looking):
        super().__init__(center, width, height, color)
        
        self.images = shuriken_img.convert_alpha()
        self.shuriken_velocity = 1
        self.shuriken_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates shuriken to point that direction
        self.shuriken_angle_start = 0
        self.set_angle(self.shuriken_angle) # sets the direction of all the vertices to face the right way
        self.spread = 1
        self.damage = 5
        self.to_render = Render(self.images, center, self.shuriken_angle, self.spread)

        # for the spinning of the shuriken
        self.rotation_angle = 0
        self.spin_speed_degrees = 4
        self.spin_speed = self.spin_speed_degrees * math.pi / 180

    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y


    def render(self, surface):
        self.to_render.render_single(surface)

    def self_spin(self):
        self.rotation_angle -= self.spin_speed_degrees

        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.spin_speed * self.dt) + (self.vertices[i].y - self.center.y) * -math.sin(self.spin_speed * self.dt) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.spin_speed * self.dt) + (self.vertices[i].y - self.center.y) * math.cos(self.spin_speed * self.dt) + self.center.y


    def handle_rotation_shuriken(self, rotation_input):
        if not rotation_input["reset"]: # have to do this because it interferes with the shuriken rotation (might have to do it with everything else to make it cleaner)
            self.handle_rotation(rotation_input)



        if rotation_input["reset"]:
            # print(self.shuriken_angle, self.shuriken_angle_start)
            if self.shuriken_angle != self.shuriken_angle_start:
                self.reset_shuriken_rotation()
                self.shuriken_angle = self.shuriken_angle_start
            return # so no continuous rotation


        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.shuriken_angle -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.shuriken_angle += self.rotationspeed


    def reset_shuriken_rotation(self):
        back = -(self.shuriken_angle - self.shuriken_angle_start)
        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(back) + (self.center.y - mid_y) * -math.sin(back) + mid_x, (self.center.x - mid_x) * math.sin(back) + (self.center.y - mid_y) * math.cos(back) + mid_y
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(back) + (self.vertices[i].y - mid_y) * -math.sin(back) + mid_x, (self.vertices[i].x - mid_x) * math.sin(back) + (self.vertices[i].y - mid_y) * math.cos(back) + mid_y
        
    def update(self, rotation_input, direction):
        self.self_spin()
        self.move(direction * -1 * self.velocity) # have to multiply player velocity as well???
        self.translate(Vector(math.cos(self.shuriken_angle), math.sin(self.shuriken_angle)) * self.shuriken_velocity * self.dt) # if i want to simulate shooting shurikens, remove this * self.shuriken_velocity and then put it into translate instead
        self.handle_rotation_shuriken(rotation_input)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = -self.rotation_angle


    def translate(self, direction):
        self.center += direction # * self.shuriken_velocity // simulates pull back of shurikens
        for i in range(len(self.vertices)):
            self.vertices[i] += direction # * self.shuriken_velocity



