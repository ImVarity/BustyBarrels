from pygame.locals import *
import pygame
import random
from Square import Hitbox
from render import *
import time
from game import GameLoop
from sounds import SFX
from vector import Vector

import json

flags = DOUBLEBUF


screen_width, screen_height = 800, 800


pygame.init()
pygame.mixer.init()


sounds = SFX()
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

talk_surface = pygame.Surface((display_width - 60, display_height - 60)).convert_alpha()
talk_surface.fill(npc_color)


tab_surface = pygame.Surface((display_width - 60, 150)).convert_alpha()
tab_surface.fill(npc_color)

mousePos = pygame.mouse.get_pos()

keys_held = set()

clock = pygame.time.Clock()
inputs = {
    "Movements" : {
        "up" : False,
        "down" : False,
        "left" : False,
        "right" : False
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
        "stats" : False,
        "next" : False
    }
}





# Bob = Slime([-40, -40], 12, 12, black, Vector(1, 0), Vector(player.center.x, player.center.y))

random_slime_count = 120

# slimes = [Bob]



bounding_boxes = [
    Hitbox((-24, -624), 624 * 2, 40, red),
    Hitbox((590, -24), 40, 624 * 2, red),
    Hitbox((-24, 590), 624 * 2, 40, red),
    Hitbox((-624, -24), 40, 624 * 2, red)
]

 


# with open('save_files.txt') as save_file:
#     data = json.load(save_file)

screen_shake = 0
pre_time = time.perf_counter()
last_time = time.time()

running = True
paused = False
Game = GameLoop()
Game.sounds = sounds
# Game.load_data(data)

saving_game = False

# --------------------------------------------------------------- Main loop ------------------------------------------------------------------

while running:


    now_time = time.perf_counter()
    dt = now_time - pre_time
    dt *= 60

    pre_time = time.perf_counter()



    screen.fill(white)
    display.fill(grass_green)
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    fps = clock.get_fps()
    FPS_text = "FPS:" + str(int(fps))


# ------------------------------------------------------- Handling input ------------------------------------------------------------------
    inputs["Action"]["shoot"] = False
    inputs["Action"]["throw"] = False

    npc_input = { # in main loop so that it only registers once per click
        "up" : False,
        "down" : False,
        "confirm" : False
    }

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            saving_game = True


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            if event.key == pygame.K_t:
                inputs["Action"]["interact"] = not inputs["Action"]["interact"]
            if event.key == pygame.K_k:
                inputs["Action"]["dash"] = True
            if event.key == pygame.K_UP:
                npc_input["up"] = True
            if event.key == pygame.K_DOWN:
                npc_input["down"] = True
            if event.key == pygame.K_RETURN:
                npc_input["confirm"] = True
            if event.key == pygame.K_SPACE:
                inputs["Action"]["throw"] = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                inputs["Action"]["shoot"] = True
            if event.key == pygame.K_i:
                inputs["Action"]["autofire"] = not inputs["Action"]["autofire"]
            if event.key == pygame.K_BACKQUOTE:
                inputs["Admin"]["hitboxes"] = not inputs["Admin"]["hitboxes"]
            if event.key == pygame.K_c:
                inputs["HUD"]["next"] = True
                if inputs["Action"]["interact"]:
                    sounds.menu_click.play()

    inputs["Rotation"]["counterclockwise"] = keys[pygame.K_e]
    inputs["Rotation"]["clockwise"] = keys[pygame.K_q]
    inputs["Rotation"]["reset"] = keys[pygame.K_z]
    if saving_game:
        inputs["Rotation"]["reset"] = True

    inputs["Movements"]["up"] = keys[pygame.K_w]
    inputs["Movements"]["down"] = keys[pygame.K_s]
    inputs["Movements"]["left"] = keys[pygame.K_a]
    inputs["Movements"]["right"] = keys[pygame.K_d]
    inputs["Movements"]["lock"] = keys[pygame.K_l]
    inputs["Movements"]["stats"] = keys[pygame.K_TAB]

    
    if inputs["Action"]["autofire"]:
        inputs["Action"]["shoot"] = True
    else:
        inputs["Action"]["shoot"] = keys[pygame.K_j]

    

    Game.npc_input = npc_input
    Game.inputs = inputs
    Game.paused = paused
    Game.to_render_sorted = [Game.player]
    Game.to_render = [Game.player]

    
    Game.main(dt, display)
    direction = Game.direction



    Game.update_and_render_tiles(display)
    Game.render_all(display)


    render_text((12, 12), FPS_text, display)

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

    screen_shake = Game.screen_shake

    if screen_shake > 0:
        screen_shake -= 1
    render_offset = [0, 0]
    if screen_shake:
        render_offset[0] = random.randint(0, 8) - 4
        render_offset[1] = random.randint(0, 8) - 4
    Game.screen_shake = screen_shake
        
    
    if not paused:
        display.blit(overlay_surface, (0, 0))

    if saving_game:
        print(inputs["Rotation"]["reset"])
        running = False
    screen.blit(pygame.transform.scale(display, screen.get_size()), render_offset)
    pygame.display.flip()
    clock.tick(60)

    
    


# Quit Pygame


# data = Game.save_data(data)
# with open('save_files.txt', 'w') as save_file:
#     json.dump(data, save_file, indent=4)

pygame.quit()



