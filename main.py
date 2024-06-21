import pygame
import math
import bisect
import random
from Square import Hitbox
from vector import Vector
from Circle import Circle
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
from tile import Tile
from render import *
import time


screen_width = 800
screen_height = 800




pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Busty Barrels')

display_width, display_height = 400, 400
mid_x, mid_y = display_width / 2, display_height /2
display = pygame.Surface((display_width, display_height))

pause_color = (169, 169, 169, 100)
pause_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
pause_surface.fill(pause_color)

overlay_color = (250, 240, 230, 45)
overlay_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
overlay_surface.fill(overlay_color)



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
    "dash": False

}

admin_input = {
    "hitboxes": False
}


# ------------------------------------------------------------ Player ------------------------------------------------------------------------

player = Player([0, 0], 8, 8, blue, health=500)
player_arrow = PlayerArrow([mid_x + 12, mid_y], 16, 16, blue)
spawnpoint = Barrel((0, 0), 8, 8, black)


cur_point = Hitbox((0, 0), 8, 8, black)

# ------------------------------------------------------------ Radius ------------------------------------------------------------------

render_radius = 200
collision_radius = 33


# -------------------------------------------------- Where items and objects are held --------------------------------------------------------------------------------

to_render = []
boxes = []
arrows = []
watermelons = []
collectables = {
    "Arrows" : [],
    "Watermelons" : []
}

random_barrel_count = 100
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
    barrels.append(Barrel([random.randrange(-display_width, display_width), random.randrange(-display_height, display_height)], 16, 16, pink, health=25))


# for i in range(100):
#     watermelons.append(Watermelon([random.randrange(0, display_width), random.randrange(0, display_height)], 12, 12, green))



# ------------------------------------------------- Bosses and NPCS ----------------------------------------------------------------------



font = pygame.font.Font('fonts/tiny.ttf', 8)


Tifanie = Uno([mid_x, mid_y], 32, 32, black)

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

def delete_arrow(arrows, arrow_to_delete):
    for i in range(len(arrows)):
        if arrows[i] == arrow_to_delete:
            # could draw like arrow in the ground
            del arrows[i]
            break


def delete_barrel(barrels, barrel_to_delete, watermelons, player):

    for i in range(len(barrels)):
        if barrels[i] == barrel_to_delete:
            # watermelons appear after breaking barrel
            watermelons.append(Collectable([barrels[i].center.x, barrels[i].center.y], 12, 12, green, watermelon_images))
            player.barrels_busted += 1
            del barrels[i]
            break


# ------------------------------------------------ Testing stuff that will be fixed in the future ------------------------------------------------

attack = False

attack_end = 120
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


quest = ""


# --------------------------------------------------------------- Main loop ------------------------------------------------------------------

while running:
    now_time = time.perf_counter()
    dt = now_time - pre_time
    dt *= 60
    pre_time = time.perf_counter()
    start_of_game_pause += 1



    screen.fill(white)
    display.fill(grass_green)
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    fps = clock.get_fps()

    FPS_text = "FPS:" + str(int(fps))


# ------------------------------------------------------- Handling input ------------------------------------------------------------------
    action_input["shoot"] = False

    npc_input = { # in main loop so that it only registers once per click
        "up" : False,
        "down" : False,
        "confirm" : False
    }

    if start_of_game_pause == 60:
        paused = not paused


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


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                action_input["shoot"] = True
            if event.key == pygame.K_i:
                action_input["autofire"] = not action_input["autofire"]
            if event.key == pygame.K_BACKQUOTE:
                admin_input["hitboxes"] = not admin_input["hitboxes"]
            if event.key == pygame.K_c:
                if input["interact"]:
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
        collectables["Arrows"].append(Collectable([random.randrange(int(Tifanie.center.x - mid_x), int(Tifanie.center.x + mid_x)), random.randrange(int(Tifanie.center.y - mid_y), int(Tifanie.center.y + mid_y))], 12, 12, black, arrow_images))


