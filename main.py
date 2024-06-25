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
from chat import TextBubble
from health import HealthBar
from watermelon import Watermelon
from collectable import Collectable
from npc import NPC
from uno import Uno
from uno import Shuriken
from particles import Particle
from bomb import Bomb
from tile import Tile
from Dos import Dos
from render import *
import time
from pygame.locals import *
flags = DOUBLEBUF


screen_width = 800
screen_height = 800


pygame.init()
pygame.mixer.init()

dash_sound = pygame.mixer.Sound('sfx/grabitem.wav')
collect_sound_2 = pygame.mixer.Sound('sfx/collectitem2.wav')
explosion_sound = pygame.mixer.Sound('sfx/explosion.wav')
menu_click = pygame.mixer.Sound('sfx/menuclick.wav')
arrow_shot = pygame.mixer.Sound('sfx/arrow_shot.wav')
arrow_shot2 = pygame.mixer.Sound('sfx/arrow_sound2.wav')
swing = pygame.mixer.Sound('sfx/swing_sound.wav')

explosion_sound.set_volume(.2)
pygame.mixer.music.load('sfx/bgm.mp3')

pygame.mixer.music.play(loops=-1)


pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN,pygame.KEYUP])

screen = pygame.display.set_mode((screen_width, screen_height), flags, 32)
pygame.display.set_caption('Busty Barrels')

display_width, display_height = 400, 400
mid_x, mid_y = display_width / 2, display_height /2
display = pygame.Surface((display_width, display_height))

pause_color = (169, 169, 169, 100)
pause_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha()
pause_surface.fill(pause_color)

overlay_color = (250, 240, 230, 45)
overlay_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
overlay_surface.fill(overlay_color)

npc_color = (47,79,79, 100)
npc_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha()
npc_surface.fill(npc_color)




mousePos = pygame.mouse.get_pos()

keys_held = set()

clock = pygame.time.Clock()


input = {
    "right": False,
    "left" : False,
    "down" : False,
    "up": False,
    "lock" : False,
    "interact": False,
    "stats" : False
}

rotation_input = {
    "reset": False,
    "clockwise" : False,
    "counterclockwise" : False
}

action_input = {
    "ultimate" : False,
    "shoot" : False,
    "autofire": False,
    "dash": False,
    "throw" : False

}

admin_input = {
    "hitboxes": False
}


# ------------------------------------------------------------ Player ------------------------------------------------------------------------

player = Player([0, 0], 8, 8, blue, health=500)
player_arrow = PlayerArrow([mid_x + 12, mid_y], 16, 16, blue)
spawnpoint = Barrel((0, 0), 8, 8, black)
tif_spawnpoint = Barrel((200, 200), 8, 8, black)




# ------------------------------------------------------------ Radius ------------------------------------------------------------------

render_radius = 200
collision_radius = 33


# -------------------------------------------------- Where items and objects are held --------------------------------------------------------------------------------

to_render = []
boxes = []
arrows = []
bombs = []
watermelons = []
collectables = {
    "Arrows" : [],
    "Watermelons" : [],
    "Powerups" : []
}

bigger_bomb_images = []
for i in range(len(bomb_images)):
    n = pygame.transform.scale(bomb_images[i], (bomb_images[i].get_width() + 20, bomb_images[i].get_height() + 20))
    n.convert_alpha()
    bigger_bomb_images.append(n)
powerup = Collectable((mid_x, mid_x), 16, 16, black, bigger_bomb_images)


random_barrel_count = 150
random_arrow_count = 100

check = Barrel([150, 150], 16, 16, pink, health=500)

barrels = [
    check,
    Barrel([250, 150], 16, 16, pink, health=500),
    Barrel([150, 250], 16, 16, pink, health=500),
    Barrel([250, 250], 16, 16, pink, health=500)
]


for i in range(random_arrow_count):
    collectables["Arrows"].append(Collectable([random.randrange(-display_width, display_width), random.randrange(-display_height, display_height)], 12, 12, black, arrow_images))


for i in range(random_barrel_count):
        barrels.append(Barrel([random.randrange(int(spawnpoint.center.x - 400), int(spawnpoint.center.x + 400)), random.randrange(int(spawnpoint.center.y - 400), int(spawnpoint.center.y + 400))], 16, 16, pink, health=25))



