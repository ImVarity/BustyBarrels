import pygame
from render import *
from pygame.locals import *
import pygame
import math
import bisect
import random
from Square import Hitbox
from vector import Vector
from z_throwables.arrow import Arrow
from barrel import Barrel
from player import Player, PlayerArrow
from collectable import Collectable
from npc import NPC
from uno import Uno
from particles import Particle, dust, explode, celebrate
from z_enemies.slime import Slime
from z_throwables.bomb import Bomb
from bullets import Shuriken, SwordShot
from map import Tilemap
from render import *
from z_enemies.butterfly import Butterfly
from bridge import BridgePart
from car import Alpha
from kingv2 import Kingv2
import time


MAX_ARROW_COUNT_COLLECTABLES = 75
MAX_BANANA_COUNT_COLLECTABLES = 20
MAX_BARRELS = 60


class GameLoop:
    def __init__(self) -> None:
        
        self.save_files = {}

        self.Map = Tilemap()

        self.dt = 1
        self.sounds = None
        self.first_pass = False # does everything that needs to happen in the first loop

        self.direction = Vector(0, 0)
        self.paused = False
        self.intro_paused_timer = 0
        self.intro_paused = False


        self.player = Player([0, 0], 8, 8, blue, health=500)
        self.player_arrow = PlayerArrow([mid_x + 12, mid_y], 16, 16, blue)
        self.spawnpoint = Barrel((0, 0), 8, 8, black)
        self.tif_spawnpoint = Barrel([-405, 325], 8, 8, black)
        self.syl_spawnpoint = Barrel([-400, -400], 8, 8, black)
        self.cry_spawnpoint = Barrel([400, 400], 8, 8, blue)
        self.bk_spawnpoint = Barrel([400, -400], 8, 8, blue)
        self.powerup = Collectable((mid_x, mid_x), 16, 16, black, [img.convert_alpha() for img in bigger_bomb_images])
        self.powerup.to_render.spread = 1.2

        # Bosses
        self.Tifanie = Uno([-405, 325], 32, 32, purple, "Tifanie", health=500)
        self.Sylvia = Butterfly([-400, -400], 32, 32, blue, "Sylvia", health=400)
        self.Crystal = Butterfly([400, 400], 32, 32, blue, "Crystal", health=400)
        self.BarrelKing = Kingv2([400, -400], 32, 32, black, "King", health=1000)

        self.bosses = [self.Tifanie, self.Sylvia, self.Crystal, self.BarrelKing]

        # Car
        self.Alpha = Alpha([-35, -20], 56, 48, red, health=100)

        # NPCS
        self.Mikhail = NPC([0, -40], 64, 64, red, rock_images)
        self.npcs = [self.Mikhail]

        # Enemies
        self.Bob = Slime([-40, -40], 12, 12, black, Vector(1, 0), Vector(self.player.center.x, self.player.center.y))
        self.random_slime_count = 0
        self.slimes = []


        # Camera
        self.camera_follow = self.player.location
        self.screen_shake = 0
        self.shake_magnitude = 8

        self.to_render = []
        self.boxes = []
        self.arrows = []
        self.bombs = []
        self.spawnpoints = [self.spawnpoint, self.tif_spawnpoint, self.syl_spawnpoint, self.cry_spawnpoint, self.bk_spawnpoint]
        self.bridge = [
            BridgePart([0, -500], 99, 48, 0, red),
            BridgePart([90, -500], 99, 48, 180, red)
        ]
        self.boundaries = [Hitbox((-24, -624), 624 * 2, 40, red), Hitbox((590, -24), 40, 624 * 2, red), Hitbox((-24, 590), 624 * 2, 40, red), Hitbox((-624, -24), 40, 624 * 2, red)]


        self.barrels = [

        ]

        self.collectables = {
            "Arrows" : [],
            "Watermelons" : [],
            "Bananas" : [],
            "Powerups" : []
        }

        self.inputs = {
            "Movements" : {
                "up" : False,
                "down" : False,
                "left" : False,
                "right" : False,
                "lock" : False
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
                "interact" : False,
                "heal" : False
            },
            "Admin" : {
                "hitboxes" : False
            },
            "HUD" : {
                "stats" : False
            },
            "Tests" : {
                "click" : False
            }
        }

        self.npc_input = {
            "up" : False,
            "down" : False,
            "confirm" : False
        }

        self.collidables = {
            "Barrels": [],
            "Arrows" : [],
            "Shurikens" : [],
            "Leaves" : [],
            "Swordshots" : [],
            "Bombs" : [],
            "Bosses" : {
                "Butterflies" : [],
                "Bunny" : [],
                "King" : []
            },
            "Water" : [],
            "Boundary": []
        }

        # just put player in here immediately, it will be sorted in place anyway
        self.to_render_sorted = [self.player]


        # VFX
        self.particles = []


        self.stages = {
            "grasslands", "blank", "blink"
        }
        self.stage = "grasslands"

        self.size = 0
        self.end = display_width
        self.reached = False
        self.sized_reached = False
        self.entering_blank = False


        self.death_length = 300 # how many frames the player is dead for
        self.death_timer = 0 # when the player dies, this is the period after death before being able to play again
        self.dead = False


        self.max_barrel_count = MAX_BARRELS




        # Introductions ---------------

        # Heal intro --------
        self.heal_intro = False
        self.heal_intro_timer = 300 # 5 second introduction

        # Shoot intro -----
        self.shoot_intro = False
        self.shoot_intro_timer = 300


        # Rotate intro ----
        self.rotate_intro = False
        self.rotate_intro_timer = 300

        # Dash intro ----
        self.dash_intro = False
        self.dash_intro_timer = 300


        # Lock intro -----
        self.lock_intro = False
        self.lock_intro_timer = 300


        self.barrels_busted_final_score = 0

    def enter_blank(self, display):
        if self.reached:
            self.size += 25 * self.dt
        self.end -= 40 * self.dt

        if self.end <= -1000:
            self.reached = True

        pygame.draw.line(display, (255, 255, 255), (display_width, display_height / 2), [self.end, display_height / 2], 2)
        pygame.draw.line(display, (255, 255, 255), (display_width, display_height / 2), [self.end, display_height / 2], 2)

        if self.reached:
            pygame.draw.rect(display, white, pygame.Rect(0, display_height / 2 - self.size, display_width, self.size))
            pygame.draw.rect(display, white, pygame.Rect(0, display_height / 2, display_width, self.size))
        

        if self.size >= display_height / 2 + 400:
            self.entering_blank = False
            self.size = 0
            self.end = display_width
            self.reached = False
            self.stage = "blank"


    def death_screen(self, display):
        if self.death_timer > 0:
            death_color = (0, 0, 0, int((self.death_timer / self.death_length) * 255))
            death_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha()
            death_surface.fill(death_color)
            render_text_centered((mid_x, mid_y), f"{self.death_timer // 60 + 1}", death_surface, "white", scale=2)
            render_text_centered((mid_x, mid_y - mid_y // 2), "BUSTED", death_surface, "white", scale=2)

            display.blit(death_surface, (0, 0))
            self.dead = True
            self.death_timer -= 1
        else:
            self.dead = False




    # Gets the direction that the player is moving
    def initialize_direction(self):
        if self.dead:
            self.inputs["Movements"]["up"] = False
            self.inputs["Movements"]["down"] = False
            self.inputs["Movements"]["left"] = False
            self.inputs["Movements"]["right"] = False



        self.direction = self.player.get_direction(self.inputs["Movements"]) * self.dt
        self.player.direction = self.direction


    def final_score(self, display):
        render_text_centered((mid_x, mid_y - 150), f'GAME COMPLETE', display, "white")
        render_text_centered((mid_x, mid_y - 130), f'BUSTED {self.barrels_busted_final_score} BARRELS', display, "white")
        
    
    def FIRSTPASS(self):
        if not self.first_pass:
            self.first_pass = True
            self.player.sounds = self.sounds
            self.Mikhail.sounds = self.sounds
            self.Mikhail.text.sounds = self.sounds

    
    def main(self, dt, display): # -> dict[str]:
        self.FIRSTPASS()
        self.set_delta_time(dt)
        self.initialize_direction()

        if not self.paused:
            self.update_player()
            self.camera_tracking()


        self.update_arrows()
        self.update_barrels()
        self.update_enemies()
        self.update_car()


        # Update spawnpoints
        self.update_spawnpoints()

        # Update boundaries
        self.update_boundaries()

        # self.update_bridge()


        # checks if player shoots the arrow
        self.shoot_arrow(dt)

        # player dash effects
        self.dash_effects()
        

        # checks if player throws  abomb
        self.throw_bomb()


        # Spawn barrels
        self.add_barrels(self.max_barrel_count)

        # Spawning collectables
        self.add_collectables("Arrows", MAX_ARROW_COUNT_COLLECTABLES)
        self.add_collectables("Bananas", MAX_BANANA_COUNT_COLLECTABLES)
        self.update_collectables()

        # Bombs
        self.update_bombs()


        # NPC
        self.update_npc()


        # Boss
        self.update_bosses(dt, display)
        self.find_closest_boss() # checks which healthbar to show up top
        

       
        # Collision
        self.player_and_boundary()
        self.player_and_water()
        self.player_and_barrels()
        self.player_and_shurikens(display)
        self.player_and_leaves(display)
        self.player_and_butterflies(display)
        self.player_and_swordshots(display)
        self.arrows_and_all()
        self.bombs_and_all()

        # temp ------------------------------------


        while len(self.slimes) < self.random_slime_count:
            self.slimes.append(Slime([random.randint(-40, 40), random.randint(-40, 40)], 12, 12, black, Vector(1, 0), Vector(self.player.center.x, self.player.center.y)))

        self.update_slimes()

        # temp ------------------------------------


        # Deletion
        self.delete_objects()

        if self.inputs["Tests"]["click"]:
            self.entering_blank = True


        self.collidables = { # in here so collidables get emptied every loop
            "Barrels": [],
            "Arrows" : [],
            "Shurikens" : [],
            "Leaves" : [],
            "Swordshots" : [],
            "Bombs" : [],
            "Bosses" : {
                "Butterflies" : [],
                "Bunny" : [],
                "King" : []
            },
            "Water" : [],
            "Boundary": []
        }


    def find_closest_boss(self):
        closest = 99999
        boss = None
        for b in self.bosses:
            if b.summoned and not b.dead:
                b.closest_to_player = False
                if math.hypot(b.center.x - self.player.center.x, b.center.y - self.player.center.y) < closest:
                    closest = math.hypot(b.center.x - self.player.center.x, b.center.y - self.player.center.y)
                    boss = b

        try:
            # print(boss.name)
            boss.closest_to_player = True
        except:
            return

    def update_car(self):
        if not self.paused:
            self.Alpha.set_delta_time(self.dt)
            self.Alpha.update(self.inputs["Rotation"], self.direction)
            if limit_render(self.Alpha, self.player.render_radius):
                return
        self.to_render.append(self.Alpha)


    def calc_butterfly_centroid(self):
        if not self.Sylvia.dead and not self.Crystal.dead:
            x1, y1 = self.Sylvia.location
            x2, y2 = self.Crystal.location
            x3, y3 = self.player.location

            centroid_x = (x1 + x2 + x3) / 3
            centroid_y = (y1 + y2 + y3) / 3

            return [centroid_x, centroid_y]
        
    


    def update_bridge(self):
        for part in self.bridge:
            part.set_delta_time(self.dt)
            part.update(self.inputs["Rotation"], self.direction)

            if part.center.x >= -32 and part.center.x <= display_width + 32 and part.center.y >= -32 and part.center.y <= display_height + 32:
                self.to_render.append(part)

    def update_boundaries(self):
        for boundary in self.boundaries:
            if not self.paused:
                boundary.set_delta_time(self.dt)
                boundary.update(self.inputs["Rotation"], self.direction)
            self.collidables["Boundary"].append(boundary)
            self.to_render.append(boundary)


    def update_spawnpoints(self):
        for spawnpoint in self.spawnpoints:
            if not self.paused:
                spawnpoint.set_delta_time(self.dt)
                spawnpoint.update(self.inputs["Rotation"], self.direction)

    def dash_effects(self):
        if not self.paused:
            if self.inputs["Action"]["dash"] and self.player.dash_start <= self.dt:
                self.sounds.dash_sound.play()
                dust(self.particles, self.player.location, self.direction)

    def completion_text(self, display):
        # text that appears when something happens
        self.player.quest_complete_text(display)
        self.player.powerup_collected(display, self.powerup)

    def update_player(self):
        self.player.set_delta_time(self.dt)
        self.player.heal(self.inputs["Action"]["heal"])
        
        # just update away the whole time because the player is moving away from the middle of the screen constantly
        self.player.update_away(self.inputs["Rotation"], self.inputs["Action"], self.direction) # apparently i had handle rotation for a player and objects, so i can just do this so that the player doesnt rotate around the camera when tracking something else. i am such a genius

        
        

        if self.player.in_water:
            lower_player(self.player)
            self.player.move(Vector(0, 1) * .1 * self.dt)
            self.player.move(self.direction * -.5 * self.dt)
        else:
            raise_player(self.player)
        self.player_arrow.update(self.player.looking)
        self.player.check_knockback()


    def update_tiles(self):
        for tile in self.Map.tiles:
            tile.set_delta_time(self.dt)
            if not self.paused:
                tile.update(self.inputs["Rotation"], self.direction)

        
    def render_tiles(self, display):
        # render tiles first
        for tile in self.Map.tiles:
            if tile.center.x >= -32 and tile.center.x <= display_width + 32 and tile.center.y >= -32 and tile.center.y <= display_height + 32:
                if self.inputs["Admin"]["hitboxes"]:
                    tile.draw_hitbox(display)

                if tile.type == "water":
                    limit_collision(tile, self.player, self.player.collision_radius, self.collidables["Water"])
                    tile.to_render.animate(display, self.dt)
                    continue
                tile.render(display)



    def shoot_arrow(self, dt):
        self.player.dexterity_check(dt)
        if self.inputs["Action"]["shoot"] and not self.paused and len(self.player.inventory["Arrows"]) > 0:
            if self.player.arrow_counter < self.player.stats["M"]:
                if self.player.can_shoot():
                    self.player.knockback_power = 1
                    self.player.knockback = True
                    shot = Arrow((self.player.center.x, self.player.center.y), 16, 1, blue, self.player.looking, self.player.angle_looking) # self.player.angle_looking based on rotation
                    self.arrows.append(shot)
                    self.player.arrow_counter += 1
            else:
                self.player.inventory["Arrows"].pop()
                self.player.arrow_counter = 0
        

    def throw_bomb(self):
        if self.inputs["Action"]["throw"] and self.player.bomber:
            bomb = Bomb((self.player.center.x, self.player.center.y), 16, 16, black, self.player.looking)
            if self.inputs["Action"]["dash"]:
                bomb = Bomb((self.player.center.x, self.player.center.y), 16, 16, black, self.player.looking, velocity=3.25)
            bomb.bomb_angle_start = self.player.angle_looking
            self.sounds.throw.play()
            self.bombs.append(bomb)

    def update_boss_bullets(self, boss, display):
        # dont need to fix z position of shurikens because always on top)
        for i, shuriken in enumerate(boss.bullets):
            shuriken.set_delta_time(self.dt)
            shuriken.update(self.inputs["Rotation"], self.direction)
            if isinstance(shuriken, SwordShot):
                shuriken.update_particles(display)
            # limit render distance
            if limit_render(shuriken, self.player.render_radius):
                continue
            
            if boss == self.Tifanie:
                bullet = "Shurikens"
            elif boss == self.Sylvia or boss == self.Crystal:
                bullet = "Leaves"
            elif boss == self.BarrelKing:
                bullet = "Swordshots"
            else:
                bullet = "Shurikens"
            limit_collision(shuriken, self.player, self.player.collision_radius, self.collidables[bullet])

    def add_collectables(self, item, MAX):
        if not self.BarrelKing.summoned:
            if len(self.collectables[item]) < MAX:
                self.collectables[item].append(Collectable([random.randrange(int(self.spawnpoint.center.x - 525), int(self.spawnpoint.center.x + 525)), random.randrange(int(self.spawnpoint.center.y - 575), int(self.spawnpoint.center.y + 575))], 12, 12, black, images[item]))
        else: # If the king is alive then remove all collectables on the screen 
            self.collectables[item] = []

    def add_barrels(self, MAX):
        if len(self.barrels) < MAX:
            self.barrels.append(Barrel([random.randrange(int(self.spawnpoint.center.x - 525), int(self.spawnpoint.center.x + 525)), random.randrange(int(self.spawnpoint.center.y - 575), int(self.spawnpoint.center.y + 575))], 16, 16, pink, health=25))
        elif len(self.barrels) > MAX:
            self.barrels = self.barrels[:MAX]

        
    def load_barrels(self, loc, health):
        b = Barrel(loc, 16, 16, pink, health=25)
        b.health_bar.set_health(health)
        self.barrels.append(b)


    def update_arrows(self):
        for arrow in self.arrows:
            if not self.paused:
                arrow.set_delta_time(self.dt)
                arrow.update(self.inputs["Rotation"], self.direction)
            self.to_render.append(arrow)

    # temporary ------------------------------------------------

    def update_slimes(self):
        for slime in self.slimes:
            if not self.paused:
                slime.set_delta_time(self.dt)
                slime.update(self.inputs["Rotation"], self.direction, self.player.center)

                if limit_render(slime, self.player.render_radius):
                    continue

            self.to_render.append(slime)
    # temporary ------------------------------------------------

    
    def update_barrels(self):
        for barrel in self.barrels:
            if not self.paused:
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

                for bomb in self.bombs:
                    if bomb.landing:
                        if abs(barrel.center.x - bomb.center.x) <= barrel.width / 2 + bomb.width / 2 and abs(barrel.center.y - bomb.center.y) <= barrel.height / 2 + bomb.height / 2:
                            self.collidables["Bombs"].append(bomb)
                            if not added:
                                self.collidables["Barrels"].append(barrel)
                    
                if not added:
                    limit_collision(barrel, self.player, self.player.collision_radius, self.collidables["Barrels"])

            self.to_render.append(barrel)

    def update_bosses(self, dt, display):
        for b in self.bosses:
            if not self.paused:
                b.set_delta_time(self.dt)

                if isinstance(b, Kingv2):
                    self.update_barrelking(b)
                elif isinstance(b, Uno):
                    self.update_uno(b)
                elif isinstance(b, Butterfly):
                    self.update_butterfly(b)

                b.attacks(dt)

                # obvious
                if not b.summoned:
                    # checks if just summoned
                    if b.check_if_summon() and isinstance(b, Kingv2):
                        self.entering_blank = True

                # updates the bullets that the boss shoots
                self.update_boss_bullets(b, display)

                b.follow_player(self.player.center)
                if b.summoned and not b.dead:
                    added = False

                    for arrow in self.arrows: # if arrows get close to the boss we add the boss to collidables
                        if abs(b.center.x - arrow.center.x) <= b.width / 2 and abs(b.center.y - arrow.center.y) <= b.height / 2:
                            self.collidables["Arrows"].append(arrow)
                            if isinstance(b, Butterfly):
                                self.collidables["Bosses"]["Butterflies"].append(b)
                            elif isinstance(b, Uno):
                                self.collidables["Bosses"]["Bunny"].append(b)
                            elif isinstance(b, Kingv2):
                                self.collidables["Bosses"]["King"].append(b)
                            added = True


                    if not added: # checks if the boss is close enough to the player to check collision if it wasnt added in the check above
                        if abs(b.center.x - self.player.center.x) <= b.width / 2 and abs(b.center.y - self.player.center.y) <= b.height / 2:
                            if isinstance(b, Butterfly):
                                self.collidables["Bosses"]["Butterflies"].append(b)
                            elif isinstance(b, Uno):
                                self.collidables["Bosses"]["Bunny"].append(b)
                            elif isinstance(b, Kingv2):
                                self.collidables["Bosses"]["King"].append(b)

                    for bomb in self.bombs:
                        if bomb.landing:
                            if abs(self.BarrelKing.center.x - bomb.center.x) <= self.BarrelKing.width / 2 + bomb.width / 2 and abs(self.BarrelKing.center.y - bomb.center.y) <= self.BarrelKing.height / 2 + bomb.height / 2:
                                self.collidables["Bombs"].append(bomb)
                                if not added:
                                    self.collidables["Bosses"]["King"].append(self.BarrelKing)



                                

            self.to_render.append(b)

    def next_boss_warning(self, display):
        for boss in self.bosses:
            if boss.dead:
                self.bosses.pop(0)
            if not boss.dead:
                if (boss.activate - boss.barrels_busted) <= 0:
                    return
                back_surface = pygame.Surface((250, 12), pygame.SRCALPHA).convert_alpha()
                back_surface.fill((47,79,79, 100))
                display.blit(back_surface, (75, 382))
                render_text_centered((mid_x, 385), f'Break {boss.activate - boss.barrels_busted} barrels for ???', display, "white")
                return


    def update_uno(self, b):
        b.update(self.inputs["Rotation"], self.inputs["Movements"], self.direction)

    def update_butterfly(self, b):
        b.update(self.inputs["Rotation"], self.inputs["Movements"], self.direction)

    def update_barrelking(self, b):
        if not self.paused:
            b.set_delta_time(self.dt)
            b.update(self.inputs["Rotation"], self.inputs["Movements"], self.direction, self.player.center)
            if b.check_if_land(): # when the boss lands it does different stuff
                self.max_barrel_count += 5
                self.stage = "blink" if self.stage == "blank" else "blank"
                self.BarrelKing.sword_color = "white" if self.BarrelKing.sword_color == "black" else "black"
                self.BarrelKing.name_color = "white" if self.BarrelKing.name_color == "black" else "black"
                self.BarrelKing.color = white if self.BarrelKing.color == black else black
                self.screen_shake = 12
                self.shake_magnitude = 12

        
    def handle_npc_inputs(self):
        if self.inputs["HUD"]["next"]:
            if self.Mikhail.interacting:
                self.Mikhail.next()
        self.inputs["HUD"]["next"] = False

        self.npc_input = {
            "up" : False,
            "down" : False,
            "confirm" : False
        }

    def update_npc(self):

        for npc in self.npcs:
            if not self.paused:
                npc.set_delta_time(self.dt)
                npc.update(self.inputs["Rotation"], self.direction)
                if limit_render(npc, self.player.render_radius):
                    continue
                if self.player.center.x >= npc.center.x - npc.width / 2 and self.player.center.x <= npc.center.x + npc.width / 2 and self.player.center.y >= npc.center.y - npc.width / 2 and self.player.center.y <= npc.center.y + npc.width / 2:
                    if self.inputs["Action"]["interact"]:
                        self.sounds.menu_click.play()
                        npc.interacting = True
                else:
                    npc.interacting = False

            self.to_render.append(npc)



    def update_enemies(self):
        pass

    def update_bombs(self):
        for bomb in self.bombs:
            if not self.paused:
                bomb.set_delta_time(self.dt)
                if not self.paused:
                    bomb.update(self.inputs["Rotation"], self.direction)

            self.to_render.append(bomb)


    def update_collectables(self):
        for items, holder in self.collectables.items():
            
            for i in range (len(holder) - 1, -1, -1):
                if not self.paused:
                    holder[i].set_delta_time(self.dt)
                    if abs(holder[i].center.x - self.player.center.x) < 8 and abs(holder[i].center.y - self.player.center.y) < 8:
                        if holder[i].powerup:
                            self.player.power_up = True
                            celebrate(self.particles)
                            del holder[i]
                            break
                        holder[i].follow_player = True
                        holder[i].follow_speed = random.randrange(50, 200) / 10000
                        self.player.inventory[items].append(holder[i])
                        # self.sounds.stick.play()
                        self.sounds.arrow_shot.play()
                        del holder[i]
                        continue
                    else:
                        if holder[i].timer >= holder[i].despawn_time:
                            del holder[i]
                            continue
                    
                    holder[i].update(self.inputs["Rotation"], self.direction)
                self.to_render.append(self.collectables[items][i])
    

    
    def render_all(self, display):

        # sorting all the things to render by y value
        self.to_render = sorted(self.to_render, key=lambda x : x.center.y)
        # arrow comes below everything else
        self.player_arrow.render(display)

        # whatever the player is holding on to
        self.render_player_inventory(display)

        # every item including player
        for object in self.to_render:   
            if isinstance(object, Player):
                object.render(display)
                # object.draw_hitbox(display)
                object.draw_healthbar(display)
            
            elif isinstance(object, Barrel):
                object.render(display)
                object.draw_healthbar(display)

            elif isinstance(object, Arrow):
                object.render(display)

            elif isinstance(object, Collectable):
                object.render(display)
            
            elif isinstance(object, Alpha):
                if self.BarrelKing.dead:
                    object.render(display)

            elif isinstance(object, NPC):
                object.render(display)

            elif isinstance(object, Uno):
                if object.summoning:
                    object.render(display)
                if object.summoned and not object.dead:
                    object.render(display)
                    object.draw_healthbar(display)
                if object.dead:
                    object.draw_hitbox(display)
            
            elif isinstance(object, Kingv2):
                if object.summoning:
                    object.render(display)
                if object.summoned and not object.dead:
                    object.draw_hitbox(display)
                    object.render(display)
                    object.draw_healthbar(display)
                if object.dead:
                    object.draw_hitbox(display)

            
            elif isinstance(object, Butterfly):
                if object.summoning:
                    object.render(display)
                if object.summoned and not object.dead:
                    object.to_render.animate(display, self.dt, type="stack")
                    object.draw_healthbar(display)
                if object.dead:
                    object.draw_hitbox(display)

            elif isinstance(object, Slime):
                object.render(display)

            elif isinstance(object, Bomb):
                object.render(display)
                object.draw_hitbox(display)


            if self.inputs["Admin"]["hitboxes"]:
                for s in self.spawnpoints:
                    s.draw_hitbox(display)
                for b in self.boundaries:
                    b.draw_hitbox(display)
                object.draw_hitbox(display)

        # things that need to drawn on top of everything



        # all the bosses bullets
        self.render_boss_bullets(display)

        # the damage number above the player
        self.draw_particles(display)

        self.player.draw_damage(display)
        self.player.draw_heal(display)

        # how to summon next boss
        self.next_boss_warning(display)

        # intros
        self.introductions(display)

        # when talking to mikhail
        self.render_npc_hud(display)
        self.completion_text(display)
        self.draw_HUD(display)


        if self.entering_blank:
            self.enter_blank(display)

        if self.BarrelKing.dead:
            self.final_score(display)
        
        # only really activates when dead
        self.death_screen(display)

        # if self.paused:
        #     self.paused_screen(display)


    def introductions(self, display):
        # print(self.inputs["Action"]["lock"])
        
        # Intro shoot -----------------------------------------------------
        if self.shoot_intro and self.shoot_intro_timer > 0:
            self.intro_paused_timer = self.introduce_shoot(display, self.inputs["Action"]["shoot"]) # checks if they pressed the key to prove they learned from the introduction

        if not self.shoot_intro_timer:
            self.intro_paused = False

        # Condition to start introduction
        if not self.shoot_intro and len(self.player.inventory["Arrows"]) > 0:
            self.intro_paused = True
            self.shoot_intro = True
            self.intro_paused_timer = self.shoot_intro_timer

        # Intro heal ------------------------------------------------------
        if self.heal_intro and self.heal_intro_timer > 0:
            self.intro_paused_timer = self.introduce_heal(display, self.inputs["Action"]["heal"])

        if not self.heal_intro_timer:
            self.intro_paused = False

        # Condition to start introduction
        if not self.heal_intro and len(self.player.inventory["Bananas"]) > 0 and self.player.health_bar.health < self.player.health_bar.maxhealth:
            self.heal_intro = True
            self.player.intro_active = True
            self.intro_paused_timer = self.heal_intro_timer


        # Intro rotate ------------------------------------------------------
        if self.rotate_intro and self.rotate_intro_timer > 0:
            self.intro_paused_timer = self.introduce_rotate(display, self.inputs["Rotation"]["clockwise"] or self.inputs["Rotation"]["counterclockwise"])
        
        if not self.rotate_intro_timer:
            self.intro_paused = False
        
        # Condition to start introduction
        if not self.rotate_intro and self.Tifanie.summoned:
            self.intro_paused = True
            self.rotate_intro = True
            self.intro_paused_timer = self.rotate_intro_timer


        # Intro dash --------------------------------------------------------
        if self.dash_intro and self.dash_intro_timer > 0:
            self.intro_paused_timer = self.introduce_dash(display, self.inputs["Action"]["dash"])
        
        if not self.dash_intro_timer:
            self.intro_paused = False
        
        # Condition to start introduction
        if not self.dash_intro and self.Tifanie.charging:
            self.intro_paused = True
            self.dash_intro = True
            self.intro_paused_timer = self.dash_intro_timer

        
        # Intro lock ------------------------------------------------------------
        if self.lock_intro and self.lock_intro_timer > 0:
            self.intro_paused_timer = self.introduce_lock(display, self.inputs["Movements"]["lock"])
        
        if not self.lock_intro_timer:
            self.intro_paused = False
        
        # Condition to start introduction
        if not self.lock_intro and self.Sylvia.summoned:
            self.intro_paused = True
            self.lock_intro = True
            self.intro_paused_timer = self.lock_intro_timer



    def introduce_lock(self, display, learned):
        if self.lock_intro_timer > 0:
            self.lock_intro_timer -= 1 * self.dt
            textone = "HOLD L"
            texttwo = "TO LOCK SHOOTING DIRECTION"

            back_surface = pygame.Surface((len(textone) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            back_surface.fill((47,79,79, 100))
            display.blit(back_surface, (mid_x - ((len(textone) * 8 + 10) // 2), mid_y - 60 - 2))

            b_s_2 = pygame.Surface((len(texttwo) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            b_s_2.fill((47,79,79, 100))
            display.blit(b_s_2, (mid_x - ((len(texttwo) * 8 + 10) // 2), mid_y - 50 - 2))


            render_text_centered((mid_x, mid_y - 60), textone, display, "white")
            render_text_centered((mid_x, mid_y - 50), texttwo, display, "white")

        if learned:
            self.lock_intro_timer = 0
            return 1

        return 0

        

    def introduce_heal(self, display, learned):
        if self.heal_intro_timer > 0:
            self.heal_intro_timer -= 1 * self.dt
            back_surface = pygame.Surface((7 * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            back_surface.fill((47,79,79, 100))
            display.blit(back_surface, (mid_x - ((7 * 8 + 10) // 2), mid_y - 60 - 2))


            b_s_2 = pygame.Surface((int(len("TO EAT A BANANA")) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            b_s_2.fill((47,79,79, 100))
            display.blit(b_s_2, (mid_x - ((int(len("TO EAT A BANANA")) * 8 + 10) // 2), mid_y - 50 - 2))

            b_s_3 = pygame.Surface((int(len(f'HEALS {self.player.banana_heal_amount} HEALTH')) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            b_s_3.fill((47,79,79, 100))
            display.blit(b_s_3, (mid_x - ((int(len(f'HEALS {self.player.banana_heal_amount} HEALTH')) * 8 + 10) // 2), mid_y - 40 - 2))


            render_text_centered((mid_x, mid_y - 60), "PRESS H", display, "white")
            render_text_centered((mid_x, mid_y - 50), "TO EAT A BANANA", display, "white")
            render_text_centered((mid_x, mid_y - 40), f'HEALS {self.player.banana_heal_amount} HEALTH', display, "white")


        if learned:
            self.heal_intro_timer = 0
            return 1
        return 0

    def introduce_shoot(self, display, learned):
        if self.shoot_intro_timer > 0:
            self.shoot_intro_timer -= 1 * self.dt
            back_surface = pygame.Surface((7 * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            back_surface.fill((47,79,79, 100))
            display.blit(back_surface, (mid_x - ((7 * 8 + 10) // 2), mid_y - 60 - 2))

            b_s_2 = pygame.Surface((int(len("TO SHOOT AN ARROW")) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            b_s_2.fill((47,79,79, 100))
            display.blit(b_s_2, (mid_x - ((int(len("TO SHOOT AN ARROW")) * 8 + 10) // 2), mid_y - 50 - 2))

            b_s_3 = pygame.Surface((int(len("DEALS 10 DAMAGE")) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            b_s_3.fill((47,79,79, 100))
            display.blit(b_s_3, (mid_x - ((int(len("DEALS 10 DAMAGE")) * 8 + 10) // 2), mid_y - 40 - 2))


            render_text_centered((mid_x, mid_y - 60), "PRESS J", display, "white")
            render_text_centered((mid_x, mid_y - 50), "TO SHOOT AN ARROW", display, "white")
            render_text_centered((mid_x, mid_y - 40), f'DEALS 10 DAMAGE', display, "white")

        if learned:
            self.shoot_intro_timer = 0
            return 1

        return 0
    

    def introduce_rotate(self, display, learned):
        if self.rotate_intro_timer > 0:
            self.rotate_intro_timer -= 1 * self.dt
            textone = "PRESS Q AND E"
            texttwo = "TO ROTATE"

            back_surface = pygame.Surface((len(textone) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            back_surface.fill((47,79,79, 100))
            display.blit(back_surface, (mid_x - ((len(textone) * 8 + 10) // 2), mid_y - 60 - 2))

            b_s_2 = pygame.Surface((len(texttwo) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            b_s_2.fill((47,79,79, 100))
            display.blit(b_s_2, (mid_x - ((len(texttwo) * 8 + 10) // 2), mid_y - 50 - 2))


            render_text_centered((mid_x, mid_y - 60), textone, display, "white")
            render_text_centered((mid_x, mid_y - 50), texttwo, display, "white")

        if learned:
            self.rotate_intro_timer = 0
            return 1

        return 0

    def introduce_dash(self, display, learned):
        if self.dash_intro_timer > 0:
            self.dash_intro_timer -= 1
            textone = "PRESS K"
            texttwo = "TO DASH"

            back_surface = pygame.Surface((len(textone) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            back_surface.fill((47,79,79, 100))
            display.blit(back_surface, (mid_x - ((len(textone) * 8 + 10) // 2), mid_y - 60 - 2))

            b_s_2 = pygame.Surface((len(texttwo) * 8 + 10, 10), pygame.SRCALPHA).convert_alpha()
            b_s_2.fill((47,79,79, 100))
            display.blit(b_s_2, (mid_x - ((len(texttwo) * 8 + 10) // 2), mid_y - 50 - 2))


            render_text_centered((mid_x, mid_y - 60), textone, display, "white")
            render_text_centered((mid_x, mid_y - 50), texttwo, display, "white")

        if learned:
            self.dash_intro_timer = 0
            return 1

        return 0


        

        

    def render_npc_hud(self, display):
        for npc in self.npcs:
            if npc.interacting:
                npc_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha()
                npc_surface.fill(npc_color)
                display.blit(npc_surface, (0, 0))
                
                if not npc.talk(display, self.npc_input, self.player, display):
                    npc.interacting = False
                    self.inputs["Action"]["interact"] = False
            else:
                npc.check_funds(display)
                if self.player.inQuest:
                    npc.update_quests(self.player)
                    npc.show_quest_status(display)
                if self.player.center.x >= self.Mikhail.center.x - self.Mikhail.width / 2 and self.player.center.x <= self.Mikhail.center.x + self.Mikhail.width / 2 and self.player.center.y >= self.Mikhail.center.y - self.Mikhail.width / 2 and self.player.center.y <= self.Mikhail.center.y + self.Mikhail.width / 2 and not self.paused:
                    M_surface = pygame.Surface((len("T to talk to Mikhail") * 7 + 4, 10), pygame.SRCALPHA).convert_alpha()
                    M_surface.fill(npc_color)
                    display.blit(M_surface, (self.player.center.x - len("T to talk to Mikhail") * 7 / 2 - 2, self.player.center.y - 40 - 2))
                    render_text_centered((self.player.center.x, self.player.center.y - 40), "T to talk to Mikhail", display, "white")
                npc.reset_talk()
        self.handle_npc_inputs()


    def render_player_inventory(self, display):
        # render max of 1 thing
        max_hold = 5
        # can put into one loop 


        for i in range(max(len(self.player.inventory["Watermelons"]) - max_hold, 0), len(self.player.inventory["Watermelons"])):
            self.player.inventory["Watermelons"][i].render(display)

        for i in range(max(len(self.player.inventory["Arrows"]) - max_hold, 0), len(self.player.inventory["Arrows"])):
            self.player.inventory["Arrows"][i].render(display)

        for i in range(max(len(self.player.inventory["Bananas"]) - max_hold, 0), len(self.player.inventory["Bananas"])):
            self.player.inventory["Bananas"][i].render(display)



    def render_boss_bullets(self, display):
        for boss in self.bosses:
            for bullet in boss.bullets:
                if self.inputs["Admin"]["hitboxes"]:
                    bullet.draw_hitbox(display)
                bullet.render(display)



    def camera_tracking(self):
        if self.Tifanie.tracking:
            self.camera_follow = self.Tifanie.location
        elif self.Sylvia.tracking:
            self.camera_follow = self.Sylvia.location
        elif self.Crystal.tracking:
            self.camera_follow = self.Crystal.location
        elif self.BarrelKing.tracking:
            self.camera_follow = self.BarrelKing.location
        else:
            self.camera_follow = self.player.location

         # follows middle of player and 2 butterflies
        if not self.Sylvia.dead and self.Sylvia.summoned and not self.Crystal.dead and self.Crystal.summoned:
            self.camera_follow = self.calc_butterfly_centroid()

        difference_vec = Vector(mid_x - self.camera_follow[0], mid_y - self.camera_follow[1])
        self.player.move(difference_vec * self.player.scroll_speed * self.dt)
        self.direction -= difference_vec * self.player.scroll_speed * self.dt


    def player_and_water(self):
        in_water = False
        for i in range(len(self.collidables["Water"]) - 1, -1, -1):
            bodyB = self.collidables["Water"][i]
            collided, depth, normal = self.player.handle_collision(bodyB.normals(), self.player.normals(), bodyB)
            if collided:
                in_water = True
                break
        self.player.in_water = in_water

    def player_and_boundary(self):
        # Player colliding with Shurikens
        for i in range(len(self.collidables["Boundary"]) - 1, -1, -1):
            bodyB = self.collidables["Boundary"][i]
            collided, depth, normal = self.player.handle_collision(bodyB.normals(), self.player.normals(), bodyB)
            if collided:
                self.player.move(normal * depth * self.dt)



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

    def player_and_shurikens(self, display):
        # Player colliding with Shurikens
        for i in range(len(self.collidables["Shurikens"]) - 1, -1, -1):
            bodyB = self.collidables["Shurikens"][i]
            collided, depth, normal = self.player.handle_collision(bodyB.normals(), self.player.normals(), bodyB)

            if collided:
                self.player.damage(bodyB.damage, display)
                self.Tifanie.delete_shuriken(bodyB)
                del self.collidables["Shurikens"][i]
                if self.player.health_bar.health <= 0:
                    x_distance = math.sqrt((self.player.center.x - self.spawnpoint.center.x) ** 2 + (self.player.center.y - self.spawnpoint.center.y) ** 2)
                    v = Vector((self.player.center.x - self.spawnpoint.center.x), (self.player.center.y - self.spawnpoint.center.y))
                    v.normalize()
                    self.player.move_distance(v * -1, x_distance)
                    t_x_distance = math.sqrt((self.Tifanie.center.x- self.tif_spawnpoint.center.x) ** 2 + (self.Tifanie.center.y - self.tif_spawnpoint.center.y) ** 2)
                    t_v = Vector((self.Tifanie.center.x - self.tif_spawnpoint.center.x), (self.Tifanie.center.y - self.tif_spawnpoint.center.y))
                    t_v.normalize()
                    self.Tifanie.move_distance(t_v * -1, t_x_distance)
                    self.Tifanie.temp_death()
                    self.player.player_death()
                    self.death_timer = self.death_length
                    self.stage = "grasslands"
                    break
                self.player.move(normal * .05)

    def player_and_swordshots(self, display):
        # Player colliding with Swords
        for i in range(len(self.collidables["Swordshots"]) - 1, -1, -1):
            bodyB = self.collidables["Swordshots"][i]
            collided, depth, normal = self.player.handle_collision(bodyB.normals(), self.player.normals(), bodyB)

            if collided:
                self.player.damage(bodyB.damage, display)
                self.BarrelKing.delete_bullets(bodyB)
                del self.collidables["Swordshots"][i]
                if self.player.health_bar.health <= 0:
                    x_distance = math.sqrt((self.player.center.x - self.spawnpoint.center.x) ** 2 + (self.player.center.y - self.spawnpoint.center.y) ** 2)
                    v = Vector((self.player.center.x - self.spawnpoint.center.x), (self.player.center.y - self.spawnpoint.center.y))
                    v.normalize()
                    self.player.move_distance(v * -1, x_distance)
                    t_x_distance = math.sqrt((self.BarrelKing.center.x- self.bk_spawnpoint.center.x) ** 2 + (self.BarrelKing.center.y - self.bk_spawnpoint.center.y) ** 2)
                    t_v = Vector((self.BarrelKing.center.x - self.bk_spawnpoint.center.x), (self.BarrelKing.center.y - self.bk_spawnpoint.center.y))
                    t_v.normalize()
                    self.BarrelKing.move_distance(t_v * -1, t_x_distance)
                    self.BarrelKing.temp_death()
                    self.max_barrel_count = MAX_BARRELS
                    self.player.player_death()
                    self.death_timer = self.death_length
                    self.stage = "grasslands"
                    break
                # self.player.move(normal * .05)

    def player_and_leaves(self, display):
        # Player colliding with Leaves
        for i in range(len(self.collidables["Leaves"]) - 1, -1, -1):
            bodyB = self.collidables["Leaves"][i]
            collided, depth, normal = self.player.handle_collision(bodyB.normals(), self.player.normals(), bodyB)

            if collided:
                self.player.damage(bodyB.damage, display)
                self.Sylvia.delete_shuriken(bodyB)
                self.Crystal.delete_shuriken(bodyB)
                del self.collidables["Leaves"][i]
                if self.player.health_bar.health <= 0:
                    x_distance = math.sqrt((self.player.center.x - self.spawnpoint.center.x) ** 2 + (self.player.center.y - self.spawnpoint.center.y) ** 2)
                    v = Vector((self.player.center.x - self.spawnpoint.center.x), (self.player.center.y - self.spawnpoint.center.y))
                    v.normalize()
                    self.player.move_distance(v * -1, x_distance)

                    t_x_distance = math.sqrt((self.Sylvia.center.x- self.syl_spawnpoint.center.x) ** 2 + (self.Sylvia.center.y - self.syl_spawnpoint.center.y) ** 2)
                    t_v = Vector((self.Sylvia.center.x - self.syl_spawnpoint.center.x), (self.Sylvia.center.y - self.syl_spawnpoint.center.y))
                    t_v.normalize()
                    self.Sylvia.move_distance(t_v * -1, t_x_distance)
                    self.Sylvia.temp_death()

                    s_x_distance = math.sqrt((self.Crystal.center.x- self.cry_spawnpoint.center.x) ** 2 + (self.Crystal.center.y - self.cry_spawnpoint.center.y) ** 2)
                    s_v = Vector((self.Crystal.center.x - self.cry_spawnpoint.center.x), (self.Crystal.center.y - self.cry_spawnpoint.center.y))
                    s_v.normalize()
                    self.Crystal.move_distance(s_v * -1, s_x_distance)
                    self.Crystal.temp_death()

                    self.player.player_death()
                    self.death_timer = self.death_length
                    self.stage = "grasslands"
                    break
                self.player.move(normal * .05)
        
    def player_and_butterflies(self, display):
        for i in range(len(self.collidables["Bosses"]["Butterflies"])):
            bodyB = self.collidables["Bosses"]["Butterflies"][i]
            collided, depth, normal = self.player.handle_collision(bodyB.normals(), self.player.normals(), bodyB)

            if collided:
                if bodyB.attack_damage > 0:
                    self.player.damage(bodyB.attack_damage, display)
                if self.player.health_bar.health <= 0:
                    x_distance = math.sqrt((self.player.center.x - self.spawnpoint.center.x) ** 2 + (self.player.center.y - self.spawnpoint.center.y) ** 2)
                    v = Vector((self.player.center.x - self.spawnpoint.center.x), (self.player.center.y - self.spawnpoint.center.y))
                    v.normalize()
                    self.player.move_distance(v * -1, x_distance)

                    t_x_distance = math.sqrt((self.Sylvia.center.x- self.syl_spawnpoint.center.x) ** 2 + (self.Sylvia.center.y - self.syl_spawnpoint.center.y) ** 2)
                    t_v = Vector((self.Sylvia.center.x - self.syl_spawnpoint.center.x), (self.Sylvia.center.y - self.syl_spawnpoint.center.y))
                    t_v.normalize()
                    self.Sylvia.move_distance(t_v * -1, t_x_distance)
                    self.Sylvia.temp_death()

                    s_x_distance = math.sqrt((self.Crystal.center.x- self.cry_spawnpoint.center.x) ** 2 + (self.Crystal.center.y - self.cry_spawnpoint.center.y) ** 2)
                    s_v = Vector((self.Crystal.center.x - self.cry_spawnpoint.center.x), (self.Crystal.center.y - self.cry_spawnpoint.center.y))
                    s_v.normalize()
                    self.Crystal.move_distance(s_v * -1, s_x_distance)
                    self.Crystal.temp_death()

                    self.player.player_death()
                    self.death_timer = self.death_length
                    self.stage = "grasslands"
                    break
                self.player.move(normal * .05)
    
        

    def arrows_and_all(self):
        # Arrows colliding with Barrels
        for i in range(len(self.collidables["Arrows"]) - 1, -1, -1):
            bodyA = self.collidables["Arrows"][i]
            hit = False
            for j in range(len(self.collidables["Barrels"]) - 1, -1, -1):
                bodyB = self.collidables["Barrels"][j]
                collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

                if collided:
                    bodyB.health_bar.damage(bodyA.damage)
                    bodyB.move(Vector(math.cos(bodyA.arrow_angle), math.sin(bodyA.arrow_angle)) * .1 * self.dt)
                    self.delete_arrow(bodyA)
                    self.sounds.damage.play()
                    del self.collidables["Arrows"][i]
                    if bodyB.health_bar.health <= 0:
                        self.screen_shake = 10
                        self.shake_magnitude = 8
                        self.delete_barrel(bodyB)
                        del self.collidables["Barrels"][j]
                    hit = True
                    break  # okay to break because the arrow already hit something and it wont hit anything else

        
        # Arrows colliding with bosses
        for i in range(len(self.collidables["Arrows"]) - 1, -1, -1):
            bodyA = self.collidables["Arrows"][i]
            hit = False
            for j in range(len(self.collidables["Bosses"]["Butterflies"]) - 1, -1, -1):
                bodyB = self.collidables["Bosses"]["Butterflies"][j]
                collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

                if collided:
                    bodyB.health_bar.damage(bodyA.damage)
                    bodyB.move(Vector(math.cos(bodyA.arrow_angle), math.sin(bodyA.arrow_angle)) * .1 * self.dt)
                    self.delete_arrow(bodyA)
                    self.sounds.damage.play()
                    del self.collidables["Arrows"][i]
                    if bodyB.health_bar.health <= 0:
                        self.screen_shake = 10
                        self.shake_magnitude = 12
                        # Powerup after killing the boss -------
                        if self.Sylvia.dead or self.Crystal.dead:
                            p = Collectable((bodyB.center.x, bodyB.center.y), 8, 8, black, bomb_images)
                            p.powerup = True
                            self.player.bomber = True
                            self.collectables["Powerups"].append(p)
                        # --------------------------------------

                        bodyB.death()

                    break  # okay to break because the arrow already hit something and it wont hit anything else

            # Boss colliding with Arrows (only have one boss for now will have to split into another for loop probably)
            if hit == False and len(self.collidables["Bosses"]["Bunny"]) > 0: # check if it already hit something
                bodyB = self.Tifanie
                collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
                if collided:
                    bodyB.health_bar.damage(bodyA.damage)
                    self.delete_arrow(bodyA)
                    self.sounds.damage.play()
                    del self.collidables["Arrows"][i]
                    if bodyB.health_bar.health <= 0:
                        if not self.Tifanie.dead:
                            self.screen_shake = 30
                            self.shake_magnitude = 12
                        self.Tifanie.death()
                    break


            # King colliding with arrows
            if hit == False and len(self.collidables["Bosses"]["King"]) > 0 and not self.BarrelKing.check_in_air(): # can attack the boss only if he is on the ground
                bodyB = self.BarrelKing
                collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
                if collided:
                    bodyB.health_bar.damage(bodyA.damage)
                    self.delete_arrow(bodyA)
                    self.sounds.damage.play()
                    del self.collidables["Arrows"][i]
                    if bodyB.health_bar.health <= 0:
                        if not self.BarrelKing.dead:
                            self.screen_shake = 30
                            self.shake_magnitude = 12

                        self.Alpha.center = self.BarrelKing.center # spawns car where king dies
                        self.BarrelKing.death()
                        self.barrels_busted_final_score = self.player.barrels_busted
                        self.max_barrel_count = MAX_BARRELS
                        self.stage = "grasslands"
                    break
    
    def bombs_and_all(self):
        self.bombs_and_barrels()
        self.bombs_and_barrelking()


    def bombs_and_barrelking(self):
        # Bombs colliding with Barrel King
        for i in range(len(self.collidables["Bombs"]) - 1, -1, -1):
            bodyA = self.collidables["Bombs"][i]

            bodyB = self.BarrelKing
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

            if collided:
                bodyB.health_bar.damage(bodyA.damage)
                del self.collidables["Bombs"][i]
                if bodyB.health_bar.health <= 0:
                    if not self.BarrelKing.dead:
                        self.screen_shake = 30
                        self.shake_magnitude = 12

                    self.Alpha.center = self.BarrelKing.center # spawns car where king dies
                    self.BarrelKing.death()
                    self.barrels_busted_final_score = self.player.barrels_busted
                    self.max_barrel_count = MAX_BARRELS
                    self.stage = "grasslands"
                break  # okay to break because the arrow already hit something and it wont hit anything else
    

    def bombs_and_barrels(self):
        # Bombs colliding with Barrels
        for i in range(len(self.collidables["Bombs"]) - 1, -1, -1):
            bodyA = self.collidables["Bombs"][i]
            
            for j in range(len(self.collidables["Barrels"]) - 1, -1, -1):
                bodyB = self.collidables["Barrels"][j]
                collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

                if collided:
                    bodyB.health_bar.damage(bodyA.damage)
                    bodyB.move(Vector(math.cos(bodyA.bomb_angle), math.sin(bodyA.bomb_angle)) * .1)
                    del self.collidables["Bombs"][i]
                    if bodyB.health_bar.health <= 0:
                        self.screen_shake = 10
                        self.shake_magnitude = 8
                        self.delete_barrel(bodyB)
                        del self.collidables["Barrels"][j]
                    break  # okay to break because the arrow already hit something and it wont hit anything else


    def delete_arrow(self, arrow_to_delete):
        try:
            self.arrows.remove(arrow_to_delete)
        except:
            pass

    def delete_barrel(self, barrel_to_delete): # (barrels, barrel_to_delete, watermelons, Tifanie, player):
        try:
            for boss in self.bosses:
                if not boss.dead: # this is so that other bosses dont get activated
                    if isinstance(boss, Butterfly):
                        self.Sylvia.barrels_busted += 1
                        self.Crystal.barrels_busted += 1
                        break
                    boss.barrels_busted += 1
                    break

            self.player.barrels_busted += 1
            if self.player.inQuest:
                self.player.quest_barrels_busted += 1
            yes = random.randint(0, 1)
            if yes:
                self.collectables["Watermelons"].append(Collectable([barrel_to_delete.center.x, barrel_to_delete.center.y], 12, 12, green, watermelon_images))
            self.barrels.remove(barrel_to_delete)
        except:
            pass

    def delete_objects(self):
        # deletes arrows that are off the screen
        for i in range(len(self.arrows) -1, -1, -1):
            if math.hypot(self.arrows[i].center.x - self.player.center.x, self.arrows[i].center.y - self.player.center.y) > self.player.stats["R"]:
                del self.arrows[i]
            # if arrows[i].center.x < 0 or arrows[i].center.x > display_width or arrows[i].center.y < 0 or arrows[i].center.y > display_height:
            #     del arrows[i]


        # deletes all the shots that bosses shoot past their deletion radius
        for boss in self.bosses:
            for i in range(len(boss.bullets) - 1, -1, -1):
                if math.hypot(boss.center.x - boss.bullets[i].center.x, boss.center.y - boss.bullets[i].center.y) > boss.delete_radius:
                    del boss.bullets[i]

        # checks if the bomb height is lower enough then explodes it
        for i in range(len(self.bombs) -1, -1, -1):
            if self.bombs[i].bomb_height < -6:
                self.explode([self.bombs[i].center.x, self.bombs[i].center.y])
                del self.bombs[i]

    def draw_HUD(self, display):
        margin = 0
        start_x = 320
        start_y = 20
        inc = 20

        if not self.Mikhail.interacting:
            arrow_count = str(len(self.player.inventory["Arrows"]))
            icon_arrow = pygame.transform.rotate(arrow_images[len(arrow_images) // 2 - 1], 90)
            display.blit(icon_arrow.convert_alpha(), (12, 12))
            arrow_ry = 12 + icon_arrow.get_width()

            banana_count = str(len(self.player.inventory["Bananas"]))
            display.blit(banana_img.convert_alpha(), (12, 12 + inc))
            banana_ry = 12 + banana_img.get_width()

            display.blit(watermelon_img.convert_alpha(), (12, 12 + inc * 2))
            watermelon_ry = 12 + watermelon_img.get_width()

            display.blit(barrel_img.convert_alpha(), (12 - 1, 12 + inc * 3))
            barrel_ry = 12 + barrel_img.get_width() - 1

            biggest = max([banana_ry, arrow_ry, watermelon_ry, barrel_ry])


            render_text((biggest + 5, 12 + (15 - 6) // 2), arrow_count, display)
            render_text((len(str(arrow_count)) * 8 + (biggest + 5) , 12 + (15 - 6) // 2), "x" + str(self.player.stats["M"]), display)
            render_text((biggest + 5, 12 + inc + (15 - 6) // 2), str(banana_count), display)
            render_text((biggest + 5, 12 + (inc * 2) + (15 - 6) // 2), str(len(self.player.inventory["Watermelons"])), display)
            render_text((biggest + 5, 12 + (inc * 3) + (15 - 6) // 2), str(self.player.barrels_busted), display)
        else:
            back_surface = pygame.Surface((300, 30), pygame.SRCALPHA).convert_alpha()
            back_surface.fill((47,79,79, 100))
            display.blit(back_surface, (50, 340))
            arrow_count = str(len(self.player.inventory["Arrows"]))
            icon_arrow = pygame.transform.rotate(arrow_images[len(arrow_images) // 2 - 1], 90)
            display.blit(icon_arrow.convert_alpha(), (100, 350 - (icon_arrow.get_height() / 2) + 3))
            render_text((115, 350), arrow_count + " x" + str(self.player.stats["M"]), display)

            display.blit(watermelon_img.convert_alpha(), (180, 350 - 3))
            render_text((200, 350),str(len(self.player.inventory["Watermelons"])), display)

            display.blit(barrel_img.convert_alpha(), (245, 345))
            render_text((270, 350), str(self.player.barrels_busted), display)

    def paused_screen(self, display):

        npc_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha()
        npc_surface.fill(npc_color)
        display.blit(npc_surface, (0, 0))
        display.blit(paused_img.convert_alpha(), (mid_x - paused_img.get_width() // 2, mid_y - paused_img.get_height() // 2 - 150))

        start = -30
        render_text((mid_x - len("controls") * 7 / 2, mid_y + start - 100), "controls", display)
        render_text((mid_x - len("WASD to move") * 7 / 2, mid_y + start - 70), "WASD to move", display, "white")
        render_text((mid_x - len("Q and E to rotate") * 7 / 2, mid_y + start - 50), "Q and E to rotate", display, "white")
        render_text((mid_x - len("T to interact") * 7 / 2, mid_y + start - 30), "T to interact", display, "white")
        render_text((mid_x - len("J to shoot") * 7 / 2, mid_y + start - 10), "J to shoot", display, "white")
        render_text((mid_x - len("K to dash") * 7 / 2, mid_y + start + 10), "K to dash", display, "white")
        render_text((mid_x - len("L to lock look direction") * 7 / 2, mid_y + start + 30), "L to lock look direction", display, "white")
        render_text((mid_x - len("I to autoshoot") * 7 / 2, mid_y + start + 50), "I to autoshoot", display, "white")
        render_text((mid_x - len("Arrow keys to navigate") * 7 / 2, mid_y + start + 70), "Arrow keys to navigate", display, "white")
        render_text((mid_x - len("Enter to confirm") * 7 / 2, mid_y + start + 90), "Enter to confirm", display, "white")
        render_text((mid_x - len("Tab for stats") * 7 / 2, mid_y + start + 110), "Tab for stats", display, "white")
        render_text((mid_x - len("Escape to pause") * 7 / 2, mid_y + start + 130), "Escape to pause", display, "white")


    def draw_particles(self, display):
        for i in range(len(self.particles) - 1, -1, -1):
            particle = self.particles[i]
            particle.all(display)
            if particle.dead():
                self.particles.remove(particle)

    def explode(self, loc):
        self.sounds.explosion_sound.play()
        explode(self.particles, loc)

    def set_delta_time(self, dt):
        self.dt = dt

    

    def load_data(self, data):
        self.player.center.x, self.player.center.y = data["player_location"][0], data["player_location"][1]
        self.player.set_vertices()
        for i in range(len(data["barrels"]["locations"])):
            self.load_barrels(data["barrels"]["locations"][i], data["barrels"]["health"][i])

        data["barrels"]["locations"] = []
        data["barrels"]["health"] = []

    def save_data(self, data):
        data["player_location"] = [self.player.center.x - self.spawnpoint.center.x, self.player.center.y - self.spawnpoint.center.y]
        for barrel in self.barrels:
            data["barrels"]["locations"].append((barrel.location[0] - self.spawnpoint.location[0], barrel.location[1] - self.spawnpoint.location[1]))
            data["barrels"]["health"].append(barrel.health_bar.health)

        return data
