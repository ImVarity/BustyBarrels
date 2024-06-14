import pygame
import sys
import math
import bisect
import random
from Square import Hitbox
from vector import Vector
from Circle import Circle
from arrow import Arrow
from barrel import Barrel
from player import Player
from render import *

screen_width = 800
screen_height = 800

heather = (210, 145, 255)
indigo = (75, 0, 130)
pink = (255, 182, 193)
blue = (30, 144, 255)
white = (255, 255, 255)
black = (0, 0, 0)




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
    "shoot" : False
}



player = Player([mid_x, mid_y], 8, 8, blue)

render_radius = 200
collision_radius = 20


boxes = []
arrows = []
to_render = []



barrels = [
    Barrel([50, 50], 16, 16, pink),
    Barrel([100, 100], 16, 16, pink)
]


# for i in range(200):
#     barrels.append(Barrel([random.randrange(0, display_width), random.randrange(0, display_height)], 16, 16, pink))


# for i in range(50):
#     barrels.append(Barrel([150, 150], 16, 16, pink))


# Main loop
running = True
paused = False


font = pygame.font.SysFont("microsoftsansserif", 8)


print(pygame.font.get_fonts())
while running:
    screen.fill(white)
    display.fill(white)
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    fps = clock.get_fps()
    FPS_text = "FPS: " + str(int(fps))
    FPS_text_surface = font.render(FPS_text, True, (0, 0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused


    rotation_input["counterclockwise"] = keys[pygame.K_e]
    rotation_input["clockwise"] = keys[pygame.K_q]
    rotation_input["reset"] = keys[pygame.K_z]

    input["up"] = keys[pygame.K_w]
    input["down"] = keys[pygame.K_s]
    input["left"] = keys[pygame.K_a]
    input["right"] = keys[pygame.K_d]

    action_input["shoot"] = keys[pygame.K_j]


    direction = player.get_direction(input)
    last_looked = player.last_looked

    if not paused:
        player.update(rotation_input)
    player.render(display)
    player.draw_hitbox(display)



    if action_input["shoot"] and not paused:
        shot = Arrow((mid_x, mid_y), 16, 1, black, last_looked)
        arrows.append(shot)

    
    

    barrels_sorted = []
    collidables = []


    
    for i in range(len(barrels)):
        if not paused:
            barrels[i].update(rotation_input, direction) # such a pain.. have to update before checking
            # limits the render distance by adding the things to be rendered to lists
            if barrels[i].center.x  > mid_x + render_radius or barrels[i].center.x < mid_x - render_radius:
                continue
            if barrels[i].center.y > mid_y + render_radius or barrels[i].center.y < mid_y - render_radius:
                continue
            if barrels[i].center.x  <= mid_x + collision_radius and barrels[i].center.x >= mid_x - collision_radius:
                collidables.append(barrels[i])
            if barrels[i].center.y <= mid_y + collision_radius and barrels[i].center.y >= mid_y - collision_radius:
                collidables.append(barrels[i])

        index = bisect.bisect_left([o.center.y for o in barrels_sorted], barrels[i].center.y)
        barrels_sorted.insert(index, barrels[i])




    for arrow in arrows:
        arrow.draw_hitbox(display)
        if not paused:
            arrow.update(rotation_input, direction)
        arrow.render(display)


    for barrel in barrels_sorted:
        barrel.draw_hitbox(display)
        barrel.render(display)

    
    

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
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
            # depth - how far you move in before you start pushing it
            if collided:
                # so that the player doesnt move
                if bodyA == player:
                    bodyB.move(normal * -1 * (depth / 3)) # if you divide depth by more, can be treated like slime
                    continue
                # so that the player doesnt move
                if bodyB == player:
                    bodyA.move(normal * (depth / 3))
                    continue
                bodyA.move(normal * (depth / 3))
                bodyB.move(normal * -1 * (depth / 3))
            



    # Update the display
    FPS_text_rect = FPS_text_surface.get_rect(center=(24, 12))

    display.blit(FPS_text_surface, FPS_text_rect)
    if paused:
        display.blit(pause_surface, (0, 0))
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick(60)

    barrels_sorted = []

# Quit Pygame
pygame.quit()
sys.exit()



