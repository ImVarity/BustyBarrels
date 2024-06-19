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

heather = (210, 145, 255)
indigo = (75, 0, 130)
pink = (255, 182, 193)
blue = (30, 144, 255)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 161, 82)
linen = (250, 240, 230)
slate_grey = (174, 198, 224)
lime_green = (50, 205, 50)
grass_green = (142, 200, 64)
red = (220, 20, 60)

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Collision')

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
    "interact": False
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


player = Player([0, 0], 8, 8, blue, health=500)
player_arrow = PlayerArrow([mid_x + 12, mid_y], 16, 16, blue)
test = Barrel([mid_x + 12, mid_y], 16, 16, blue)

 
# print(player.center.x, player.center.y)

render_radius = 200
collision_radius = 33

to_render = []

boxes = []
arrows = []
watermelons = []
collectables = {
    "Arrows" : []
}

random_barrel_count = 10

barrels = [
    Barrel([150, 150], 16, 16, pink, health=500),
    Barrel([250, 150], 16, 16, pink, health=500),
    Barrel([150, 250], 16, 16, pink, health=500),
    Barrel([250, 250], 16, 16, pink, health=500)
]


for i in range(40):
    collectables["Arrows"].append(Collectable([random.randrange(0, display_width), random.randrange(0, display_height)], 12, 12, black, arrow_images))


for i in range(random_barrel_count):
    barrels.append(Barrel([random.randrange(0, display_width), random.randrange(0, display_height)], 16, 16, pink, health=random.randrange(250, 500)))


# for i in range(100):
#     watermelons.append(Watermelon([random.randrange(0, display_width), random.randrange(0, display_height)], 12, 12, green))




# Main loop
running = True
paused = False


font = pygame.font.Font('fonts/tiny.ttf', 8)


boss = Uno([mid_x, mid_y], 32, 32, black)

bosses = [boss]

Mikhail = NPC([0, 200], 32, 32, red, player_images)

npcs = [Mikhail]

map = [
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0],
]


tiles = []


for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == 1:
            tiles.append(Tile((j * 48 - 24, i * 48 - 24), 48, 48, white, grass_img))



def delete_arrow(arrows, arrow_to_delete):
    for i in range(len(arrows)):
        if arrows[i] == arrow_to_delete:
            # could draw like arrow in the ground
            del arrows[i]
            break

def delete_barrel(barrels, barrel_to_delete, watermelons):
    for i in range(len(barrels)):
        if barrels[i] == barrel_to_delete:
            # watermelons appear after breaking barrel
            watermelons.append(Watermelon((barrels[i].center.x, barrels[i].center.y), 12, 12, green, 20))
            del barrels[i]
            break


attack = False

attack_end = 360
attack_start = 0
attack_inc = 1

tracker = 0