# ------------------------------------------------- Handling the rotation and direction and some updating -------------------------------------------------------
# -------------------------------------------- Other updating happens in the z-positiong updating so less for loops ----------------------------------------



    direction = player.get_direction(input)
    direction *= dt
    player.direction = direction


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
            player.knockback_power = 1
            player.knockback = True
            shot = Arrow((player.center.x, player.center.y), 16, 1, blue, player.looking)
            shot.arrow_angle_start = player.angle_looking
            arrows.append(shot)
            player.arrow_counter += 1
        else:
            player.inventory["Arrows"].pop()
            player.arrow_counter = 0
    


    player.update_actions(input)
    player.check_knockback()

    # NEED TO FIX
    attack_start += attack_inc
    if attack_start == attack_end:
        attack_start = 0
        if Tifanie.summoned and not Tifanie.dead:
            Tifanie.attack_one(player.angle_looking)
    

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
        "Bosses" : []
    }

    # just put player in here immediately, it will be sorted in place anyway
    to_render_sorted = [player]

    if not paused:
        spawnpoint.update(rotation_input, direction)

# ---------------------------------------- Sorting stuff that need to be ordered for correct z-position --------------------------------------------

    for npc in npcs:
        if not paused:
            npc.update(rotation_input, direction)
            limit_render(npc, render_radius)
            if player.center.x >= npc.center.x - npc.width / 2 and player.center.x <= npc.center.x + npc.width / 2 and player.center.y >= npc.center.y - npc.width / 2 and player.center.y <= npc.center.y + npc.width / 2:
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
                if holder[i].center.x < player.center.x + 8 and holder[i].center.x > player.center.x - 8 and holder[i].center.y < player.center.y + 8 and holder[i].center.y > player.center.y - 8:
                    holder[i].follow_player = True
                    holder[i].follow_speed = random.randrange(50, 200) / 10000
                    player.inventory[items].append(holder[i])
                    del holder[i]
                    continue
                holder[i].update(rotation_input, direction)
            
            index = bisect.bisect_left([o.center.y for o in to_render_sorted], collectables[items][i].center.y)
            to_render_sorted.insert(index, collectables[items][i])



    # UNO sorting
    for b in bosses:
        if not paused:
            b.update(rotation_input, direction)
            if b.summoned:
                for arrow in arrows:
                    if b.center.x  <= arrow.center.x + b.width / 2 and b.center.x >= arrow.center.x - b.width / 2 and b.center.y <= arrow.center.y + b.height / 2 and b.center.y >= arrow.center.y - b.height / 2:
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
                if barrel.center.x  <= arrow.center.x + barrel.width / 2 and barrel.center.x >= arrow.center.x - barrel.width / 2 and barrel.center.y <= arrow.center.y + barrel.height / 2 and barrel.center.y >= arrow.center.y - barrel.height / 2:
                    collidables["Arrows"].append(arrow)
                    collidables["Barrels"].append(barrel)
                    added = True
                
                    
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


    # dont need to fix z position of shurikens because always on top
    for i, shuriken in enumerate(Tifanie.shurikens):
        if not paused:
            shuriken.update(rotation_input, direction)
            
            # limit render distance
            if limit_render(shuriken, render_radius):
                continue

            limit_collision(shuriken, player, collision_radius, collidables["Shurikens"])


    # fixes z position of watermelons
    for watermelon in watermelons:
        if not paused:
            watermelon.update(rotation_input, direction)

            if watermelon.follow_player:
                diff_vec = Vector((player.center.x - watermelon.center.x, player.center.y - watermelon.center.y))
                watermelon.move(diff_vec * watermelon.follow_speed)
            
            if not watermelon.follow_player:
                if watermelon.center.x < player.center.x + 8 and watermelon.center.x > player.center.x - 8 and watermelon.center.y < player.center.y + 8 and watermelon.center.y > player.center.y - 8:
                    watermelon.follow_player = True
                    watermelon.follow_speed = random.randrange(50, 200) / 10000

            # 1 limits render distance
            limit_render(watermelon, render_radius)
        # 3 add to to-be-rendered
        # index = bisect.bisect_left([o.center.y for o in to_render_sorted], watermelon.center.y)
        # to_render_sorted.insert(index, watermelon)



