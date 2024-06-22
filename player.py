from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
import math


display_center_x = 200
display_center_y = 200


class Player(Hitbox):
    def __init__(self, center, width, height, color, health=200):
        super().__init__(center, width, height, color)
        self.images = player_images
        self.spread = 1
        self.direction = Vector((0, 0))
        self.to_render = Render(self.images, center, self.angle, self.spread)
        self.spawnpoint = Hitbox((0, 0), 1, 1, (0, 0, 0))

        self.original_health = health
        self.health = health

        self.health_bar = HealthBar(self.health, color)
        self.looking = Vector((0, 0))

        # how fast the camera returns to the player
        self.scroll_speed = 0.02


        self.dead = False

        # default stats for the player


        self.knockback_power = 5
        self.knockback = False
        self.knock_start = 0
        self.knock_end = 6
        self.knock_increment = 1
        

        self.dash_speed = 1
        self.dash_friction = .03
        self.dash_start = 0
        self.dash_end = 12
        self.dash_increment = 1

        self.tracking = True

        self.inventory = {
            "Arrows" : [],
            "Watermelons": []
        }


        self.barrels_busted = 0

        self.stats = {
            'M' : 100,
            'R' : 50
        }

        # self.arrow_multiplier = 1

        self.arrow_counter = 0


    def player_death(self):
        self.health_bar.set_health(self.original_health)

        # probably reset their stats or something
        # keep barrels busted the same

        pass

    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)

    def update(self, rotation_input, action_input, direction): # order matters here so images dont move first
        self.handle_rotation(rotation_input, player=True)
        self.handle_dash(action_input, direction)
        self.collectables_follow(rotation_input, direction)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

    
    def update_away(self, rotation_input, action_input, direction):
        self.handle_rotation(rotation_input)
        self.handle_dash(action_input, direction)
        self.collectables_follow(rotation_input, direction)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

    def update_spawnpoint(self, rotation_input, direction):
        self.spawnpoint.handle_rotation(rotation_input)
        self.spawnpoint.move(direction * -1)

    def handle_dash(self, action_input, direction):
        if self.dash_start == self.dash_end:
            self.dash_start = 0
            self.dash_speed = 1
            action_input["dash"] = False
            return
        if action_input["dash"]:
            self.dash_start += self.dash_increment
            self.dash_speed -= self.dash_friction
            if direction.x == 0 and direction.y == 0:
                direction *= self.dash_speed
            self.move(direction)
        

    def update_actions(self, action_input):
        if not action_input["lock"]:
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

    def shoot(self, arrows):
        pass

    def collectables_follow(self, rotation_input, direction):
        for items, holder in self.inventory.items():
            for i in range(len(holder)):
                diff_vec = Vector((self.center.x - holder[i].center.x, self.center.y - holder[i].center.y))
                holder[i].move(diff_vec * holder[i].follow_speed)
                holder[i].update(rotation_input, direction)

        




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
