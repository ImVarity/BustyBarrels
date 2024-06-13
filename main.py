import pygame
import sys
import math
import bisect
import random
from Square import Square
from vector import Vector
from Circle import Circle
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

box = Square([display_width / 2, display_height / 2], 8, 8, blue)
boxtwo = Square([250, 250], 16, 16, pink)
boxthree = Square([300, 300], 16, 16, heather)


player_hitbox = box

boxes = [
    box, boxtwo, boxthree
]

to_render = [
    Render(player_images, [box.center.x, box.center.y], box.angle, 1),
    Render(barrel_images, [boxtwo.center.x, boxtwo.center.y], boxtwo.angle, 1.5),
    Render(arrow_images, [boxthree.center.x, boxthree.center.y], boxthree.angle, 1.5)
]


for i in range(50):
    sample_box = Square([random.randrange(0, display_width), random.randrange(0, display_height)], 16, 16, pink)
    boxes.append(sample_box)
    to_render.append(Render(barrel_images, [sample_box.center.x, sample_box.center.y], sample_box.angle, 1.5))


to_render_sorted = []
to_render_boxes = []

render_radius = 100

arrows = []
arrows_to_render = []

arrow_hitbox = Square([display_width / 2, display_height / 2], 8, 8, black)

# Main loop
running = True
while running:
    screen.fill(white)
    display.fill(white)
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                pass

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
    box.draw(display)
    boxtwo.draw(display)
    boxthree.draw(display)


    direction = box.get_direction(input)
    box.handle_rotation(rotation_input, player=True)


    if action_input["shoot"]:
        shot = Square([display_width / 2, display_height / 2], 8, 8, black)
        shot.direction = direction
        if direction.x == 0 and direction.y == 0:
            shot.direction = Vector((1, 0))
        shot.arrow_angle = math.atan2(direction.y, direction.x)
        shot.self_rotate_arrow(shot.arrow_angle)

        print(direction)
        arrows.append(shot)
        
        arrows_to_render.append(Render(arrow_images, [shot.center.x, shot.center.y], shot.angle + (shot.arrow_angle * 180 / math.pi), 1.5))

    if len(arrows) > 0:
        print(arrows[0].direction)
        print(arrows[0].arrow_angle * 180 / math.pi)



    # moves everything opposite direction to simulate movement of a static player
    for i in range(1, len(boxes)):
        boxes[i].handle_rotation(rotation_input)
        boxes[i].move(direction * -1)


    for i in range(len(arrows)):
        arrows[i].draw(display)
        # arrow.move_arrow()
        arrows[i].move(arrows[i].direction + (direction * -1 * arrows[i].arrow_velocity * boxes[0].velocity))
        arrows[i].handle_rotation(rotation_input)
        arrows_to_render[i].loc = [arrows[i].center.x, arrows[i].center.y]
        arrows_to_render[i].angle = -arrows[i].arrow_angle * 180 / math.pi

        arrows_to_render[i].render_stack(display)


    


        # arrow.move_arrow()
        # arrow.handle_projectile_rotation(rotation_input)

    # boxtwo.draw_projection(screen, normalstwo)
    # box.draw_projection(display, normals)

    for i in range(len(to_render_boxes)):
        bodyA = to_render_boxes[i]
        
        for j in range(len(to_render_boxes)):
            bodyB = to_render_boxes[j]

            if bodyB == bodyA:
                continue
            collided, depth, normal = bodyA.handle_collision(bodyB.normals(), bodyA.normals(), bodyB)
            if collided:
                # so that the player doesnt move
                if bodyA == boxes[0]: 
                    bodyB.move(normal * -1 * (depth / 2))
                    continue
                # so that the player doesnt move
                if bodyB == boxes[0]:
                    bodyA.move(normal * (depth / 2))
                    continue
                bodyA.move(normal * (depth / 2))
                bodyB.move(normal * -1 * (depth / 2))
            



    # Update the display

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    to_render_sorted = []
    to_render_boxes = []

# Quit Pygame
pygame.quit()
sys.exit()



