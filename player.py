from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
import math



class Player(Hitbox):
    def __init__(self, center, width, height, color, health=200):
        super().__init__(center, width, height, color)
        self.images = [img.convert_alpha() for img in player_images]
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
            "Watermelons": [],
            "Powerups" : []
        }

        self.active_quest_code = ""
        self.active_quest = ""
        self.barrels_busted = 0
        self.quest_barrels_busted = 0
        self.inQuest = False


        self.quest_completed = False
        self.quest_complete_text_start = 0
        self.quest_complete_text_speed = 2
        self.quest_complete_text_friction = .05

        self.bomber = False # can throw bombs
 
        self.power_up = False
        self.power_up_text_start = 0
        self.power_up_text_end = 300
        self.power_up_text_inc = 1
        

        self.stats = {
            'M' : 1000,
            'R' : 200
        }

        # self.arrow_multiplier = 1

        self.arrow_counter = 0


        self.in_water = False

        self.shot = False



        self.damage_taken = []
        self.damage_flash = False
        self.damage_flash_counter = 0

    def player_death(self):
        self.health_bar.set_health(self.original_health)
        self.inventory["Arrows"] = self.inventory["Arrows"][:len(self.inventory["Arrows"])//2]
        self.inventory["Watermelons"] = self.inventory["Watermelons"][:len(self.inventory["Watermelons"])//2]

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
        self.handle_damage()
        self.update_actions(action_input)
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

    def handle_damage(self):
        for damage in self.damage_taken:
            damage.update([self.center.x, self.center.y])

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

    def damage(self, damage, surface):
        self.damage_taken.append(DamageNumber(damage, [self.center.x, self.center.y]))
        self.health -= damage
        self.health_bar.damage(damage)
        self.damage_flash = True

    
    def draw_damage(self, surface):
        for i in range(len(self.damage_taken) -1, -1, -1):
            self.damage_taken[i].draw(surface)
            if self.damage_taken[i].height >= self.damage_taken[i].disappear_counter:
                del self.damage_taken[i]

        if self.damage_flash:
            damage_surface = pygame.Surface((mid_x * 2, mid_y * 2), pygame.SRCALPHA).convert_alpha()
            damage_surface.fill(damage_color)
            surface.blit(damage_surface, (0, 0))
            self.damage_flash_counter += 1
        if self.damage_flash_counter > 5:
            self.damage_flash = False
            self.damage_flash_counter = 0

        

    def shoot(self, arrows):
        pass

    def collectables_follow(self, rotation_input, direction):
        for items, holder in self.inventory.items():
            for i in range(len(holder)):
                diff_vec = Vector((self.center.x - holder[i].center.x, self.center.y - holder[i].center.y))
                holder[i].move(diff_vec * holder[i].follow_speed)
                holder[i].update(rotation_input, direction,)
    

    def quest_complete_text(self, surface):
        if self.quest_completed:
            render_text((mid_x - len("Quest Comepleted") * 7 / 2, mid_y - self.quest_complete_text_start), "Quest Completed", surface, "white")
            self.quest_complete_text_start += self.quest_complete_text_speed
            self.quest_complete_text_speed  -= self.quest_complete_text_friction
        if self.quest_complete_text_start < -200:
            self.quest_completed = False
            self.quest_complete_text_start = 0
            self.quest_complete_text_speed = 2

    def powerup_collected(self, surface, powerup):
        if self.power_up:
            powerup.render(surface)
            npc_surface = pygame.Surface((mid_x * 2, mid_y * 2), pygame.SRCALPHA).convert_alpha()
            npc_surface.fill(npc_color)
            surface.blit(npc_surface, (0, 0))
            render_text((mid_x - len("POWERUP") * 7 / 2, mid_y - 100), "POWERUP", surface, "white")
            render_text((mid_x - len("PRESS SPACE TO USE") * 7 / 2, mid_y - 50), "PRESS SPACE TO USE", surface, "white")
            self.power_up_text_start += self.power_up_text_inc
            
        if self.power_up_text_start == self.power_up_text_end:
            self.power_up = False
            self.power_up_text_start = 0



class DamageNumber:
    def __init__(self, damage, loc) -> None:

        self.loc = loc
        self.number = damage

        # how how above player numer starts
        self.height = 5
        self.width = 0
        self.disappear_counter = 13
        self.rise_speed = .5

    def update(self, loc):
        self.loc[0] = loc[0]
        self.loc[1] = loc[1]
        self.height += self.rise_speed
        

    def draw(self, surface):
        render_text_centered((self.loc[0] + self.width, self.loc[1] - self.height), str(self.number), surface, "red")


class PlayerArrow(Hitbox):
    def __init__(self, center, width, height, color):
        super().__init__(center, width, height, color)
        self.image = arrow_img.convert_alpha()
        self.arrow_angle = 0
        self.arrow_difference = 0
        self.arrow_angle_degrees = 0

        

    def update(self, direction):
        self.arrow_angle = math.atan2(direction.y, direction.x)
        self.arrow_angle_degrees = -self.arrow_angle * 180 / math.pi
        self.arrow_rotation(self.arrow_angle + self.arrow_difference)
        self.arrow_difference = -self.arrow_angle
        

        

    def render(self, surface):
        rotated_img = pygame.transform.rotate(self.image, self.arrow_angle_degrees)
        surface.blit(rotated_img, (self.center.x - rotated_img.get_width() // 2 , self.center.y - rotated_img.get_height() // 2))


    def arrow_rotation(self, angle):
        self.center.x, self.center.y = (self.center.x - mid_x) * math.cos(angle) + (self.center.y - mid_x) * -math.sin(angle) + mid_x, (self.center.x - mid_x) * math.sin(angle) + (self.center.y - mid_x) * math.cos(angle) + mid_x
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - mid_x) * math.cos(angle) + (self.vertices[i].y - mid_x) * -math.sin(angle) + mid_x, (self.vertices[i].x - mid_x) * math.sin(angle) + (self.vertices[i].y - mid_x) * math.cos(angle) + mid_x


    def set_angle(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(angle) + (self.vertices[i].y - self.center.y) * -math.sin(angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(angle) + (self.vertices[i].y - self.center.y) * math.cos(angle) + self.center.y