pre_time = time.perf_counter()
while running:
    now_time = time.perf_counter()
    dt = now_time - pre_time
    dt *= 60
    pre_time = time.perf_counter()
    tracker += 30



    screen.fill(white)
    display.fill(grass_green)
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    fps = clock.get_fps()
    FPS_text = "FPS: " + str(int(fps))
    FPS_text_surface = font.render(FPS_text, True, (0, 0, 0))
    barrel_count_text = "Barrels: " + str(len(barrels))
    barrel_count_text_surface = font.render(barrel_count_text, True, (0, 0, 0))

    watermelon_count_text = "Watermelons: " + str(len(watermelons))
    watermelon_count_text_surface = font.render(watermelon_count_text, True, (0, 0, 0))


    # Handle events
    action_input["shoot"] = False

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
    
    if action_input["autofire"]:
        action_input["shoot"] = True
    else:
        action_input["shoot"] = keys[pygame.K_j]



    if len(collectables["Arrows"]) < 30:
        collectables["Arrows"].append(Collectable([random.randrange(int(boss.center.x - mid_x), int(boss.center.x + mid_x)), random.randrange(int(boss.center.y - mid_y), int(boss.center.y + mid_y))], 12, 12, black, arrow_images))




    direction = player.get_direction(input)
    direction *= dt
    player.direction = direction

    if not paused:
        player.update(rotation_input, action_input, direction)


        
    player.update_actions(input)
    player.check_knockback()


    # so player will catch up when leaving the center
    if not paused:
        difference_vec = Vector((mid_x - player.center.x, mid_y - player.center.y))
        player.move(difference_vec * player.scroll_speed)
        direction -= difference_vec * player.scroll_speed



    if action_input["shoot"] and not paused and len(player.inventory["Arrows"]) > 0:
        player.inventory["Arrows"].pop()
        player.knockback_power = 1
        player.knockback = True
        shot = Arrow((player.center.x, player.center.y), 16, 1, blue, player.looking)
        shot.arrow_angle_start = player.angle_looking
        arrows.append(shot)


    for i in range(len(player.inventory["Arrows"])):
        if not paused:
            diff_vec = Vector((player.center.x - player.inventory["Arrows"][i].center.x, player.center.y - player.inventory["Arrows"][i].center.y))
            player.inventory["Arrows"][i].move(diff_vec * player.inventory["Arrows"][i].follow_speed)
            player.inventory["Arrows"][i].update(rotation_input, direction)

    attack_start += attack_inc
    if attack_start == attack_end:
        attack_start = 0
        boss.attack_one(player.angle_looking)
    

    if not paused:
        player_arrow.update(player.looking, player.center)



    # just put player in here immediately, it will be sorted in place anyway
    to_render_sorted = [player]
    collidables = []

    for tile in tiles:
        if not paused:
            tile.update(rotation_input, direction)


    for npc in npcs:
        if not paused:
            npc.update(rotation_input, direction)
            limit_render(npc, render_radius)

            if player.center.x >= npc.center.x - npc.width / 2 and player.center.x <= npc.center.x + npc.width / 2 and player.center.y >= npc.center.y - npc.width / 2 and player.center.y <= npc.center.y + npc.width / 2:
                if input["interact"]:
                    npc.interacting = True

            if not input["interact"]:
                npc.interacting = False


        index = bisect.bisect_left([o.center.y for o in to_render_sorted], npc.center.y)
        to_render_sorted.insert(index, npc)
    

    for i in range(len(collectables["Arrows"]) - 1, -1, -1):
        if not paused:
        
            if collectables["Arrows"][i].center.x < player.center.x + 8 and collectables["Arrows"][i].center.x > player.center.x - 8 and collectables["Arrows"][i].center.y < player.center.y + 8 and collectables["Arrows"][i].center.y > player.center.y - 8:
                collectables["Arrows"][i].follow_player = True
                collectables["Arrows"][i].follow_speed = random.randrange(50, 200) / 10000
                player.inventory["Arrows"].append(collectables["Arrows"][i])
                del collectables["Arrows"][i]
                continue
                    
            
            collectables["Arrows"][i].update(rotation_input, direction)
        index = bisect.bisect_left([o.center.y for o in to_render_sorted], collectables["Arrows"][i].center.y)
        to_render_sorted.insert(index, collectables["Arrows"][i])


    # UNO sorting
    for b in bosses:
        if not paused:

            b.update(rotation_input, direction)
            for arrow in arrows:
                if b.center.x  <= arrow.center.x + b.width / 2 and b.center.x >= arrow.center.x - b.width / 2 and b.center.y <= arrow.center.y + b.height / 2 and b.center.y >= arrow.center.y - b.height / 2:
                    collidables.append(arrow)
                    collidables.append(b)

        index = bisect.bisect_left([o.center.y for o in to_render_sorted], b.center.y)
        to_render_sorted.insert(index, b)





    # fixes z position
    for barrel in barrels:
        if not paused:
            barrel.update(rotation_input, direction) # such a pain.. have to update before checking

            # limits the render distance by not allowing things outside of range to be added to to_render
            if limit_render(barrel, render_radius):
                continue

            for arrow in arrows:
                if barrel.center.x  <= arrow.center.x + barrel.width / 2 and barrel.center.x >= arrow.center.x - barrel.width / 2 and barrel.center.y <= arrow.center.y + barrel.height / 2 and barrel.center.y >= arrow.center.y - barrel.height / 2:
                    collidables.append(arrow)
                    collidables.append(barrel)

            limit_collision_T(barrel, player, collision_radius, collidables)

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
    for i, shuriken in enumerate(boss.shurikens):
        if not paused:
            shuriken.update(rotation_input, direction)
            
            # limit render distance
            if limit_render(shuriken, render_radius):
                continue

            limit_collision(shuriken, player, collision_radius, collidables)



        
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
        index = bisect.bisect_left([o.center.y for o in to_render_sorted], watermelon.center.y)
        to_render_sorted.insert(index, watermelon)

    for tile in tiles:
        tile.render(display)

    player_arrow.render(display)

    # every item including player
    for object in to_render_sorted:
        
        if isinstance(object, Player):
            object.render(display)
            # object.draw_hitbox(display)
            # object.draw_healthbar(display)

        elif isinstance(object, NPC):
            object.render(display)


        elif isinstance(object, Barrel):
            object.render(display)
            object.draw_healthbar(display)
        elif isinstance(object, Arrow):
            object.render(display)

        elif isinstance(object, Watermelon):
            object.render(display)

        elif isinstance(object, Collectable):
            object.render(display) 
            # object.draw_hitbox(display)

        elif isinstance(object, Uno):
            object.render(display)
            object.draw_healthbar(display)
            object.draw_hitbox(display)
        

        
        if admin_input["hitboxes"]:
            object.draw_hitbox(display)

    # because rendering after, always on top of everything
    for arrow in player.inventory["Arrows"]:
        arrow.render(display)

    for shuriken in boss.shurikens:
        shuriken.render(display)
        # shuriken.draw_hitbox(display)


    # deletes arrows that are off the screen
    for i in range(len(arrows) -1, -1, -1):
        if arrows[i].center.x < 0 or arrows[i].center.x > display_width or arrows[i].center.y < 0 or arrows[i].center.y > display_height:
            del arrows[i]

    # deletes all the boss shots that pass a certain radius
    for i in range(len(boss.shurikens) - 1, -1, -1):
        if math.sqrt((boss.center.x - boss.shurikens[i].center.x) ** 2 + (boss.center.y - boss.shurikens[i].center.y) ** 2) > boss.delete_radius:
            del boss.shurikens[i]

    for npc in npcs:
        if npc.interacting:
            npc.talk(display)
        else:
            npc.reset_talk()

    count = 0
    # print(len(collidables) * len(collidables))
    for i in range(len(collidables) + 1): # +1 to account for player collision
        bodyA = player
        if i != len(collidables):
            bodyA = collidables[i]

        for j in range(len(collidables)):
            bodyB = collidables[j]

            if bodyB == bodyA:
                continue

            if isinstance(bodyB, Arrow): # only arrow will collide with others as bodyA (should do if hitting everything)
                continue
            if isinstance(bodyB, NPC): # so you can only interact with them
                continue
            if isinstance(bodyB, Shuriken) and isinstance(bodyA, Shuriken): # so that they dont collide
                continue
            if isinstance(bodyA, Watermelon) and isinstance(bodyB, Watermelon): # never collide
                continue
            
            

            if isinstance(bodyA, Uno) and isinstance(bodyB, Player) or isinstance(bodyA, Player) and isinstance(bodyB, Uno): # never collide
                continue
            if isinstance(bodyA, Uno) and isinstance(bodyB, Shuriken) or isinstance(bodyA, Shuriken) and isinstance(bodyB, Uno): # never collide
                continue
            if isinstance(bodyA, Shuriken) and isinstance(bodyB, Barrel) or isinstance(bodyA, Barrel) and isinstance(bodyB, Shuriken): # never collide
                continue



            count += 1
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
            # depth - how far you move in before you start pushing it
            if collided:

                if bodyA == player:

                    if isinstance(bodyB, Shuriken):
                        bodyA.move(normal * .05)
                        continue

                    bodyA.move(normal * (depth / 2)) # moves plater so that the player camera moves
                    bodyB.move(normal * -1 * (depth / 2)) # if you divide depth by more, can be treated like slime
                    continue
                
                if isinstance(bodyA, Arrow) and isinstance(bodyB, Barrel):
                    bodyB.health_bar.damage(bodyA.damage)
                    bodyB.move(Vector((math.cos(bodyA.arrow_angle), math.sin(bodyA.arrow_angle))) * .1)
                    delete_arrow(arrows, bodyA)
                    if bodyB.health_bar.health <= 0:
                        delete_barrel(barrels, bodyB, watermelons)
                        continue
                    continue
                    
                if isinstance(bodyA, Arrow) and isinstance(bodyB, Uno) or isinstance(bodyA, Uno) and isinstance(bodyB, Arrow):
                    bodyB.health_bar.damage(bodyA.damage)
                    delete_arrow(arrows, bodyA)
                    continue


                bodyA.move(normal * (depth / 2))
                bodyB.move(normal * -1 * (depth / 2))
    # print(count)

    # Update the display
    FPS_text_rect = FPS_text_surface.get_rect(center=(28, 12))
    barrel_count_text_rect = barrel_count_text_surface.get_rect(center=(28, 24))
    watermelon_count_text_rect = watermelon_count_text_surface.get_rect(center=(40, 36))


    display.blit(FPS_text_surface, FPS_text_rect)
    display.blit(barrel_count_text_surface, barrel_count_text_rect)
    display.blit(watermelon_count_text_surface, watermelon_count_text_rect)


    if paused:
        display.blit(paused_controls_img, (mid_x - paused_controls_img.get_width() // 2, mid_y - paused_controls_img.get_height() // 2))
        display.blit(paused_img, (mid_x - paused_img.get_width() // 2, mid_y - paused_img.get_height() // 2 - 100))
        display.blit(pause_surface, (0, 0))
    if not paused:
        display.blit(overlay_surface, (0, 0))
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick(60)

    to_render_sorted = []

# Quit Pygame
pygame.quit()



