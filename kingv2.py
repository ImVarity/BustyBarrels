from mod import Boss
from Square import Hitbox
from vector import Vector
from health import HealthBar
from uno import Shuriken
from king import SwordShot
from timer import Timer
from render import *
import random
import math





class Kingv2(Boss):
    def __init__(self, center, width, height, color, name, health=1):
        super().__init__(center, width, height, color, name, health)
        self.images = [img.convert_alpha() for img in barrelking_images]
        self.num_images = len(self.images)
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.summon_rise = 12
        self.summon_end = self.num_images * self.summon_rise
        self.activate = 1


        self.king_height = 0
        self.landing = False
        self.can_jump = False
        self.locked = False
        self.lock = Vector(0, 0)
        self.locked_distance = 0

        self.king_velocity_max = 0.01
        self.king_velocity = self.king_velocity_max
        self.speed = 2.2
        self.gravity = 0.1
        self.king_jump_velocity = 4




        # Landing attack stuff ------------
        self.pause = 0
        self.pause_end = 60
        self.pause_inc = 1


        self.eight_shot = False
        self.number_of_eight_shots = 0
        self.landed = False
        self.just_landed = False
        self.in_air = False



        # Half square attack stuff ------------
        self.sword_show_timer = Timer(75) # 75
        self.sword_attack_timer = Timer(120) # 120

        self.throwing_point = 0
        self.throwing_points = [[mid_x - 150, mid_y + 150],
                                [mid_x - 150, mid_y - 150]]
        self.throwing_points_vertical = [[mid_x + 150, mid_y - 150],
                                        [mid_x - 150, mid_y - 150]]

    def update(self, rotation_input, input, direction, player_center):
        self.jump(player_center)
        self.move(direction * -1 * self.velocity)
        self.get_direction(input)
        self.handle_rotation(rotation_input)

        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

    def jump(self, player_center):
        if self.summoned and not self.dead:
            if self.can_jump:
                if self.locked == False:
                    self.lock = self.track_player(player_center)
                    self.locked = True
                    self.locked_distance = math.hypot((self.center.x - player_center.x), (self.center.y - player_center.y))
                    if self.locked_distance > self.get_jump_distance():
                        self.locked_distance = self.get_jump_distance()

                self.king_velocity = self.king_velocity_max
                self.king_height += self.speed * self.dt
                self.speed -= self.gravity * self.dt
                if self.king_height < 0:
                    self.landing = True
                    self.can_jump = False
                    self.king_height = 0
                    self.speed = 2.2
                    self.locked = False
                else:
                    self.landing = False

                self.move(self.lock * -1 * (self.locked_distance / self.get_jump_distance() * 1.1) * self.king_jump_velocity * self.dt)
            else:
                self.pause += self.pause_inc * self.dt
            
            if self.pause >= self.pause_end:
                self.can_jump = True
                self.king_velocity = 0
                self.pause = 0

        # checks whether the king is in the air or not
        if self.king_height > 0:
            self.in_air = True
        else:
            self.in_air = False


    def check_in_air(self):
        return self.in_air
    
    def check_if_land(self):
        if self.king_height == 0 and not self.landed:
            self.landed = True
            self.just_landed = True
            return self.just_landed 
        
        elif self.king_height == 0 and self.landed:
            self.just_landed = False
            return self.just_landed
        else:
            self.landed = False
            self.just_landed = False
            return self.just_landed

    
    def translate(self, direction):
        self.center += direction 
        for i in range(len(self.vertices)):
            self.vertices[i] += direction 

    def attacks(self, dt):
        if self.summoned and not self.dead:
            self.directional_attack()
            self.half_square_attack(dt)
    
    
    def follow_player(self, player_center):
        v = self.center - player_center
        v = v.normalize()
        self.looking = v
        angle = math.atan2(v.x, v.y)
        angle = angle * 180 / math.pi
        self.to_render.angle = angle + 90
    
    def track_player(self, player_center):
        v = self.center - player_center
        v = v.normalize()
        # self.looking = v
        angle = math.atan2(v.x, v.y)
        angle = angle * 180 / math.pi
        self.to_render.angle = angle - 45
        return v
    

    def directional_attack(self):
        if self.just_landed:
            while self.boss_angle_degrees < 360:
                self.s = Vector(math.cos(self.s_x), math.sin(self.s_y))
                g = math.atan2(self.s.y, self.s.x) - self.angle * math.pi / 180
                a = (360 + (g * 180 / math.pi)) * math.pi / 180
                x, y = math.cos(a), math.sin(a)
                self.s = Vector(x, y)


                shot_5 = SwordShot([self.center.x, self.center.y], 16, 16, blue, self.s, sword_angle_start=0)
                shot_5.sword_angle_start = math.atan2(self.s.y, self.s.x) + self.angle * math.pi / 180
                shot_5.sword_velocity = 1

                
                self.boss_angle_degrees += self.boss_angle_degrees_increment
                self.number_of_eight_shots += 1

                self.s_x, self.s_y = self.boss_angle_degrees * math.pi / 180, self.boss_angle_degrees * math.pi / 180
                shot_5.damage = 5
                self.bullets.append(shot_5)

            self.boss_angle_degrees %= 360


    def half_square_attack(self, dt):
        if self.summoned and not self.dead:
            self.sword_attack_timer.start_timer(dt)
            self.sword_show_timer.start_timer(dt)
            if self.sword_show_timer.alarm:
                self.sword_show()
                self.sword_show_timer.reset_timer()
                self.sword_show_timer.active = False

            if self.sword_attack_timer.alarm:
                for sword in self.bullets:
                    sword.sword_velocity = sword.sword_velocity_og
                self.sword_attack_timer.reset_timer()
                self.sword_show_timer.active = True

    def sword_show(self):
        self.throwing_point = random.randint(0, 1)
        num_of_swords = 11 # how many swords per side are summoned
        skip = random.randint(1, num_of_swords - 2) # creates a gap that players can pass through
        half_sword_damage = 5

        for i in range(num_of_swords):
            if i == skip:
                continue
            point = [self.throwing_points[self.throwing_point][0] + i * 25, self.throwing_points[self.throwing_point][1]]
            upright = vec_to_mid(point)
            shot = SwordShot(point, 24, 11, black, upright, math.atan2(upright.y, upright.x) + self.angle * math.pi / 180)
            shot.sword_velocity = 0
            shot.damage = half_sword_damage
            self.bullets.append(shot)
        self.throwing_point = random.randint(0, 1)
        for i in range(num_of_swords):
            if i == skip or i == skip + 1:
                continue
            point = [self.throwing_points_vertical[self.throwing_point][0], self.throwing_points_vertical[self.throwing_point][1] + i * 25]
            upright = vec_to_mid(point)
            shot = SwordShot(point, 24, 11, black, upright, math.atan2(upright.y, upright.x) + self.angle * math.pi / 180)
            shot.damage = half_sword_damage
            shot.sword_velocity = 0
            self.bullets.append(shot)

        

    
    def render(self, surface):
        self.to_render.images = self.images[self.summon_index:self.num_images]
        for i, img in enumerate(self.to_render.images):
            img.convert_alpha()
            rotated_img = pygame.transform.rotate(img, self.to_render.angle)
            surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - self.king_height - rotated_img.get_height() // 2 - i * self.spread))
    

    def death(self):
        self.images = barrelking_images
        self.dead = True
        for sword in self.bullets: # this is so that in the half sqaure attack the swords floating wont get stuck after the boss dies
            sword.sword_velocity = sword.sword_velocity_og

    def get_jump_distance(self):
        initial_vertical_velocity = 2.2
        horizontal_velocity = self.king_jump_velocity
        gravity = 0.1
        time_up = initial_vertical_velocity / gravity
        total_air_time = 2 * time_up
        horizontal_distance = horizontal_velocity * total_air_time
        return horizontal_distance