# ------------------------------------------------- Bosses and NPCS ----------------------------------------------------------------------



font = pygame.font.Font('fonts/tiny.ttf', 8)


Tifanie = Uno([mid_x, mid_y], 32, 32, purple)

bosses = [Tifanie]

Mikhail = NPC([0, -20], 64, 64, red, rock_images)

npcs = [Mikhail]


# -------------------------------------------------- Map stuff that needs to be moved somewhere else ------------------------------------------------

map_br = [
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0],
]
map_bl = [
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 0, 0, 0],
]
map_tr = [
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0],
]
map_tl = [
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0],
]


tiles = []



for i in range(len(map_tl)):
    for j in range(len(map_tl[0])):
        if map_tl[i][j] == 1:
            tiles.append(Tile((-(j * 48 - 24), -(i * 48 - 24)), 48, 48, white, grass_img))

for i in range(len(map_tr)):
    for j in range(len(map_tr[0])):
        if map_tr[i][j] == 1:
            tiles.append(Tile(((j * 48 - 24), -(i * 48 - 24)), 48, 48, white, grass_img))

for i in range(len(map_bl)):
    for j in range(len(map_bl[0])):
        if map_bl[i][j] == 1:
            tiles.append(Tile((-(j * 48 - 24), i * 48 - 24), 48, 48, white, grass_img))

for i in range(len(map_br)):
    for j in range(len(map_br[0])):
        if map_br[i][j] == 1:
            tiles.append(Tile((j * 48 - 24, i * 48 - 24), 48, 48, white, grass_img))



# ------------------------------------------------------ Useful functions ------------------------------------------------------------

def explode(particles, loc):
    explosion_sound.play()
    for i in range(30):
        particles.append(Particle([loc[0], loc[1]], [random.randint(-628, 628) / 100 / 2, random.randint(-628, 0) / 100], random.randint(10, 20), "explosion"))

def dust(particles, loc, direction):

    # v_x = random.randint(-200, 400) / 500 * direction.x * -2 * 2
    # v_y = random.randint(0, 400) / 500 * direction.y * -1 * 2

    for i in range(2):
        v_x = random.randint(-100, 400) / 500 * direction.x * -2 * 2
        v_y = random.randint(0, 400) / 500 * direction.y * -1 * 2
        p = Particle([loc[0], loc[1] + 4], [v_x, v_y], random.randint(3, 5), "dust")
        p.gravity = -.02
        p.shrink_rate = .08
        particles.append(p)


def delete_arrow(arrows, arrow_to_delete):
    if arrow_to_delete in arrows:
        arrows.remove(arrow_to_delete)


def delete_barrel(barrels, barrel_to_delete, watermelons, Tifanie, player):
    if barrel_to_delete in barrels:
        Tifanie.barrels_busted += 1
        player.barrels_busted += 1
        if player.inQuest:
            player.quest_barrels_busted += 1
        watermelons.append(Collectable([barrel_to_delete.center.x, barrel_to_delete.center.y], 12, 12, green, watermelon_images))
        barrels.remove(barrel_to_delete)
    

# ------------------------------------------------ Testing stuff that will be fixed in the future ------------------------------------------------

attack = False

attack_end = 30
attack_start = 0
attack_inc = 1

start_of_game_pause = 0

arrow_count = "0"


tracking = player

pre_time = time.perf_counter()
running = True
paused = False


quest_encryption = {
    "1" : "Deliver",
    "2" : "Break",
    "M" : "Arrow Multiplier",
    "R" : "Range",
    "A" : "Arrows",
    "B" : "Barrels",
    "W" : "Watermelons"
}

# 1 - deliver (Deliver 100 arrows/watermelons)
# 2 - action (Break 100 barrels)

# A - arrows
# W - watermelons
# B - barrels

# M - arrow multiplier
# R - range


# Ex
# 1A100M10 (deliver 100 arrows for 100 arrow multiplier)
# 2B100R9 (Break 5 barrels for 9 more range)


particles = []

quest = ""


screen_shake = 0

timer = 0

# --------------------------------------------------------------- Main loop ------------------------------------------------------------------

while running:
    now_time = time.perf_counter()
    dt = now_time - pre_time
    dt *= 60
    pre_time = time.perf_counter()
    start_of_game_pause += 1
    timer += 1

    screen.fill(white)
    display.fill(grass_green)
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    fps = clock.get_fps()
    FPS_text = "FPS:" + str(int(fps))


