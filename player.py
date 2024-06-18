from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
import math


display_center_x = 200
display_center_y = 200


class Player(Hitbox):
    def __init__(self, center, width, height, color, health=100):
        super().__init__(center, width, height, color)
        self.images = player_images
        self.spread = 1
        # self.direction = Vector((0, 0))
        self.to_render = Render(self.images, center, self.angle, self.spread)

        self.health = health

        self.health_bar = HealthBar(self.health, color)
        self.looking = Vector((0, 0))

        # how fast the camera returns to the player
        self.scroll_speed = 0.02

        self.knockback_power = 5
        self.knockback = False
        self.knock_start = 0
        self.knock_end = 6
        self.knock_increment = 1


        self.inventory = {
            "Arrows" : []
        }



    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)

    def update(self, rotation_input): # order matters here so images dont move first
        self.handle_rotation(rotation_input, player=True)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

    def update_actions(self, action_input):
        if action_input["shootlock"]:
            self.looking = self.looking
        else:
            self.looking = self.last_looked

    def check_knockback(self):
        if self.knock_start < self.knock_end:
            self.knock_start += self.knock_increment
        else:
            self.knock_start = 0
            self.knockback = False

        if self.knockback == True:
            self.knock_start += self.knock_increment
            self.move(self.looking * -1 * self.knockback_power)

    def damage(self, damage):
        self.health -= damage
        self.health_bar.damage(damage)



class PlayerArrow(Hitbox):
    def __init__(self, center, width, height, color):
        super().__init__(center, width, height, color)
        self.image = arrow_img
        self.arrow_angle = 0
        self.arrow_difference = 0
        self.arrow_angle_degrees = 0

        

    def update(self, direction, player_center):
        self.arrow_angle = math.atan2(direction.y, direction.x)
        self.arrow_angle_degrees = -self.arrow_angle * 180 / math.pi
        self.arrow_rotation(self.arrow_angle + self.arrow_difference)
        self.arrow_difference = -self.arrow_angle

        

    def render(self, surface):
        rotated_img = pygame.transform.rotate(self.image, self.arrow_angle_degrees)
        surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - rotated_img.get_height() // 2))


    def arrow_rotation(self, angle):
        self.center.x, self.center.y = (self.center.x - display_center_x) * math.cos(angle) + (self.center.y - display_center_x) * -math.sin(angle) + display_center_x, (self.center.x - display_center_x) * math.sin(angle) + (self.center.y - display_center_x) * math.cos(angle) + display_center_x
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - display_center_x) * math.cos(angle) + (self.vertices[i].y - display_center_x) * -math.sin(angle) + display_center_x, (self.vertices[i].x - display_center_x) * math.sin(angle) + (self.vertices[i].y - display_center_x) * math.cos(angle) + display_center_x


    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y
