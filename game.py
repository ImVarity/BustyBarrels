import pygame
from render import *
from pygame.locals import *
import pygame
import math
import bisect
import random
from Square import Hitbox
from vector import Vector
from arrow import Arrow
from barrel import Barrel
from player import Player
from player import PlayerArrow
from collectable import Collectable
from npc import NPC
from uno import Uno
from particles import Particle
from slime import Slime
from bomb import Bomb
from tile import Tile
from render import *
import time

MAX_ARROW_COUNT_COLLECTABLES = 75
MAX_BARREL_COUNT_COLLECTABLES = 75

class GameLoop:
    def __init__(self) -> None:
        
        self.save_files = {}

        self.dt = 1

        self.direction = Vector(0, 0)
        self.paused = False

        self.player = Player([0, 0], 8, 8, blue, health=500)
        self.player_arrow = PlayerArrow([mid_x + 12, mid_y], 16, 16, blue)
        self.spawnpoint = Barrel((0, 0), 8, 8, black)
        self.tif_spawnpoint = Barrel([mid_x + 16, mid_y + 16], 8, 8, black)

        # Camera
        self.camera_follow = self.player

        self.to_render = []
        self.boxes = []
        self.arrows = []
        self.bombs = []
        self.watermelons = []


        self.barrels = [
            Barrel([250, 150], 16, 16, pink, health=500),
            Barrel([150, 250], 16, 16, pink, health=500),
            Barrel([250, 250], 16, 16, pink, health=500)
        ]

        self.collectables = {
            "Arrows" : [],
            "Watermelons" : [],
            "Powerups" : []
        }

        self.inputs = {
            "Movements" : {
                "up" : False,
                "down" : False,
                "left" : False,
                "right" : False,
            },
            "Rotation" : {
                "reset" : False,
                "clockwise" : False,
                "counterclockwise" : False
            },
            "Action" : {
                "lock" : False,
                "ultimate" : False,
                "shoot" : False,
                "autofire": False,
                "dash": False,
                "throw" : False,
                "interact" : False
            },
            "Admin" : {
                "hitboxes" : False
            },
            "HUD" : {
                "stats" : False
            }
        }


        self.collidables = {
            "Barrels": [],
            "Arrows" : [],
            "Shurikens" : [],
            "Bombs" : [],
            "Bosses" : [],
            "Water" : [],
            "Boundary": []
        }

        # just put player in here immediately, it will be sorted in place anyway
        self.to_render_sorted = [self.player]


    # Gets the direction that the player is moving
    def initialize_direction(self):
        self.direction = self.player.get_direction(self.inputs["Movements"]) * self.dt
        self.player.direction = self.direction
    
    def main(self, dt, display): # -> dict[str]:
        self.set_delta_time(dt)
        self.initialize_direction()

        if not self.paused:
            self.update_player()
            self.camera_tracking()
            self.update_arrows()
            self.update_barrels()
            self.update_enemies()





            self.shoot_arrow()


            # Spawning collectables
            self.add_collectables("Arrows", MAX_ARROW_COUNT_COLLECTABLES)
            self.update_collectables()


            # Collision
            self.player_and_barrels()
            self.arrows_and_barrels()



        
        self.collidables = { # in here so collidables get emptied every loop
            "Barrels": [],
            "Arrows" : [],
            "Shurikens" : [],
            "Bombs" : [],
            "Bosses" : [],
            "Water" : [],
            "Boundary": []
        }

        # self.to_render_sorted = []


    def update_player(self):
        if self.camera_follow == self.player:
            self.player.set_delta_time(self.dt)
            self.player.update(self.inputs["Rotation"], self.inputs["Action"], self.direction)
        else:
            self.player.update_away(self.inputs["Rotation"], self.inputs["Action"], self.direction) # apparently i had handle rotation for a player and objects, so i can just do this so that the player doesnt rotate around the camera when tracking something else. i am such a genius


        if self.player.in_water:
            lower_player(self.player)
            self.player.move(Vector((0, 1)) * .1 * self.dt)
            self.player.move(self.direction * -.5 * self.dt)
        else:
            raise_player(self.player)

        self.player_arrow.update(self.player.looking)
        self.player.check_knockback()


    def shoot_arrow(self):
        if self.inputs["Action"]["shoot"] and not self.paused: #and len(self.player.inventory["Arrows"]) > 0:
            if self.player.arrow_counter < self.player.stats["M"]:
                self.player.shot = not self.player.shot
                if not self.player.shot:
                    self.player.knockback_power = 1
                    self.player.knockback = True
                    shot = Arrow((self.player.center.x, self.player.center.y), 16, 1, blue, self.player.looking, self.player.angle_looking) # self.player.angle_looking based on rotation
                    self.arrows.append(shot)
                    self.player.arrow_counter += 1
            else:
                # self.player.inventory["Arrows"].pop()
                self.player.arrow_counter = 0

    def add_collectables(self, item, MAX):
        if len(self.collectables[item]) < MAX:
            self.collectables[item].append(Collectable([random.randrange(0, int(200)), random.randrange(0, int(200))], 12, 12, black, images[item]))

    def update_arrows(self):
        for arrow in self.arrows:
            if not self.paused:
                arrow.update(self.inputs["Rotation"], self.direction)
            index = bisect.bisect_left([o.center.y for o in self.to_render_sorted], arrow.center.y)
            self.to_render_sorted.insert(index, arrow)

    
    def update_barrels(self):
        for barrel in self.barrels:
            barrel.set_delta_time(self.dt)
            barrel.update(self.inputs["Rotation"], self.direction)
        
            # limits the render distance by not allowing things outside of range to be added to to_render
            if limit_render(barrel, self.player.render_radius):
                continue
            
            added = False

            for arrow in self.arrows:
                if abs(barrel.center.x - arrow.center.x) <= barrel.width / 2 and abs(barrel.center.y - arrow.center.y) <= barrel.height / 2:
                    self.collidables["Arrows"].append(arrow)
                    self.collidables["Barrels"].append(barrel)
                    added = True

            # for bomb in bombs:
            #     if bomb.landing:
            #         if abs(barrel.center.x - bomb.center.x) <= barrel.width / 2 + bomb.width / 2 and abs(barrel.center.y - bomb.center.y) <= barrel.height / 2 + bomb.height / 2:
            #             self.collidables["Bombs"].append(bomb)
            #             if not added:
            #                 self.collidables["Barrels"].append(barrel)
                
            if not added:
                limit_collision(barrel, self.player, self.player.collision_radius, self.collidables["Barrels"])

            index = bisect.bisect_left([o.center.y for o in self.to_render_sorted], barrel.center.y)
            self.to_render_sorted.insert(index, barrel)


    def update_enemies(self):
        pass


    def update_collectables(self):
        print(len(self.collectables["Arrows"]))
        for items, holder in self.collectables.items():
            for i in range (len(holder) - 1, -1, -1):
                if abs(holder[i].center.x - self.player.center.x) < 8 and abs(holder[i].center.y - self.player.center.y) < 8:
                    # if holder[i].powerup:
                    #     player.power_up = True
                    #     celebrate(particles)
                    #     del holder[i]
                    #     break
                    holder[i].follow_player = True
                    holder[i].follow_speed = random.randrange(50, 200) / 10000
                    self.player.inventory[items].append(holder[i])
                    # stick.play()
                    # arrow_shot.play()
                    del holder[i]
                    continue
                else:
                    if holder[i].timer >= holder[i].despawn_time:
                        del holder[i]
                        continue
                holder[i].update(self.inputs["Rotation"], self.direction)
                
                index = bisect.bisect_left([o.center.y for o in self.to_render_sorted], self.collectables[items][i].center.y)
                self.to_render_sorted.insert(index, self.collectables[items][i])


    
    def render_all(self, display):
        self.player_arrow.render(display)
        # every item including player
        for object in self.to_render_sorted:
            
            if isinstance(object, Player):
                object.render(display)
                # object.draw_hitbox(display)
                object.draw_healthbar(display)
            
            if isinstance(object, Barrel):
                object.render(display)
                object.draw_healthbar(display)

            if isinstance(object, Arrow):
                object.render(display)

            if isinstance(object, Collectable):
                object.render(display)


            if self.inputs["Admin"]["hitboxes"]:
                object.draw_hitbox(display)

        self.render_player_inventory(display)



    def render_player_inventory(self, display):
        # renders max of 30 things
        for i in range(max(len(self.player.inventory["Watermelons"]) - 10, 0), len(self.player.inventory["Watermelons"])):
            self.player.inventory["Watermelons"][i].render(display)
        # renders max of 30 things
        for i in range(max(len(self.player.inventory["Arrows"]) - 10, 0), len(self.player.inventory["Arrows"])):
            self.player.inventory["Arrows"][i].render(display)


    def camera_tracking(self):
        difference_vec = Vector(mid_x - self.camera_follow.center.x, mid_y - self.camera_follow.center.y)
        self.player.move(difference_vec * self.player.scroll_speed)
        self.direction -= difference_vec * self.player.scroll_speed


    def player_and_barrels(self):
        # Player and barrels colliding with barrels
        for i in range(len(self.collidables["Barrels"]) + 1 - 1, -1, -1):
            bodyA = self.player

            if i != len(self.collidables["Barrels"]):
                bodyA = self.collidables["Barrels"][i]

            for j in range(len(self.collidables["Barrels"]) - 1, -1, -1):
                bodyB = self.collidables["Barrels"][j]

                collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

                if collided:
                    bodyA.move(normal * (depth / 2) * self.dt)
                    bodyB.move(normal * -1 * (depth / 2) * self.dt)

    def arrows_and_barrels(self):
        # Arrows colliding with Barrels
        for i in range(len(self.collidables["Arrows"]) - 1, -1, -1):
            bodyA = self.collidables["Arrows"][i]
            hit = False
            for j in range(len(self.collidables["Barrels"]) - 1, -1, -1):
                bodyB = self.collidables["Barrels"][j]
                collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

                if collided:
                    bodyB.health_bar.damage(bodyA.damage)
                    bodyB.move(Vector((math.cos(bodyA.arrow_angle), math.sin(bodyA.arrow_angle))) * .1 * self.dt)
                    self.delete_arrow(bodyA)
                    # damage.play()
                    del self.collidables["Arrows"][i]
                    if bodyB.health_bar.health <= 0:
                        # screen_shake = 10
                        self.delete_barrel(bodyB)#, collectables["Watermelons"], Tifanie, player)
                        del self.collidables["Barrels"][j]
                    hit = True
                    break  # okay to break because the arrow already hit something and it wont hit anything else

    def delete_arrow(self, arrow_to_delete):
        self.arrows.remove(arrow_to_delete)

    def delete_barrel(self, barrel_to_delete):
        self.barrels.remove(barrel_to_delete)


    def set_delta_time(self, dt):
        self.dt = dt

    