# ------------------------------------------------------- Handling input ------------------------------------------------------------------
    action_input["shoot"] = False
    action_input["throw"] = False

    npc_input = { # in main loop so that it only registers once per click
        "up" : False,
        "down" : False,
        "confirm" : False
    }

    # if start_of_game_pause == 60:
        # paused = not paused


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            if event.key == pygame.K_t:
                input["interact"] = not input["interact"]
            if event.key == pygame.K_k:
                action_input["dash"] = True
            if event.key == pygame.K_UP:
                npc_input["up"] = True
            if event.key == pygame.K_DOWN:
                npc_input["down"] = True
            if event.key == pygame.K_RETURN:
                npc_input["confirm"] = True
            if event.key == pygame.K_SPACE:
                action_input["throw"] = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                action_input["shoot"] = True
            if event.key == pygame.K_i:
                action_input["autofire"] = not action_input["autofire"]
            if event.key == pygame.K_BACKQUOTE:
                admin_input["hitboxes"] = not admin_input["hitboxes"]
            if event.key == pygame.K_c:
                if input["interact"]:
                    menu_click.play()
                    npc.next()
                    




    rotation_input["counterclockwise"] = keys[pygame.K_e]
    rotation_input["clockwise"] = keys[pygame.K_q]
    rotation_input["reset"] = keys[pygame.K_z]

    input["up"] = keys[pygame.K_w]
    input["down"] = keys[pygame.K_s]
    input["left"] = keys[pygame.K_a]
    input["right"] = keys[pygame.K_d]
    input["lock"] = keys[pygame.K_l]
    input["stats"] = keys[pygame.K_TAB]
    
    if action_input["autofire"]:
        action_input["shoot"] = True
    else:
        action_input["shoot"] = keys[pygame.K_j]


# ---------------------------------------------------------- Adding collectables to places -------------------------------------------------------

    if len(collectables["Arrows"]) < random_arrow_count:
        collectables["Arrows"].append(Collectable([random.randrange(int(spawnpoint.center.x - 400), int(spawnpoint.center.x + 400)), random.randrange(int(spawnpoint.center.y - 400), int(spawnpoint.center.y + 400))], 12, 12, black, arrow_images))

    if len(barrels) < random_barrel_count:
        barrels.append(Barrel([random.randrange(int(spawnpoint.center.x - 400), int(spawnpoint.center.x + 400)), random.randrange(int(spawnpoint.center.y - 400), int(spawnpoint.center.y + 400))], 16, 16, pink, health=25))

# ------------------------------------------------- Handling the rotation and direction and some updating -------------------------------------------------------
# -------------------------------------------- Other updating happens in the z-positiong updating so less for loops ----------------------------------------


    direction = player.get_direction(input)
    direction *= dt
    player.direction = direction

    # if direction.x > 0 or direction.y > 0: # makes sound if moving
        # footstep.play()

    if not paused:
        if tracking == player:
            player.update(rotation_input, action_input, direction)
        else:
            player.update_away(rotation_input, action_input, direction) # apparently i had handle rotation for a player and objects, so i can just do this so that the player doesnt rotate around the camera when tracking something else. i am such a genius


        
    # camera tracking
    if not paused:
        difference_vec = Vector((mid_x - tracking.center.x, mid_y - tracking.center.y))
        player.move(difference_vec * player.scroll_speed)
        direction -= difference_vec * player.scroll_speed


    if action_input["shoot"] and not paused and len(player.inventory["Arrows"]) > 0:
        if player.arrow_counter < player.stats["M"]:
            arrow_shot2.play()
            player.knockback_power = 1
            player.knockback = True
            shot = Arrow((player.center.x, player.center.y), 16, 1, blue, player.looking)
            shot.arrow_angle_start = player.angle_looking # based on rotation
            arrows.append(shot)
            player.arrow_counter += 1


            
        else:
            player.inventory["Arrows"].pop()
            player.arrow_counter = 0

    if action_input["throw"] and player.bomber:
        bomb = Bomb((player.center.x, player.center.y), 16, 16, black, player.looking)
        if action_input["dash"]:
            bomb = Bomb((player.center.x, player.center.y), 16, 16, black, player.looking, velocity=3.25)
        bomb.bomb_angle_start = player.angle_looking
        bombs.append(bomb)
    
    
    if action_input["dash"] and player.dash_start <= 1:
        dash_sound.play()
        dust(particles, [player.center.x, player.center.y], direction)



    player.update_actions(input)
    player.check_knockback()

    # NEED TO FIX
    attack_start += attack_inc
    if attack_start == attack_end:
        attack_start = 0
        if Tifanie.summoned and not Tifanie.dead:
            # Tifanie.attack_one(player.angle_looking)
            if not paused:
                Tifanie.spiral_attack()


    if Tifanie.summoned and not Tifanie.dead and Tifanie.health_bar.health < 500:
        if not paused:
            Tifanie.attack_two()

    
    


    # print(player.center)
    if not paused:
        player_arrow.update(player.looking, player.center)



    for tile in tiles:
        if not paused:
            tile.update(rotation_input, direction)
    # in here so collidables get emptied every loop
    collidables = {
        "Barrels": [],
        "Arrows" : [],
        "Shurikens" : [],
        "Bombs" : [],
        "Bosses" : []
    }

    # just put player in here immediately, it will be sorted in place anyway
    to_render_sorted = [player]

    if not paused:
        spawnpoint.update(rotation_input, direction)
        tif_spawnpoint.update(rotation_input, direction)

    powerup.update_powerup()

