from z_extensions.render import *
from z_extensions.Square import Hitbox
from z_extensions.vector import Vector
from z_health.health import HealthBar
from z_extensions.timer import Timer
import random
import math

mid_x = 200
mid_y = 200


class Butterfly(Hitbox):
    def __init__(self, center, width, height, color, name, health=500):
        super().__init__(center, width, height, color)
        self.health = health

        self.images = []
        for i in range(len(butterfly_images_stack)):
            self.images.append([img.convert_alpha() for img in butterfly_images_stack[i]])

        self.num_images = len(self.images[0])

        self.attack_damage = 50 

        self.spread = 1.3
        self.to_render = Render(self.images, center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)


        self.shoot_angle_degrees = 45
        self.shoot_angle_radians = 0

        self.start_shoot_angle = 10

        self.turn_angle_degrees = 1

        self.delete_radius = 200

        
        self.summon_rise = 15 # layer appears every 15 frames (4 layers every second)

        self.summoning = False
        self.summon_start = 0
        self.summon_end = self.num_images * self.summon_rise
        self.summon_index = self.num_images
        self.summoned = False


        self.looking = Vector(0, 0)
        self.locked = Hitbox([0, 0], 4, 4, black)
        self.charge_towards = Vector(0, 0)


        self.charge_speed = 2 # how fast it charges at the player
        self.max_charge_distance = 200

        self.charging_timer = Timer(45)
        self.pausing_timer = Timer(45)


        self.bullets = []

        self.tracking = False

        self.dead = False

        self.name = name

        self.barrels_busted = 0
        

        self.boss_looking = Vector(1, 0)
        self.boss_angle_degrees_increment = 45
        self.boss_angle_degrees = 0
        self.s_x, self.s_y = self.boss_angle_degrees * math.pi / 180, self.boss_angle_degrees * math.pi / 180
        self.s = Vector(math.cos(self.s_x), math.sin(self.s_y))


        self.activate = 35 # 35 activates after breaking this many barrels


        self.closest_to_player = False





    def check_if_summon(self):
        if self.barrels_busted >= self.activate and not self.summoned and not self.dead:
            self.summoning = True
            self.tracking = True

        if self.summoning:
            self.summon_start += self.dt

            if self.summon_start >= self.summon_rise:
                self.summon_start = 0
                if self.summon_index > 0:
                    self.summon_index -= 1
                else:
                    self.to_render.images = self.images
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
        self.to_render.images = self.images[0][self.summon_index:self.num_images]
        self.to_render.render_stack(surface)
    
    def follow_player(self, player_center):
        v = self.center - player_center
        v = v.normalize()
        self.looking = v
        angle = math.atan2(v.x, v.y)
        angle = angle * 180 / math.pi
        self.to_render.angle = angle


    def draw_healthbar(self, surface):
        if self.closest_to_player:
            white_bar_width = 180
            white_bar_height = 16


            width = self.health_bar.health / self.health_bar.maxhealth * 180
            center = Vector(mid_x, 30)
            
            margin_top_bottom = 2
            margin_left_right = 2

            render_text((center.x - len(self.name) * 7 / 2, 10), self.name, surface)
            pygame.draw.rect(surface, white, pygame.Rect(center.x - (white_bar_width / 2 + margin_left_right), center.y - (white_bar_height / 2), white_bar_width + margin_left_right * 2, white_bar_height))
            pygame.draw.rect(surface, self.color, pygame.Rect(center.x - (white_bar_width / 2), center.y - (white_bar_height / 2 - margin_top_bottom), width, white_bar_height - margin_top_bottom * 2))
            

        self.health_bar.draw(surface, self.center, self.height)


    def update(self, rotation_input, input, direction):
        self.get_direction(input)
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle
        self.locked.update(rotation_input, direction)



    def damage(self, dmg):
        if not self.summoned:
            pass
        else:
            self.health_bar.damage(dmg)

    def attacks(self, dt):
        if self.summoned and not self.dead:
            self.attack_two()


    def spiral_attack(self):
        
        shot_1 = Shuriken([self.center.x, self.center.y], 16, 16, blue, self.last_looked * -1)
        shot_1.shuriken_angle_start = math.atan2(self.last_looked.y * -1, self.last_looked.x * -1) + self.angle * math.pi / 180
        
        self.bullets.append(shot_1)

        shot_2 = Shuriken([self.center.x, self.center.y], 16, 16, blue, Vector(-self.last_looked.y, self.last_looked.x))
        shot_2.shuriken_angle_start = math.atan2(self.last_looked.x, -self.last_looked.y) + self.angle * math.pi / 180
        
        self.bullets.append(shot_2)

        shot_3 = Shuriken([self.center.x, self.center.y], 16, 16, blue, self.last_looked)
        shot_3.shuriken_angle_start = math.atan2(self.last_looked.y, self.last_looked.x) + self.angle * math.pi / 180
        
        self.bullets.append(shot_3)

        shot_4 = Shuriken([self.center.x, self.center.y], 16, 16, blue, Vector(self.last_looked.y, -self.last_looked.x))
        shot_4.shuriken_angle_start = math.atan2(-self.last_looked.x, self.last_looked.y) + self.angle * math.pi / 180
        
        self.bullets.append(shot_4)



        
    def attack_two(self):
        self.charge_towards = self.locked.center - self.center
        self.charge_towards.normalize()

        self.charge()



    def charge(self):
        self.charging_timer.start_timer(self.dt)
        # if there isnt an alarm, keep charging
        if not self.charging_timer.alarm:
            
            self.attack_damage = 20
            self.move(self.charge_towards * self.charge_speed * self.dt)
        else:
            self.locked.center = Vector(self.location[0], self.location[1]) + (self.looking * -self.max_charge_distance)
            self.locked.set_vertices()

            self.attack_damage = 0

            self.move(self.looking * -1 * .6 * self.dt)

            # when the charging timer ends, deactivate it
            self.charging_timer.active = False
            self.pausing_timer.active = True # activate pausing timer
            self.pausing_timer.start_timer(self.dt)

            # when the pausing timer ends,
            if self.pausing_timer.alarm: # reset all timers
                self.charging_timer.end = random.randint(25, 55)
                self.charging_timer.reset_timer()
                self.pausing_timer.reset_timer()
                self.pausing_timer.active = False
                self.charging_timer.active = True



            
            
    def directional_attack(self):
        self.s = Vector(math.cos(self.s_x), math.sin(self.s_y))
        g = math.atan2(self.s.y, self.s.x) - self.angle * math.pi / 180
        a = (360 + (g * 180 / math.pi)) * math.pi / 180
        x, y = math.cos(a), math.sin(a)
        self.s = Vector(x, y)


        shot_5 = Shuriken([self.center.x, self.center.y], 16, 16, blue, self.s)
        shot_5.shuriken_angle_start = math.atan2(self.s.y, self.s.x) + self.angle * math.pi / 180
        
        self.boss_angle_degrees += self.boss_angle_degrees_increment
        self.s_x, self.s_y = self.boss_angle_degrees * math.pi / 180, self.boss_angle_degrees * math.pi / 180



        self.bullets.append(shot_5)


    def delete_shuriken(self, shuriken_to_delete):
        for i in range(len(self.bullets)):
            if self.bullets[i] == shuriken_to_delete:
                del self.bullets[i]
                return



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


    
