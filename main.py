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
from health import HealthBar
from watermelon import Watermelon
from render import *


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

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Collision')

display_width, display_height = 400, 400
mid_x, mid_y = display_width / 2, display_height /2
display = pygame.Surface((display_width, display_height))

pause_color = (169, 169, 169, 128)
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
}

rotation_input = {
    "reset": False,
    "clockwise" : False,
    "counterclockwise" : False
}

action_input = {
    "ultimate" : False,
    "shoot" : False,
    "shootlock": False,
    "dash": False
}


player = Player([mid_x, mid_y], 8, 8, blue)

render_radius = 200
collision_radius = 20

boxes = []
arrows = []
to_render = []
watermelons = [

]

random_barrel_count = 50

barrels = [
    Barrel([150, 150], 16, 16, pink, health=500),
    Barrel([250, 150], 16, 16, pink, health=500),
    Barrel([150, 250], 16, 16, pink, health=500),
    Barrel([250, 250], 16, 16, pink, health=500)
]


for i in range(random_barrel_count):
    barrels.append(Barrel([random.randrange(0, display_width), random.randrange(0, display_height)], 16, 16, pink, health = 100))


# for i in range(10):
#     watermelons.append(Watermelon([random.randrange(0, display_width), random.randrange(0, display_height)], 12, 12, green))





health_bar = HealthBar(10, blue)

# Main loop
running = True
paused = False


font = pygame.font.SysFont("khmersangammn", 10)


dash_speed = 3

dash_friction = .03
dash_start = 0
dash_end = 12
dash_increment = 1


knock_start = 0
knock_end = 6
knock_increment = 1


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