# ---------------------------------------- Sorting stuff that need to be ordered for correct z-position --------------------------------------------


    player_center_x, player_center_y = player.center.x, player.center.y



    for npc in npcs:
        if not paused:
            npc.update(rotation_input, direction)
            limit_render(npc, render_radius)
            if player_center_x >= npc.center.x - npc.width / 2 and player_center_x <= npc.center.x + npc.width / 2 and player.center.y >= npc.center.y - npc.width / 2 and player.center.y <= npc.center.y + npc.width / 2:
                if input["interact"]:
                    npc.interacting = True
                else:
                    npc.interacting = False
            else:
                npc.interacting = False
                input["interact"] = False

            # if not input["interact"]:
        index = bisect.bisect_left([o.center.y for o in to_render_sorted], npc.center.y)
        to_render_sorted.insert(index, npc)
    

    for items, holder in collectables.items():
        for i in range (len(holder) - 1, -1, -1):

            if not paused:
                
                if abs(holder[i].center.x - player_center_x) < 8 and abs(holder[i].center.y - player_center_y) < 8:
                    if holder[i].powerup:
                        player.power_up = True
                        del holder[i]
                        break
                    holder[i].follow_player = True
                    holder[i].follow_speed = random.randrange(50, 200) / 10000
                    player.inventory[items].append(holder[i])
                    del holder[i]
                    continue
                else:
                    if holder[i].timer >= holder[i].despawn_time:
                        del holder[i]
                        continue
                holder[i].update(rotation_input, direction)
            
            index = bisect.bisect_left([o.center.y for o in to_render_sorted], collectables[items][i].center.y)
            to_render_sorted.insert(index, collectables[items][i])



    # UNO sorting
    for b in bosses:
        if not paused:
            b.update(rotation_input, input, direction)
            b.follow_player(player.center)
            if b.summoned:
                for arrow in arrows:
                    if abs(b.center.x - arrow.center.x) <= b.width / 2 and abs(b.center.y - arrow.center.y) <= b.height / 2:
                        collidables["Arrows"].append(arrow)
                        collidables["Bosses"].append(b)

        index = bisect.bisect_left([o.center.y for o in to_render_sorted], b.center.y)
        to_render_sorted.insert(index, b)




    # fixes z position
    for barrel in barrels:
        if not paused:
            barrel.update(rotation_input, direction) # such a pain.. have to update before checking

            # limits the render distance by not allowing things outside of range to be added to to_render
            if limit_render(barrel, render_radius):
                continue
            
            added = False

            for arrow in arrows:
                if abs(barrel.center.x - arrow.center.x) <= barrel.width / 2 and abs(barrel.center.y - arrow.center.y) <= barrel.height / 2:
                    collidables["Arrows"].append(arrow)
                    collidables["Barrels"].append(barrel)
                    added = True

            for bomb in bombs:
                if bomb.landing:
                    if abs(barrel.center.x - bomb.center.x) <= barrel.width / 2 + bomb.width / 2 and abs(barrel.center.y - bomb.center.y) <= barrel.height / 2 + bomb.height / 2:
                        collidables["Bombs"].append(bomb)
                        if not added:
                            collidables["Barrels"].append(barrel)
                
                    
            # breaking game :skull:
            # if not added: # dont wanna add twie
            #     for cbarrel in collidables["Barrels"]:
            #         if cbarrel.center.x <= barrel.center.x + cbarrel.width / 2 and cbarrel.center.x >= barrel.center.x - cbarrel.width / 2 and cbarrel.center.y <= barrel.center.y + cbarrel.height / 2 and cbarrel.center.y >= barrel.center.y - cbarrel.height / 2:
            #             collidables["Barrels"].append(barrel)
            #             continue
            if not added:
                limit_collision(barrel, player, collision_radius, collidables["Barrels"])

        index = bisect.bisect_left([o.center.y for o in to_render_sorted], barrel.center.y)
        to_render_sorted.insert(index, barrel)


    # fixes z position of arrows
    for arrow in arrows:
        if not paused:
            arrow.update(rotation_input, direction)
        # collidables.append(arrow)
        index = bisect.bisect_left([o.center.y for o in to_render_sorted], arrow.center.y)
        to_render_sorted.insert(index, arrow)

    for bomb in bombs:
        if not paused:
            bomb.update(rotation_input, direction)

        index = bisect.bisect_left([o.center.y for o in to_render_sorted], bomb.center.y)
        to_render_sorted.insert(index, bomb)

    # dont need to fix z position of shurikens because always on top
    for i, shuriken in enumerate(Tifanie.shurikens):
        if not paused:
            shuriken.update(rotation_input, direction)
            
            # limit render distance
            if limit_render(shuriken, render_radius):
                continue

            limit_collision(shuriken, player, collision_radius, collidables["Shurikens"])