# ------------------------------------------------------ Rendering objects -------------------------------------------------------

    # render tiles first
    for tile in tiles:
        tile.render(display)

    # arrow should be below everythign except tiles
    player_arrow.render(display)

    for melon in watermelons:
        melon.render(display)

    for melon in player.inventory["Watermelons"]:
        melon.render(display)

    for arrow in player.inventory["Arrows"]:
        arrow.render(display)



# ------------------------------------------------------- Boss stuff (to fix) -------------------------------------------------------

    if player.barrels_busted > 5 and not Tifanie.summoned:
        # Tifanie.summoned = True
        Tifanie.summoning = True
        tracking = Tifanie

    if Tifanie.summoning:
        Tifanie.summon_start += Tifanie.summon_increment

        if Tifanie.summon_start % Tifanie.summon_rise == 0:
            if Tifanie.summon_index > 0:
                Tifanie.summon_index -= 1
            else:
                tracking = player
                Tifanie.summoned = True
                Tifanie.summoning = False

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
            object.render(display)
            if object.summoned and not object.dead:
                object.draw_healthbar(display)
            # object.draw_hitbox(display)
        

        
        if admin_input["hitboxes"]:
            object.draw_hitbox(display)

    # because rendering after, always on top of everything


    for shuriken in Tifanie.shurikens:
        shuriken.render(display)

        if admin_input["hitboxes"]:
            shuriken.draw_hitbox(display)
        # shuriken.draw_hitbox(display)

    # spawnpoint.draw_hitbox(display)