while running:
    screen.fill(white)
    display.fill(linen)
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
            if event.key == pygame.K_k:
                action_input["dash"] = True


        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_j:
            #     action_input["shoot"] = True
            if event.key == pygame.K_i:
                action_input["shootlock"] = not action_input["shootlock"]



    rotation_input["counterclockwise"] = keys[pygame.K_e]
    rotation_input["clockwise"] = keys[pygame.K_q]
    rotation_input["reset"] = keys[pygame.K_z]

    input["up"] = keys[pygame.K_w]
    input["down"] = keys[pygame.K_s]
    input["left"] = keys[pygame.K_a]
    input["right"] = keys[pygame.K_d]

    action_input["shoot"] = keys[pygame.K_j]




    if dash_start == dash_end:
        dash_start = 0
        dash_speed = 3
        action_input["dash"] = False


    
    direction = player.get_direction(input)

    # print(Vector((mid_x - player.center.x, mid_y - player.center.y)))
    
    # so player will catch up when leaving the center
    difference_vec = Vector((mid_x - player.center.x, mid_y - player.center.y))
    player.move(difference_vec * player.scroll_speed)
    direction -= difference_vec * player.scroll_speed


    if action_input["shootlock"]:
        player.looking = player.looking
    else:
        player.looking = player.last_looked

    if action_input["shoot"] and not paused:
        player.knockback = True
        shot = Arrow((player.center.x, player.center.y), 16, 1, blue, player.looking)
        arrows.append(shot)
    
    if knock_start < knock_end:
        knock_start += knock_increment
    else:
        knock_start = 0
        player.knockback = False

    if player.knockback == True:
        knock_start += knock_increment
        player.move(player.looking * -1 * player.knockback)

        
        


    if not paused:
        player.update(rotation_input)


    if action_input["dash"]:
        dash_start += dash_increment
        dash_speed -= dash_friction
        if direction.x == 0 and direction.y == 0:
            direction = player.looking * dash_speed
        else:
            direction *= dash_speed
    

    

    # just put player in here immediately, it will be sorted in place anyway
    to_render_sorted = [player]
    collidables = []

    # fixes z position
    for i in range(len(barrels)):
        if not paused:
            barrels[i].update(rotation_input, direction) # such a pain.. have to update before checking
            # limits the render distance by adding the things to be rendered to lists
            if barrels[i].center.x  > mid_x + render_radius or barrels[i].center.x < mid_x - render_radius:
                continue
            if barrels[i].center.y > mid_y + render_radius or barrels[i].center.y < mid_y - render_radius:
                continue

            for arrow in arrows:
                if barrels[i].center.x  <= arrow.center.x + barrels[i].width / 2 and barrels[i].center.x >= arrow.center.x - barrels[i].width / 2 and barrels[i].center.y <= arrow.center.y + barrels[i].height / 2 and barrels[i].center.y >= arrow.center.y - barrels[i].height / 2:
                    collidables.append(barrels[i])

            # split these into two ifs and it becomes a t
            if barrels[i].center.x  <= player.center.x + collision_radius and barrels[i].center.x >= player.center.x - collision_radius and barrels[i].center.y <= player.center.y + collision_radius and barrels[i].center.y >= player.center.y - collision_radius:
                collidables.append(barrels[i])

        index = bisect.bisect_left([o.center.y for o in to_render_sorted], barrels[i].center.y)
        to_render_sorted.insert(index, barrels[i])

    # fixes z position
    for i in range(len(arrows)):
        if not paused:
            arrows[i].update(rotation_input, direction)
        
        collidables.append(arrows[i])
        index = bisect.bisect_left([o.center.y for o in to_render_sorted], arrows[i].center.y)
        to_render_sorted.insert(index, arrows[i])


    for i in range(len(watermelons)):
        if not paused:
            watermelons[i].update(rotation_input, direction)

            # 1 limits render distance
            if watermelons[i].center.x  > mid_x + render_radius or watermelons[i].center.x < mid_x - render_radius:
                continue
            if watermelons[i].center.y > mid_y + render_radius or watermelons[i].center.y < mid_y - render_radius:
                continue

        for arrow in arrows: # 2 add to collidables if near arrow
            if watermelons[i].center.x  <= arrow.center.x + watermelons[i].width / 2 and watermelons[i].center.x >= arrow.center.x - watermelons[i].width / 2 and watermelons[i].center.y <= arrow.center.y + watermelons[i].height / 2 and watermelons[i].center.y >= arrow.center.y - watermelons[i].height / 2:
                collidables.append(watermelons[i])

        # 3 add to to-be-rendered
        index = bisect.bisect_left([o.center.y for o in to_render_sorted], watermelons[i].center.y)
        to_render_sorted.insert(index, watermelons[i])


    # every item including player
    for object in to_render_sorted:
        if isinstance(object, Barrel):
            object.render(display)
            object.draw_healthbar(display)
        
        elif isinstance(object, Player):
            object.render(display)
            object.draw_hitbox(display)
            object.draw_healthbar(display)

        elif isinstance(object, Arrow):
            object.render(display)

        elif isinstance(object, Watermelon):
            object.render(display)
            
        # object.draw_hitbox(display)




    # deletes arrows that are off the screen
    for i in range(len(arrows) -1, -1, -1):
        if arrows[i].center.x < 0 or arrows[i].center.x > display_width or arrows[i].center.y < 0 or arrows[i].center.y > display_height:
            del arrows[i]



    for i in range(len(collidables) + 1): # +1 to account for player collision
        bodyA = player
        if i != len(collidables):
            bodyA = collidables[i]

        for j in range(len(collidables)):
            bodyB = collidables[j]

            if bodyB == bodyA:
                continue
            if isinstance(bodyB, Arrow):
                continue
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
            # depth - how far you move in before you start pushing it
            if collided:
                # so that the player doesnt move
                if bodyA == player:
                    bodyA.move(direction * -1)
                    bodyB.move(normal * -1 * (depth / 2)) # if you divide depth by more, can be treated like slime
                    continue
                # so that the player doesnt move
                if bodyB == player:
                    bodyA.move(normal * (depth / 2))
                    continue
                
                if isinstance(bodyA, Arrow) and isinstance(bodyB, Barrel):
                    bodyB.health_bar.damage(bodyA.damage)
                    bodyB.move(Vector((math.cos(bodyA.arrow_angle), math.sin(bodyA.arrow_angle))) * .1)
                    delete_arrow(arrows, bodyA)
                    if bodyB.health_bar.health <= 0:
                        delete_barrel(barrels, bodyB, watermelons)
                        continue
                    continue

                bodyA.move(normal * (depth / 2))
                bodyB.move(normal * -1 * (depth / 2))
            

    if paused:
        display.blit(paused_img, (mid_x - paused_img.get_width() // 2, mid_y - paused_img.get_height() // 2))

    # Update the display
    FPS_text_rect = FPS_text_surface.get_rect(center=(28, 12))
    barrel_count_text_rect = barrel_count_text_surface.get_rect(center=(28, 24))
    watermelon_count_text_rect = watermelon_count_text_surface.get_rect(center=(40, 36))


    display.blit(FPS_text_surface, FPS_text_rect)
    display.blit(barrel_count_text_surface, barrel_count_text_rect)
    display.blit(watermelon_count_text_surface, watermelon_count_text_rect)
    if paused:
        display.blit(pause_surface, (0, 0))
    display.blit(overlay_surface, (0, 0))
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick(60)

    to_render_sorted = []

# Quit Pygame
pygame.quit()