# ------------------------------------------------------ Rendering objects -------------------------------------------------------

    # render tiles first
    for tile in tiles:
        if abs(tile.center.x + 32) < display_width + 64 and abs(tile.center.y + 32) < display_height + 64:
            tile.render(display)

    # arrow should be below everythign except tiles
    player_arrow.render(display)

    # renders max of 30 things
    for i in range(max(len(player.inventory["Watermelons"]) - 10, 0), len(player.inventory["Watermelons"])):
        player.inventory["Watermelons"][i].render(display)

    # renders max of 30 things
    for i in range(max(len(player.inventory["Arrows"]) - 10, 0), len(player.inventory["Arrows"])):
        player.inventory["Arrows"][i].render(display)



# ------------------------------------------------------- Boss stuff (to fix) -------------------------------------------------------


    Tifanie.check_if_summon()
    if Tifanie.tracking:
        tracking = Tifanie
    else:
        tracking = player


# ------------------------------------------------------- End of boss stuff ------------------------------------------------------------------

# ----------------------------------------------------------- Rendering ----------------------------------------------------------------------------


    # every item including player
    for object in to_render_sorted:
        
        if isinstance(object, Player):
            object.render(display)
            # object.draw_hitbox(display)
            object.draw_healthbar(display)

        elif isinstance(object, NPC):
            object.render(display)


        elif isinstance(object, Barrel):
            object.render(display)
            object.draw_healthbar(display)
        elif isinstance(object, Arrow):
            object.render(display)

        # elif isinstance(object, Watermelon):
        #     object.render(display)

        elif isinstance(object, Collectable):
            object.render(display) 
            # object.draw_hitbox(display)

        elif isinstance(object, Uno):
            if object.summoning:
                object.render(display)
            if object.summoned and not object.dead:
                object.render(display)
                object.draw_healthbar(display)
            if object.dead:
                object.draw_hitbox(display)

        elif isinstance(object, Bomb):
            object.render(display)
            object.draw_hitbox(display)

        

        
        if admin_input["hitboxes"]:
            object.draw_hitbox(display)

    # because rendering after, always on top of everything




    for shuriken in Tifanie.shurikens:
        shuriken.render(display)

        if admin_input["hitboxes"]:
            shuriken.draw_hitbox(display)
        # shuriken.draw_hitbox(display)



    for i in range(len(particles) - 1, -1, -1):
        particle = particles[i]
        particle.all(display)
        if particle.dead():
            particles.remove(particle)