# ------------------------------------------------------- Deleting stuff -----------------------------------------------------------


    # deletes arrows that are off the screen
    for i in range(len(arrows) -1, -1, -1):
        if math.sqrt((arrows[i].center.x - player.center.x) ** 2 + (arrows[i].center.y - player.center.y) ** 2) > player.stats["R"]:
            del arrows[i]
        # if arrows[i].center.x < 0 or arrows[i].center.x > display_width or arrows[i].center.y < 0 or arrows[i].center.y > display_height:
        #     del arrows[i]

    # deletes all the Tifanie shots that pass a certain radius
    for i in range(len(Tifanie.shurikens) - 1, -1, -1):
        if math.sqrt((Tifanie.center.x - Tifanie.shurikens[i].center.x) ** 2 + (Tifanie.center.y - Tifanie.shurikens[i].center.y) ** 2) > Tifanie.delete_radius:
            del Tifanie.shurikens[i]

    for npc in npcs:
        if npc.interacting:
            npc.talk(display, npc_input)
        else:
            if player.center.x >= Mikhail.center.x - Mikhail.width / 2 and player.center.x <= Mikhail.center.x + Mikhail.width / 2 and player.center.y >= Mikhail.center.y - Mikhail.width / 2 and player.center.y <= Mikhail.center.y + Mikhail.width / 2 and not paused:
                render_text((player.center.x - len("T to talk to Mikhail") * 7 / 2, player.center.y - 15), "T to talk to Mikhail", display)
            npc.reset_talk()

    count = 0
    # print(Mikhail.active_quest)



    active_quest = Mikhail.active_quest

    transaction = False


    if len(active_quest) > 0: # just pressed enter to confirm a quest
        if active_quest[0] == "1": # means there there is a delivery quest
            end_idx = 0
            labor_amount = ""
            for i in range(2, len(active_quest)):
                if ord(active_quest[i]) > 57:
                    labor_amount = active_quest[2:i]
                    end_idx = i
                    break

            if len(player.inventory[quest_encryption[active_quest[1]]]) >= int(labor_amount):
                # taking away how many items you collected
                player.inventory[quest_encryption[active_quest[1]]] = player.inventory[quest_encryption[active_quest[1]]][int(labor_amount)::]

                # rewarding the player

                reward = active_quest[end_idx]
                reward_amount = active_quest[end_idx + 1::]

                player.stats[reward] += int(reward_amount)


                transaction = True
            else:
                transaction = False

        if active_quest[0] == "2": # breaking barrels quest
            end_idx = 0
            labor_amount = ""
            for i in range(2, len(active_quest)):
                if ord(active_quest[i]) > 57: # just checks if the unicode number is greater than the last unicode number for a number which is 9 because unicode numbers for letters are all after numbers
                    labor_amount = active_quest[2:i]
                    end_idx = i
                    break
            
            if player.barrels_busted >= int(labor_amount):
                # rewarding the player

                reward = active_quest[end_idx]
                reward_amount = active_quest[end_idx + 1::]

                player.stats[reward] += int(reward_amount)
                transaction = True
            else:
                transaction = False

    if transaction == True:
        npc.exchange(active_quest)

            
        



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
                    delete_barrel(barrels, bodyB, collectables["Watermelons"], player)
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
                x_distance = math.sqrt((player.center.x - spawnpoint.center.x) ** 2 + (player.center.y - spawnpoint.center.y) ** 2)
                v = Vector(((player.center.x - spawnpoint.center.x), (player.center.y - spawnpoint.center.y)))
                v.normalize()
                player.move_distance(v * -1, x_distance)
                player.player_death()
                break
            player.move(normal * .05)


    # print(Tifanie.summoned)


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
    display.blit(UI_arrow, (310 - (UI_arrow.get_width() / 2 + 3), 30 - (UI_arrow.get_height() / 2) + 3))
    render_text((320, 30), arrow_count, display)
    render_text((320 + len(arrow_count) * 8 + 4, 30), "x" + str(player.stats["M"]), display)

    if paused:
        display.blit(paused_img, (mid_x - paused_img.get_width() // 2, mid_y - paused_img.get_height() // 2 - 150))

        start = -30
        render_text((mid_x - len("controls") * 7 / 2, mid_y + start - 100), "controls", display)
        render_text((mid_x - len("WASD to move") * 7 / 2, mid_y + start - 70), "WASD to move", display)
        render_text((mid_x - len("Q and E to rotate") * 7 / 2, mid_y + start - 50), "Q and E to rotate", display)
        render_text((mid_x - len("T to interact") * 7 / 2, mid_y + start - 30), "T to interact", display)
        render_text((mid_x - len("J to shoot") * 7 / 2, mid_y + start - 10), "J to shoot", display)
        render_text((mid_x - len("K to dash") * 7 / 2, mid_y + start + 10), "K to dash", display)
        render_text((mid_x - len("L to lock look direction") * 7 / 2, mid_y + start + 30), "L to lock look direction", display)
        render_text((mid_x - len("I to autoshoot") * 7 / 2, mid_y + start + 50), "I to autoshoot", display)
        render_text((mid_x - len("Arrow keys to navigate") * 7 / 2, mid_y + start + 70), "Arrow keys to navigate", display)
        render_text((mid_x - len("Enter to confirm") * 7 / 2, mid_y + start + 90), "Enter to confirm", display)
        render_text((mid_x - len("Tab for stats") * 7 / 2, mid_y + start + 110), "Tab for stats", display)
        render_text((mid_x - len("Escape to pause") * 7 / 2, mid_y + start + 130), "Escape to pause", display)



        display.blit(pause_surface, (0, 0))
    if not paused:
        display.blit(overlay_surface, (0, 0))
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick(60)

    to_render_sorted = []

# Quit Pygame
pygame.quit()



