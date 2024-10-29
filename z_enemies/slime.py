from z_extensions.render import *
from z_extensions.Square import Hitbox
from z_health.health import HealthBar
from z_extensions.vector import Vector
from z_health.health import HealthBar
import math

class Slime(Hitbox):
    def __init__(self, center, width, height, color, looking, player_center, health=30):
        super().__init__(center, width, height, color)

        self.images = [img.convert_alpha() for img in slime_images]
        self.slime_velocity_max = .01
        self.slime_velocity = self.slime_velocity_max
        self.slime_looking = looking
        self.slime_angle = math.atan2(looking.y, looking.x) # gets the direction facing and rotates slime to point that direction
        self.slime_angle_start = self.slime_angle
        self.set_angle(self.slime_angle) # sets the direction of all the vertices to face the right way
        self.spread = 1
        self.to_render = Render(self.images, center, self.slime_angle, self.spread)
        self.health_bar = HealthBar(health, indigo)

        self.slime_height = 0
        self.time = 0

        self.gravity = .1
        self.speed = 2.2

        self.damage = 2
        self.distance = 50

        self.landing = False


        self.can_jump = False
        self.pause = 0
        self.pause_end = 60
        self.pause_inc = 1

        self.locked = False
        self.lock = Vector(0, 0)



    def spawn(self, vector): # vector is pointing to where the player is
        pass

    def track_player(self, player_center):
        v = self.center - player_center
        v = v.normalize()
        # self.looking = v
        angle = math.atan2(v.x, v.y)
        angle = angle * 180 / math.pi
        self.to_render.angle = angle - 45
        return v
    

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)



    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y

    def render(self, surface):
        for i, img in enumerate(self.images):
            img.convert_alpha()
            rotated_img = pygame.transform.rotate(img, self.slime_angle)
            surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - self.slime_height - rotated_img.get_height() // 2 - i * self.spread))


    def jump(self):
        self.slime_velocity = self.slime_velocity_max
        self.slime_height += self.speed
        self.speed -= self.gravity
        if self.slime_height < 0:
            self.landing = True
            self.can_jump = False
            self.slime_height = 0
            self.speed = 2.2
            self.locked = False

        



    def handle_rotation_slime(self, rotation_input):
        if not rotation_input["reset"]: # have to do this because it interferes with the slime rotation (might have to do it with everything else to make it cleaner)
            self.handle_rotation(rotation_input)


        if rotation_input["reset"]:
            if self.slime_angle != self.slime_angle_start:
                self.reset_slime_rotation()
                self.slime_angle = self.slime_angle_start
            return # so no continuous rotation


        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.slime_angle -= self.rotationspeed
            elif rotation_input["clockwise"]:
                self.slime_angle += self.rotationspeed


    def reset_slime_rotation(self):
        back = -(self.slime_angle - self.slime_angle_start)
        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(back) + (self.center.y - mid_y) * -math.sin(back) + mid_x, (self.center.x - mid_x) * math.sin(back) + (self.center.y - mid_y) * math.cos(back) + mid_y
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(back) + (self.vertices[i].y - mid_y) * -math.sin(back) + mid_x, (self.vertices[i].x - mid_x) * math.sin(back) + (self.vertices[i].y - mid_y) * math.cos(back) + mid_y
        
    def update(self, rotation_input, direction, player_center):

        if self.can_jump:
            if self.locked == False:
                # print('locking')
                self.lock = self.track_player(player_center)
                self.locked = True

            # print(self.lock.point)
            self.jump()
            self.move(self.lock * -1 * self.velocity) # have to multiply player velocity as well???

        else:
            self.pause += self.pause_inc

        if self.pause >= self.pause_end:
            self.can_jump = True
            self.slime_velocity = 0
            self.pause = 0
            

        self.translate(Vector(math.cos(self.slime_angle), math.sin(self.slime_angle)) * self.slime_velocity)
        self.move(direction * -1 * self.velocity)
        self.handle_rotation_slime(rotation_input)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = -self.slime_angle * 180 / math.pi


    def translate(self, direction):
        self.center += direction 
        for i in range(len(self.vertices)):
            self.vertices[i] += direction 