# ------------------------------------------------------- Deleting stuff -----------------------------------------------------------


    # deletes arrows that are off the screen
    for i in range(len(arrows) -1, -1, -1):
        if math.hypot(arrows[i].center.x - player_center_x, arrows[i].center.y - player_center_y) > player.stats["R"]:
            del arrows[i]
        # if arrows[i].center.x < 0 or arrows[i].center.x > display_width or arrows[i].center.y < 0 or arrows[i].center.y > display_height:
        #     del arrows[i]

    # deletes all the Tifanie shots that pass a certain radius
    for i in range(len(Tifanie.shurikens) - 1, -1, -1):
        if math.hypot(Tifanie.center.x - Tifanie.shurikens[i].center.x, Tifanie.center.y - Tifanie.shurikens[i].center.y) > Tifanie.delete_radius:
            del Tifanie.shurikens[i]


    for i in range(len(bombs) -1, -1, -1):
        if bombs[i].bomb_height < -6:
            explode(particles, [bombs[i].center.x, bombs[i].center.y])
            del bombs[i]

    for npc in npcs:
        if npc.interacting:
            display.blit(npc_surface, (0, 0))
            if not npc.talk(display, npc_input, player, display):
                input["interact"] = False
        else:
            npc.check_funds(display)
            if player.inQuest:
                npc.update_quests(player)
                npc.show_quest_status(display)
            if player_center_x >= Mikhail.center.x - Mikhail.width / 2 and player_center_x <= Mikhail.center.x + Mikhail.width / 2 and player.center.y >= Mikhail.center.y - Mikhail.width / 2 and player.center.y <= Mikhail.center.y + Mikhail.width / 2 and not paused:
                M_surface = pygame.Surface((len("T to talk to Mikhail") * 7 + 4, 10), pygame.SRCALPHA).convert_alpha()
                M_surface.fill(npc_color)
                display.blit(M_surface, (player_center_x - len("T to talk to Mikhail") * 7 / 2 - 2, player.center.y - 40 - 2))
                render_text((player_center_x - len("T to talk to Mikhail") * 7 / 2, player.center.y - 40), "T to talk to Mikhail", display, "white")
            npc.reset_talk()

    count = 0




    player.quest_complete_text(display)
    player.powerup_collected(display, powerup)


# 1 - deliver (Deliver 100 arrows/watermelons)
# 2 - action (Break 100 barrels)

# A - arrows
# W - watermelons
# B - barrels

# M - arrow multiplier
# R - range


# Ex
# 1A100M10 (deliver 100 arrows for 100 arrow multiplier)
# 2B5R9 (Break 5 barrels for 9 more range)




