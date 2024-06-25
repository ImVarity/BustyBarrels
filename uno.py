from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
import math

mid_x = 200
mid_y = 200


class Uno(Hitbox):
    def __init__(self, center, width, height, color, health=1000):
        super().__init__(center, width, height, color)
        self.health = health
        self.images = [img.convert_alpha() for img in Uno_images]
        self.num_images = len(self.images)

        self.spread = 1.3
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)

        self.boss_angle_radians = 0

        self.shoot_angle_degrees = 45
        self.shoot_angle_radians = 0

        self.start_shoot_angle = 10

        self.turn_angle_degrees = 1

        self.delete_radius = 200

        
        self.summon_rise = 15 # layer appears every 15 frames (4 layers every second)

        self.summoning = False
        self.summon_start = 0
        self.summon_end = self.num_images * self.summon_rise
        self.summon_increment = 1
        self.summon_index = self.num_images
        self.summoned = False


        self.looking = Vector((0, 0))
        self.locked = Vector((0, 0))


        self.charge_now = False
        self.charging = False
        self.charge_start = 0
        self.charge_end = 45
        self.charge_inc = 1

        self.shurikens = []

        self.tracking = False

        self.dead = False

        self.name = "Tifanie"

        self.barrels_busted = 0


    def check_if_summon(self):
        if self.barrels_busted > 2 and not self.summoned:
            self.summoning = True
            self.tracking = True

        if self.summoning:
            self.summon_start += self.summon_increment

            if self.summon_start % self.summon_rise == 0:
                if self.summon_index > 0:
                    self.summon_index -= 1
                else:
                    self.summoned = True
                    self.summoning = False
                    self.tracking = False

    def temp_death(self):

        self.health_bar.set_health(self.health)
        self.summoned = False
        self.summon_start = 0
        self.summon_index = self.num_images
        self.barrels_busted = 0




    def death(self):
        self.images = barrel_images
        self.dead = True

    def render(self, surface):
        self.to_render.images = self.images[self.summon_index:self.num_images]
        self.to_render.render_stack(surface)
    
    def follow_player(self, player_center):
        v = self.center - player_center
        v = v.normalize()
        self.looking = v
        angle = math.atan2(v.x, v.y)
        angle = angle * 180 / math.pi
        self.to_render.angle = angle - 90


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


    def update(self, rotation_input, input, direction):
        self.get_direction(input)
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle



    def damage(self, dmg):
        if not self.summoned:
            pass
        else:
            self.health_bar.damage(dmg)


    def spiral_attack(self):
        
        shot_1 = Shuriken([self.center.x, self.center.y], 16, 16, blue, self.last_looked * -1)
        shot_1.shuriken_angle_start = math.atan2(self.last_looked.y * -1, self.last_looked.x * -1) + self.angle * math.pi / 180
        
        self.shurikens.append(shot_1)

        shot_2 = Shuriken([self.center.x, self.center.y], 16, 16, blue, Vector((-self.last_looked.y, self.last_looked.x)))
        shot_2.shuriken_angle_start = math.atan2(self.last_looked.x, -self.last_looked.y) + self.angle * math.pi / 180
        
        self.shurikens.append(shot_2)

        shot_3 = Shuriken([self.center.x, self.center.y], 16, 16, blue, self.last_looked)
        shot_3.shuriken_angle_start = math.atan2(self.last_looked.y, self.last_looked.x) + self.angle * math.pi / 180
        
        self.shurikens.append(shot_3)

        shot_4 = Shuriken([self.center.x, self.center.y], 16, 16, blue, Vector((self.last_looked.y, -self.last_looked.x)))
        shot_4.shuriken_angle_start = math.atan2(-self.last_looked.x, self.last_looked.y) + self.angle * math.pi / 180
        
        self.shurikens.append(shot_4)
    def attack_two(self):
        self.locked = self.looking
        self.charging = True

        self.charge()

    def charge(self):
        if self.charging:
            self.charge_start += self.charge_inc

            self.move(self.locked * -1 * .8)

            shot = Shuriken([self.center.x, self.center.y], 16, 16, blue, self.last_looked)
            shot.shuriken_angle_start = math.atan2(self.last_looked.y, self.last_looked.x) + self.angle * math.pi / 180
            shot.shuriken_velocity = 4
            self.shurikens.append(shot)



    def delete_shuriken(self, shuriken_to_delete):
        for i in range(len(self.shurikens)):
            if self.shurikens[i] == shuriken_to_delete:
                del self.shurikens[i]
                return


class Shuriken(Hitbox):
    def __init__(self, center, width, height, color, looking):
        super().__init__(center, width, height, color)
        self.images = shuriken_img.convert_alpha()
        self.shuriken_velocity = 1
        self.shuriken_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates shuriken to point that direction
        self.shuriken_angle_start = self.shuriken_angle
        # self.set_angle(self.shuriken_angle) # sets the direction of all the vertices to face the right way
        self.damage = 50
        self.to_render = Render(self.images, center, self.shuriken_angle)

        self.rotation_angle = 0
        self.spin_speed_degrees = 4
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

