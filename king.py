from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
from timer import Timer
from uno import Shuriken
import particles as particles
import random
import math


class King(Hitbox):
    def __init__(self, center, width, height, color, looking, name, health=500):
        super().__init__(center, width, height, color)
        self.health = health 

        self.images = [img.convert_alpha() for img in barrelking_images]

        self.attack_damage = 50

        self.spread = 1.6
        self.to_render = Render(self.images, center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)

        self.num_images = len(self.images)

        self.shoot_angle_degrees = 45
        self.shoot_angle_radians = 0

        self.start_shoot_angle = 10

        self.turn_angle_degrees = 1

        self.delete_radius = 500

        
        self.summon_rise = 5 # layer appears every 15 frames (4 layers every second)

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


        self.activate = 100 # activates after breaking this many barrels


        self.closest_to_player = False


        self.bullets = []
        self.sword_show_timer = Timer(120) # 75
        self.sword_attack_timer = Timer(240) # 120

        self.spiral_show_timer = Timer(1)
        self.sprial_attack_timer = Timer(1)

        self.throwing_point = 0
        self.throwing_points = [[mid_x - 150, mid_y + 150],
                                [mid_x - 150, mid_y - 150]]
        self.throwing_points_vertical = [[mid_x + 150, mid_y - 150],
                                        [mid_x - 150, mid_y - 150]]
        

        self.throwing_point_spiral = pygame.Vector2(1, 0)
        
        self.throw_swords = False
        self.throwing_timer = Timer(120)


        self.king_height = 0
        self.landing = False
        self.can_jump = False
        self.locked = False
        self.lock = Vector(0, 0)

        self.king_velocity_max = 0.01
        self.king_velocity = self.king_velocity_max
        self.speed = 2.2
        self.gravity = 0.1


        self.pause = 0
        self.pause_end = 60
        self.pause_inc = 1


        self.king_angle = math.atan2(looking.y, looking.x)
        self.king_angle_start = self.king_angle
        self.king_angle_start = self.king_angle
        self.set_angle(self.king_angle)



        self.eight_directions = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4]
        self.eight_shot = False



    def check_if_summon(self):
        if not self.summoned and not self.summoning:
            if self.barrels_busted >= self.activate and not self.summoned:
                self.summoning = True
                self.tracking = True
                return True

        if self.summoning:
            self.can_jump = False
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

        return False
    
    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y
    
    def jump(self):
        self.king_velocity = self.king_velocity_max
        self.king_height += self.speed
        self.speed -= self.gravity
        if self.king_height < 0:
            self.landing = True
            self.can_jump = False
            self.king_height = 0
            self.speed = 2.2
            self.locked = False
        else:
            self.landing = False


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
        for i, img in enumerate(self.to_render.images):
            img.convert_alpha()
            rotated_img = pygame.transform.rotate(img, self.king_angle)
            surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - self.king_height - rotated_img.get_height() // 2 - i * self.spread))
    
    def follow_player(self, player_center):
        v = self.center - player_center
        v = v.normalize()
        self.looking = v
        angle = math.atan2(v.x, v.y)
        angle = angle * 180 / math.pi
        self.to_render.angle = angle + 90


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


    def update(self, rotation_input, input, direction, player_center):
        # self.get_direction(input)
        # self.handle_rotation(rotation_input)
        # self.move(direction * -1)

        if self.can_jump:
            if self.locked == False:
                self.lock = self.track_player(player_center)
                self.locked = True
            self.jump()
            self.move(self.lock * -1 * self.velocity)
        else:
            self.pause += self.pause_inc
        
        if self.pause >= self.pause_end:
            self.can_jump = True
            self.king_velocity = 0
            self.pause = 0

        self.translate(Vector(math.cos(self.king_angle), math.sin(self.king_angle)) * self.king_velocity)
        self.move(direction * -1 * self.velocity)
        self.handle_rotation_king(rotation_input)

        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle
        # self.locked.update(rotation_input, direction)

    
    def track_player(self, player_center):
        v = self.center - player_center
        v = v.normalize()
        # self.looking = v
        angle = math.atan2(v.x, v.y)
        angle = angle * 180 / math.pi
        self.to_render.angle = angle - 45
        return v

    def handle_rotation_king(self, rotation_input):
        if not rotation_input["reset"]: # have to do this because it interferes with the king rotation (might have to do it with everything else to make it cleaner)
            self.handle_rotation(rotation_input)


        if rotation_input["reset"]:
            if self.king_angle != self.king_angle_start:
                self.reset_king_rotation()
                self.king_angle = self.king_angle_start
            return # so no continuous rotation


        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.king_angle -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.king_angle += self.rotationspeed


    def reset_king_rotation(self):
        back = -(self.king_angle - self.king_angle_start)
        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(back) + (self.center.y - mid_y) * -math.sin(back) + mid_x, (self.center.x - mid_x) * math.sin(back) + (self.center.y - mid_y) * math.cos(back) + mid_y
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(back) + (self.vertices[i].y - mid_y) * -math.sin(back) + mid_x, (self.vertices[i].x - mid_x) * math.sin(back) + (self.vertices[i].y - mid_y) * math.cos(back) + mid_y
        

    def damage(self, dmg):
        if not self.summoned:
            pass
        else:
            self.health_bar.damage(dmg)

    def attacks(self, dt, particles):
        if self.summoned and not self.dead:
            # self.half_square_attack(dt)
            # self.landing_attack(dt)
            # self.spiral_attack(dt)
            self.directional_attack()

    def translate(self, direction):
        self.center += direction 
        for i in range(len(self.vertices)):
            self.vertices[i] += direction 
        

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

    def spiral_attack(self, dt):
        self.sprial_attack_timer.start_timer(dt)
        self.spiral_show_timer.start_timer(dt)

        if self.spiral_show_timer.alarm:
            self.spiral_attack_show()
            self.spiral_show_timer.reset_timer()
            self.spiral_show_timer.active = False
        if self.sprial_attack_timer.alarm:
            for sword in self.bullets:
                sword.sword_velocity = sword.sword_velocity_og
            self.sprial_attack_timer.reset_timer()
            self.spiral_show_timer.active = True

    def directional_attack(self):
        if self.king_height == 0 and not self.eight_shot:
            self.eight_shot = True
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
        else:
            self.eight_shot = False

    def landing_attack(self, dt):
        print(self.pause)

        if self.pause > 50:
            radius = 100 # distance sword is thrown from player
            throw_point = self.throwing_point_spiral * radius + pygame.Vector2(200, 200)
            direction = self.throwing_point_spiral
            self.throwing_point_spiral = self.throwing_point_spiral.rotate(12)  
            shot = SwordShot(throw_point, 24, 11, black, direction, math.atan2(direction.y, direction.x) + self.angle * math.pi /180)
            shot.sword_velocity = 1
            shot.damage = 0

            self.bullets.append(shot)
        
        # if self.king_height == 0 and not self.eight_shot: # the king is on the floor
        #     self.eight_shot = True
        #     for direction in self.eight_directions:
        #         sin = math.sin(direction)
        #         cos = math.cos(direction)
        #         shot = SwordShot([self.center.x, self.center.y], 24, 11, black, Vector(sin, cos), math.atan2(cos, sin) + self.angle * math.pi / 180)
        #         shot.sword_velocity = 0
        #         shot.damage = 0
        #         shot.sword_velocity = 1
        #         self.bullets.append(shot)
        
        # if not self.landing:
        #     self.eight_shot = False 

        # self.s = Vector(math.cos(self.s_x), math.sin(self.s_y))
        # g = math.atan2(self.s.y, self.s.x) - self.angle * math.pi / 180
        # a = (360 + (g * 180 / math.pi)) * math.pi / 180
        # x, y = math.cos(a), math.sin(a)
        # self.s = Vector(x, y)


        # shot_5 = SwordShot([self.center.x, self.center.y], 16, 16, black, self.s, 0)
        # shot_5.sword_angle_start = math.atan2(self.s.y, self.s.x) + self.angle * math.pi / 180
        # shot_5.damage = 0
        # self.boss_angle_degrees += self.boss_angle_degrees_increment
        # self.s_x, self.s_y = self.boss_angle_degrees * math.pi / 180, self.boss_angle_degrees * math.pi / 180

        # self.bullets.append(shot_5)

        # point = [self.center.x, self.center.y]
        # upright = self.vec_to_mid(point)
        # upright = upright
        # shot = SwordShot(point, 24, 11, black, upright, math.atan2(upright.y, upright.x) + self.angle * math.pi / 180)
        # shot.sword_velocity = 1
        # shot.damage = 0
        # print(point)
        # self.bullets.append(shot)



        





    def spiral_attack_show(self):
        radius = 100 # distance sword is thrown from player
        throw_point = self.throwing_point_spiral * radius + pygame.Vector2(200, 200)
        direction = -self.throwing_point_spiral
        self.throwing_point_spiral = self.throwing_point_spiral.rotate(12)  
        shot = SwordShot(throw_point, 24, 11, black, direction, math.atan2(direction.y, direction.x) + self.angle * math.pi /180)
        shot.sword_velocity = 0
        shot.damage = 0

        self.bullets.append(shot)

        

    def sword_show(self):
        self.throwing_point = random.randint(0, 1)
        num_of_swords = 11 # how many swords per side are summoned
        skip = random.randint(1, num_of_swords - 2) # creates a gap that players can pass through

        for i in range(num_of_swords):
            if i == skip:
                continue
            point = [self.throwing_points[self.throwing_point][0] + i * 25, self.throwing_points[self.throwing_point][1]]
            upright = self.vec_to_mid(point)
            shot = SwordShot(point, 24, 11, black, upright, math.atan2(upright.y, upright.x) + self.angle * math.pi / 180)
            shot.sword_velocity = 0
            self.bullets.append(shot)
        self.throwing_point = random.randint(0, 1)
        for i in range(num_of_swords):
            if i == skip or i == skip + 1:
                continue
            point = [self.throwing_points_vertical[self.throwing_point][0], self.throwing_points_vertical[self.throwing_point][1] + i * 25]
            upright = self.vec_to_mid(point)
            shot = SwordShot(point, 24, 11, black, upright, math.atan2(upright.y, upright.x) + self.angle * math.pi / 180)
            shot.sword_velocity = 0
            self.bullets.append(shot)


    def vec_to_mid(self, point):
        return Vector(200 - point[0], 200 - point[1]).normalize()
        
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



            


    def delete_shuriken(self, shuriken_to_delete):
        for i in range(len(self.bullets)):
            if self.bullets[i] == shuriken_to_delete:
                del self.bullets[i]
                return



class SwordShot(Hitbox):
    def __init__(self, center, width, height, color, looking, sword_angle_start):
        super().__init__(center, width, height, color)
        
        self.images = swordshot_image.convert_alpha()
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


    
