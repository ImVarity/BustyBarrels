from mod import Boss
from Square import Hitbox
from vector import Vector
from health import HealthBar
from uno import Shuriken
from king import SwordShot
from render import *
import math





class Kingv2(Boss):
    def __init__(self, center, width, height, color, name, health=1000):
        super().__init__(center, width, height, color, name, health)
        self.images = [img.convert_alpha() for img in barrelking_images]
        self.num_images = len(self.images)
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.summon_end = self.num_images * self.summon_rise
        self.activate = 1



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


        self.eight_shot = False
        self.number_of_eight_shots = 0

    def update(self, rotation_input, input, direction, player_center):
        if self.can_jump:
            if self.locked == False:
                self.lock = self.track_player(player_center)
                self.locked = True
            self.jump()
            self.move(self.lock * -1 * 2)
        else:
            self.pause += self.pause_inc
        
        if self.pause >= self.pause_end:
            self.can_jump = True
            self.king_velocity = 0
            self.pause = 0

        
        self.move(direction * -1 * self.velocity)
        self.get_direction(input)
        self.handle_rotation(rotation_input)

        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

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

    def translate(self, direction):
        self.center += direction 
        for i in range(len(self.vertices)):
            self.vertices[i] += direction 

    def attacks(self, dt):
        if self.summoned and not self.dead:
            print(self.center)
            self.directional_attack()
    
    
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
        if self.king_height == 0 and not self.eight_shot:
            self.eight_shot = True
            self.s = Vector(math.cos(self.s_x), math.sin(self.s_y))
            g = math.atan2(self.s.y, self.s.x) - self.angle * math.pi / 180
            a = (360 + (g * 180 / math.pi)) * math.pi / 180
            x, y = math.cos(a), math.sin(a)
            self.s = Vector(x, y)


            shot_5 = SwordShot([self.center.x, self.center.y], 16, 16, blue, self.s, sword_angle_start=0)
            shot_5.sword_angle_start = math.atan2(self.s.y, self.s.x) + self.angle * math.pi / 180
            shot_5.sword_velocity = 1

            
            self.boss_angle_degrees += self.boss_angle_degrees_increment
            self.boss_angle_degrees %= 360
            self.number_of_eight_shots += 1

            self.s_x, self.s_y = self.boss_angle_degrees * math.pi / 180, self.boss_angle_degrees * math.pi / 180
            shot_5.damage = 0
            self.bullets.append(shot_5)
    

        if self.number_of_eight_shots < 8:
            self.eight_shot = False
        
        if not self.landing:
            self.eight_shot = False
            self.number_of_eight_shots = 0

    
    def render(self, surface):
        self.to_render.images = self.images[self.summon_index:self.num_images]
        for i, img in enumerate(self.to_render.images):
            img.convert_alpha()
            rotated_img = pygame.transform.rotate(img, self.to_render.angle)
            surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - self.king_height - rotated_img.get_height() // 2 - i * self.spread))
    