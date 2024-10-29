from z_extensions.render import *
from z_extensions.Square import Hitbox
from z_extensions.vector import Vector
from z_health.health import HealthBar
from z_throwables.bullets import Shuriken
import math

mid_x = 200
mid_y = 200


class Uno(Hitbox):
    def __init__(self, center, width, height, color, name, health=1000):
        super().__init__(center, width, height, color)
        self.health = health
        self.images = [img.convert_alpha() for img in Uno_images]
        self.num_images = len(self.images)

        self.spread = 1.3
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)


        self.shoot_angle_degrees = 45
        self.shoot_angle_radians = 0

        self.start_shoot_angle = 10

        self.turn_angle_degrees = 1

        self.delete_radius = 200

        
        self.summon_rise = 10 # layer appears every 15 frames (4 layers every second)

        self.summoning = False
        self.summon_start = 0
        self.summon_end = self.num_images * self.summon_rise
        self.summon_index = self.num_images
        self.summoned = False


        self.looking = Vector(0, 0)
        self.locked = Vector(0, 0)


        self.charge_now = False
        self.charging = False
        self.charge_start = 0
        self.charge_end = 45
        self.charge_inc = 1
        self.charge_speed = 1

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


        self.attack_start = 0
        self.attack_end = 8

        self.activate = 10 # 10


        self.closest_to_player = False


    def check_if_summon(self):
        if not self.summoned and not self.summoning and not self.dead:
            if self.barrels_busted >= self.activate and not self.summoned:
                self.summoning = True
                self.tracking = True
                return True

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
        return False
        

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
        if self.closest_to_player:
            white_bar_width = 180
            white_bar_height = 16


            width = self.health_bar.health / self.health_bar.maxhealth * 180
            center = Vector(mid_x, 30)
            
            margin_top_bottom = 2
            margin_left_right = 2

            render_text((center.x - len(self.name) * 7 / 2, 10), self.name, surface, "white")
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

    def attacks(self, dt):
        self.attack_start += dt
        if self.attack_start >= self.attack_end:
            self.attack_start = 0
            if self.summoned and not self.dead:
                self.spiral_attack()
                self.directional_attack()
        
        if self.summoned and not self.dead and self.health_bar.health < self.health_bar.maxhealth // 2:
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
        self.locked = self.looking
        self.charging = True

        self.charge()


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


    def charge(self):
        if self.charging:
            self.charge_start += self.dt

            self.move(self.locked * -1 * self.charge_speed * self.dt)

            shot = Shuriken([self.center.x, self.center.y], 16, 16, blue, self.last_looked)
            shot.shuriken_angle_start = math.atan2(self.last_looked.y, self.last_looked.x) + self.angle * math.pi / 180
            shot.shuriken_velocity = 4
            self.bullets.append(shot)



    def delete_shuriken(self, shuriken_to_delete):
        for i in range(len(self.bullets)):
            if self.bullets[i] == shuriken_to_delete:
                del self.bullets[i]
                return


