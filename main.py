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
display = pygame.Surface((display_width, display_height))

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


box = Hitbox([display_width / 2, display_height / 2], 8, 8, blue)
boxtwo = Hitbox([250, 250], 16, 16, pink)
boxthree = Hitbox([300, 300], 8, 8, heather)


player_hitbox = box

boxes = [
    box, boxtwo, boxthree
]

to_render = [
    Render(player_images, [box.center.x, box.center.y], box.angle, 1),
    Render(barrel_images, [boxtwo.center.x, boxtwo.center.y], boxtwo.angle, 1.5),
    Render(arrow_images, [boxthree.center.x, boxthree.center.y], boxthree.angle, 1.5)
]


test_barrels = []

# for i in range(50):
#     sample_box = Hitbox([random.randrange(0, display_width), random.randrange(0, display_height)], 16, 16, pink)
#     boxes.append(sample_box)
#     to_render.append(Render(barrel_images, [sample_box.center.x, sample_box.center.y], sample_box.angle, 1.5))


for i in range(10):
    sample_barrel = Barrel([random.randrange(0, display_width), random.randrange(0, display_height)], 16, 16, pink)
    test_barrels.append(sample_barrel)



to_render_sorted = []
to_render_boxes = []

render_radius = 100




arrows = []

pause_color = (169, 169, 169, 128)
pause_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
pause_surface.fill(pause_color)

# Main loop
running = True
paused = False


font = pygame.font.SysFont("hoeflertext", 10)


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


    # limits the render distance by adding the things to be rendered to lists
    for i in range(len(to_render)):
        if boxes[i].center.x  > display_width / 2 + render_radius or boxes[i].center.x < display_width / 2 - render_radius:
            continue
        if boxes[i].center.y > display_height / 2 + render_radius or boxes[i].center.y < display_width / 2 - render_radius:
            continue
        to_render[i].loc = [boxes[i].center.x, boxes[i].center.y]
        to_render[i].angle = boxes[i].angle
        index = bisect.bisect_left([o.loc[1] for o in to_render_sorted], to_render[i].loc[1])
        to_render_sorted.insert(index, to_render[i])
        to_render_boxes.insert(index, boxes[i])

    # rendering what needs to be rendered
    for item in to_render_sorted:
        item.render_stack(display)


    # draws the hitbox
    box.draw_hitbox(display)
    boxtwo.draw_hitbox(display)
    boxthree.draw_hitbox(display)

    # direction player is facing
    direction = box.get_direction(input)
    if not paused:
        box.handle_rotation(rotation_input, player=True)
    

    if action_input["shoot"] and not paused:
        shot = Arrow((display_width / 2, display_height / 2), 16, 1, black)
        shot.direction = direction
        shot.arrow_angle = math.atan2(direction.y, direction.x) # gets the direction facing and rotates arrow to point that direction
        shot.set_angle(shot.arrow_angle)
        arrows.append(shot)


    for arrow in arrows:
        arrow.draw_hitbox(display)
        if not paused:
            arrow.update(rotation_input, direction)
        arrow.render(display)


    for barrel in test_barrels:
        barrel.update(rotation_input, direction)
        barrel.render(display)

    # moves everything opposite direction to simulate movement of a static player
    for i in range(1, len(boxes)):
        if not paused:
            boxes[i].handle_rotation(rotation_input)
            boxes[i].move(direction * -1)


    # deletes arrows that are off the screen
    for i in range(len(arrows) -1, -1, -1):
        if arrows[i].center.x < 0 or arrows[i].center.x > display_width or arrows[i].center.y < 0 or arrows[i].center.y > display_height:
            del arrows[i]



    for i in range(len(to_render_boxes)):
        bodyA = to_render_boxes[i]
        for j in range(len(to_render_boxes)):
            bodyB = to_render_boxes[j]
            if bodyB == bodyA:
                continue
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
            # depth - how far you move in before you start pushing it
            if collided:
                # so that the player doesnt move
                if bodyA == boxes[0]:
                    bodyB.move(normal * -1 * (depth / 3)) # if you divide depth by more, can be treated like slime
                    continue
                # so that the player doesnt move
                if bodyB == boxes[0]:
                    bodyA.move(normal * (depth / 3))
                    continue
                bodyA.move(normal * (depth / 3))
                bodyB.move(normal * -1 * (depth / 3))

    for i in range(len(test_barrels) + 1):
        bodyA = test_barrels[0]
        if i == len(test_barrels):
            bodyA = player_hitbox
        else:
            bodyA = test_barrels[i]


        for j in range(len(test_barrels)):

            bodyB = test_barrels[j]

            if bodyB == bodyA:
                continue
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
            # depth - how far you move in before you start pushing it
            if collided:
                # so that the player doesnt move
                if bodyA == boxes[0]:
                    bodyB.move(normal * -1 * (depth / 3)) # if you divide depth by more, can be treated like slime
                    continue
                # so that the player doesnt move
                if bodyB == boxes[0]:
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
    to_render_sorted = []
    to_render_boxes = []

# Quit Pygame
pygame.quit()
sys.exit()