# ----------------------------------------------------- Collision with stuff ------------------------------------------------------------
    # print(collidables["Bosses"])
    counter = 0
    # Barrels colliding with Barrels
    for i in range(len(collidables["Barrels"]) + 1 - 1, -1, -1):
        bodyA = player

        if i != len(collidables["Barrels"]):
            bodyA = collidables["Barrels"][i]

        for j in range(len(collidables["Barrels"]) - 1, -1, -1):
            counter += 1
            bodyB = collidables["Barrels"][j]

            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

            if collided:
                bodyA.move(normal * (depth / 2))
                bodyB.move(normal * -1 * (depth / 2))


    # Bombs colliding with Barrels
    for i in range(len(collidables["Bombs"]) - 1, -1, -1):
        bodyA = collidables["Bombs"][i]
        
        hit = False
        for j in range(len(collidables["Barrels"]) - 1, -1, -1):
            bodyB = collidables["Barrels"][j]
            counter += 1
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

            if collided:
                bodyB.health_bar.damage(bodyA.damage)
                bodyB.move(Vector((math.cos(bodyA.bomb_angle), math.sin(bodyA.bomb_angle))) * .1)
                delete_arrow(arrows, bodyA)
                del collidables["Bombs"][i]
                if bodyB.health_bar.health <= 0:
                    screen_shake = 10
                    delete_barrel(barrels, bodyB, collectables["Watermelons"], Tifanie, player)
                    del collidables["Barrels"][j]
                hit = True
                break  # okay to break because the arrow already hit something and it wont hit anything else

    # Arrows colliding with Barrels
    for i in range(len(collidables["Arrows"]) - 1, -1, -1):
        bodyA = collidables["Arrows"][i]

        hit = False
        for j in range(len(collidables["Barrels"]) - 1, -1, -1):
            bodyB = collidables["Barrels"][j]
            counter += 1
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)

            if collided:
                bodyB.health_bar.damage(bodyA.damage)
                bodyB.move(Vector((math.cos(bodyA.arrow_angle), math.sin(bodyA.arrow_angle))) * .1)
                delete_arrow(arrows, bodyA)
                del collidables["Arrows"][i]
                if bodyB.health_bar.health <= 0:
                    # screen_shake = 10
                    delete_barrel(barrels, bodyB, collectables["Watermelons"], Tifanie, player)
                    del collidables["Barrels"][j]
                hit = True
                break  # okay to break because the arrow already hit something and it wont hit anything else

        # Boss colliding with Arrows (only have one boss for now will have to split into another for loop probably)
        if hit == False and len(collidables["Bosses"]) > 0: # check if it already hit something
            bodyB = Tifanie
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
            if collided:
                bodyB.health_bar.damage(bodyA.damage)
                delete_arrow(arrows, bodyA)
                del collidables["Arrows"][i]
                if bodyB.health_bar.health <= 0:
                    
                    if not Tifanie.dead:
                        p = Collectable((Tifanie.center.x, Tifanie.center.y), 8, 8, black, bomb_images)
                        p.powerup = True
                        player.bomber = True
                        collectables["Powerups"].append(p)
                    Tifanie.death()
                

    # Player colliding with Shurikens
    for i in range(len(collidables["Shurikens"]) - 1, -1, -1):
        bodyB = collidables["Shurikens"][i]
        counter += 1
        collided, depth, normal = player.handle_collision(bodyB.normals(), player.normals(), bodyB)

        if collided:
            player.health_bar.damage(bodyB.damage)
            Tifanie.delete_shuriken(bodyB)
            del collidables["Shurikens"][i]
            if player.health_bar.health <= 0:
                x_distance = math.sqrt((player_center_x - spawnpoint.center.x) ** 2 + (player.center.y - spawnpoint.center.y) ** 2)
                v = Vector(((player_center_x - spawnpoint.center.x), (player.center.y - spawnpoint.center.y)))
                v.normalize()
                player.move_distance(v * -1, x_distance)
                t_x_distance = math.sqrt((Tifanie.center.x- tif_spawnpoint.center.x) ** 2 + (Tifanie.center.y - tif_spawnpoint.center.y) ** 2)
                t_v = Vector(((Tifanie.center.x - tif_spawnpoint.center.x), (Tifanie.center.y - tif_spawnpoint.center.y)))
                t_v.normalize()
                Tifanie.move_distance(t_v * -1, t_x_distance)
                Tifanie.temp_death()
                player.player_death()
                break
            player.move(normal * .05)


    # print(counter)






# ------------------------------------------------------- Rendering text / images ------------------------------------------------------------------

    render_text((12, 20), FPS_text, display)

    if input["stats"]: # hold tab to see stats
        render_text((150, 330), "Barrels busted:" + str(player.barrels_busted), display)
        render_text((150, 345), "Watermelons holding:" + str(len(player.inventory["Watermelons"])), display)
        render_text((150, 360), "Arrow multiplier:" + str(player.stats['M']), display)
        render_text((150, 375), "Range:" + str(player.stats['R']), display)





    # arrow on thej top left
    arrow_count = str(len(player.inventory["Arrows"]))
    UI_arrow = pygame.transform.rotate(arrow_images[len(arrow_images) // 2 - 1], 90)
    display.blit(UI_arrow.convert_alpha(), (310 - (UI_arrow.get_width() / 2 + 3), 30 - (UI_arrow.get_height() / 2) + 3))
    render_text((320, 30), arrow_count, display)
    render_text((320 + len(arrow_count) * 8 + 4, 30), "x" + str(player.stats["M"]), display)

    if paused:
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



        
    if screen_shake > 0:
        screen_shake -= 1
    
    render_offset = [0, 0]

    if screen_shake:
        render_offset[0] = random.randint(0, 8) - 4
        render_offset[1] = random.randint(0, 8) - 4
        
    
    if not paused:
        display.blit(overlay_surface, (0, 0))
    screen.blit(pygame.transform.scale(display, screen.get_size()), render_offset)
    pygame.display.flip()
    clock.tick(60)

    to_render_sorted = []

# Quit Pygame
pygame.quit()



