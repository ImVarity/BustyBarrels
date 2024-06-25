from render import *
from Square import Hitbox
from health import HealthBar
from vector import Vector
from arrow import Arrow
import math

class Dos(Hitbox):
    def __init__(self, center, width, height, color, health=1000):
        super().__init__(center, width, height, color)
        self.images = Uno_images
        self.num_images = len(self.images)
        self.spread = 1.2
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)

        self.delete_radius = 200
        self.summon_rise = 15 # layer appears every 15 frames (4 layers every second)

        self.summoning = False
        self.summon_start = 0
        self.summon_end = self.num_images * self.summon_rise
        self.summon_increment = 1
        self.summon_index = self.num_images
        self.summoned = True

        self.tracking = False

        self.dead = False

        self.name = "Tif"

        self.shurikens = []

        self.angle_r = 0

        self.tif_last_looked_og = Vector((0, 1))
        self.tif_angle_looking_og = 90 * math.pi / 180 
        
        self.tif_last_looked = Vector((0, 1))
        self.tif_angle_looking = 90 * math.pi / 180 



        self.v_add = Vector((0, 1))
        self.angle_add = 45 * math.pi / 180


    # def random_direction(self):


    def spiral_attack(self):
        
        shot = Shuriken([self.center.x, self.center.y], 16, 16, blue, self.tif_last_looked)
        shot.shuriken_angle_start = math.atan2(self.tif_last_looked.y, self.tif_last_looked.x) + self.angle * math.pi / 180
        self.shurikens.append(shot)

        


    def follow_player(self, player_center):
        v = self.center - player_center
        v = v.normalize()
        angle = math.atan2(v.x, v.y)
        angle = angle * 180 / math.pi
        self.to_render.angle = angle - 90
        
    def death(self):
        self.to_render.images = barrel_images
        self.dead = True
    
    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)

    def damage(self, dmg):
        if not self.summoned:
            pass
        else:
            self.health_bar.damage(dmg)

    # def update_look(self, angle_looking, looking):

    #     print("looks", looking, self.last_looked)
    #     # self.looking = looking
    #     # self.angle_looking = angle_looking
    #     # self.looking = looking

    def update(self, rotation_input, input, direction):
        # print(self.angle_looking, math.atan2(self.tif_last_looked.y, self.tif_last_looked.x) + self.angle * math.pi / 180)
        # print(90 * math.pi / 180 - self.angle * math.pi / 180, self.angle, self.angle_looking)
        # print(self.angle_looking * 180 / math.pi)
        # print(self.angle_looking - 45 * math.pi / 180)
        # print(self.tif_last_looked, self.tif_angle_looking)
        print(self.angle_looking, math.atan2(self.tif_last_looked.y, self.tif_last_looked.x))
        self.get_direction(input)
        self.handle_rotation(rotation_input)
        # if rotation_input["reset"]:
        #     self.tif_angle_looking = self.tif_angle_looking_og
        #     self.tif_last_looked = self.tif_last_looked_og
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

    def draw_healthbar(self, surface):
        white_bar_width = 180
        white_bar_height = 16


        width = self.health_bar.health / self.health_bar.maxhealth * 180
        center = Vector((mid_x, 30))
        
        margin_top_bottom = 2
        margin_left_right = 2

        render_text((center.x - len(self.name) * 7 / 2, 10), self.name, surface)
        pygame.draw.rect(surface, white, pygame.Rect(center.x - (white_bar_width / 2 + margin_left_right), center.y - (white_bar_height / 2), white_bar_width + margin_left_right * 2, white_bar_height))
        pygame.draw.rect(surface, purple, pygame.Rect(center.x - (white_bar_width / 2), center.y - (white_bar_height / 2 - margin_top_bottom), width, white_bar_height - margin_top_bottom * 2))
        
        self.health_bar.draw(surface, self.center, self.height)



class Shuriken(Hitbox):
    def __init__(self, center, width, height, color, looking):
        super().__init__(center, width, height, color)
        self.images = shuriken_img.convert_alpha()
        self.shuriken_velocity = .1
        self.shuriken_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates shuriken to point that direction
        self.shuriken_angle_start = 0
        self.set_angle(self.shuriken_angle) # sets the direction of all the vertices to face the right way
        self.damage = 50
        self.to_render = Render(self.images, center, self.shuriken_angle)

        self.rotation_angle = 0
        self.spin_speed_degrees = 4
        self.spin_speed = self.spin_speed_degrees * math.pi / 180

        

    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y


    def render(self, surface):
        self.to_render.render_single(surface)


    def handle_rotation_shuriken(self, rotation_input):
        
        # print("shuri angle", self.shuriken_angle * 180 / math.pi, "started with", self.shuriken_angle_start * 180 / math.pi, "subtracted", self.shuriken_angle * 180 / math.pi - self.shuriken_angle_start * 180 / math.pi)
        # print("turned", (self.shuriken_angle * 180 / math.pi - self.shuriken_angle_start * 180 / math.pi), "degrees")

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


        # print(self.shuriken_angle * 180 / math.pi - self.shuriken_angle_start * 180 / math.pi)

        back = -(self.shuriken_angle - self.shuriken_angle_start)

        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(back) + (self.center.y - mid_y) * -math.sin(back) + mid_x, (self.center.x - mid_x) * math.sin(back) + (self.center.y - mid_y) * math.cos(back) + mid_y
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(back) + (self.vertices[i].y - mid_y) * -math.sin(back) + mid_x, (self.vertices[i].x - mid_x) * math.sin(back) + (self.vertices[i].y - mid_y) * math.cos(back) + mid_y
        
    def self_spin(self):
        self.rotation_angle -= self.spin_speed_degrees

        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.spin_speed) + (self.vertices[i].y - self.center.y) * -math.sin(self.spin_speed) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.spin_speed) + (self.vertices[i].y - self.center.y) * math.cos(self.spin_speed) + self.center.y


    def update(self, rotation_input, direction):
        # self.self_spin()
        self.handle_rotation_shuriken(rotation_input)
        self.translate(Vector((math.cos(self.shuriken_angle), math.sin(self.shuriken_angle))) * self.shuriken_velocity) # if i want to simulate shooting shurikens, remove this * self.shuriken_velocity and then put it into translate instead
        self.translate(direction * -1 * self.velocity) # have to multiply player velocity as well???
        self.to_render.angle = self.rotation_angle
        self.to_render.loc = [self.center.x, self.center.y]


    def translate(self, direction):
        self.center += direction # * self.shuriken_velocity // simulates pull back of shurikens
        for i in range(len(self.vertices)):
            self.vertices[i] += direction # * self.shuriken_velocity


    def translate(self, direction):
        self.center += direction # * self.arrow_velocity // simulates pull back of arrows
        for i in range(len(self.vertices)):
            self.vertices[i] += direction # * self.arrow_velocity

