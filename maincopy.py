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
from game import GameLoop
from map import Tilemap
from sounds import SFX
flags = DOUBLEBUF


screen_width, screen_height = 800, 800


pygame.init()
pygame.mixer.init()



# dash_sound = pygame.mixer.Sound('sfx/grabitem.wav')
# collect_sound_2 = pygame.mixer.Sound('sfx/collectitem2.wav')
# explosion_sound = pygame.mixer.Sound('sfx/explosion.wav')
# menu_click = pygame.mixer.Sound('sfx/menuclick.wav')
# arrow_shot = pygame.mixer.Sound('sfx/arrow_shot.wav')
# arrow_shot.set_volume(3)

# arrow_shot2 = pygame.mixer.Sound('sfx/arrow_sound2.wav')
# # swing = pygame.mixer.Sound('sfx/swing_sound.wav')
# damage = pygame.mixer.Sound('sfx/damage.mp3')
# throw = pygame.mixer.Sound('sfx/throw.wav')
# stick = pygame.mixer.Sound('sfx/stick.wav')

# explosion_sound.set_volume(.2)
# pygame.mixer.music.load('sfx/bgm.mp3')

# pygame.mixer.music.play(loops=-1)

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


# ------------------------------------------------------------ Player ------------------------------------------------------------------------





# ------------------------------------------------------------ Radius ------------------------------------------------------------------



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


random_barrel_count = 75
random_arrow_count = 50

check = Barrel([150, 150], 16, 16, pink, health=500)

barrels = [
    check,
    Barrel([250, 150], 16, 16, pink, health=500),
    Barrel([150, 250], 16, 16, pink, health=500),
    Barrel([250, 250], 16, 16, pink, health=500)
]




# ------------------------------------------------- Bosses and NPCS ----------------------------------------------------------------------


Tifanie = Uno([mid_x + 16, mid_y + 16], 32, 32, purple)

bosses = [Tifanie]

Mikhail = NPC([0, -40], 64, 64, red, rock_images)

npcs = [Mikhail]

# Bob = Slime([-40, -40], 12, 12, black, Vector(1, 0), Vector(player.center.x, player.center.y))

random_slime_count = 120

# slimes = [Bob]

# -------------------------------------------------- Map stuff that needs to be moved somewhere else ------------------------------------------------


bounding_boxes = [
    Hitbox((-24, -624), 624 * 2, 40, red),
    Hitbox((590, -24), 40, 624 * 2, red),
    Hitbox((-24, 590), 624 * 2, 40, red),
    Hitbox((-624, -24), 40, 624 * 2, red)
]

            



# ------------------------------------------------------ Useful functions ------------------------------------------------------------



    

# ------------------------------------------------ Testing stuff that will be fixed in the future ------------------------------------------------



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


screen_shake = 0
last_time = time.time()


Game = GameLoop()
Game.sounds = sounds
# Map = Tilemap()

# --------------------------------------------------------------- Main loop ------------------------------------------------------------------

while running:
    now_time = time.perf_counter()
    dt = now_time - pre_time
    dt *= 60
    # dt = min(1.2, dt) # dont want to go over
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
            running = False

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
    Game.to_render_sorted = [Game.player]

    print(dt)

    Game.main(dt, display)

    # print(Game.dt)
    direction = Game.direction
    # player.direction = direction



    Game.update_and_render_tiles(display)
            
    Game.render_all(display)

    render_text((12, 12), FPS_text, display)


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
    screen.blit(pygame.transform.scale(display, screen.get_size()), render_offset)
    pygame.display.flip()
    clock.tick(60)


# Quit Pygame
pygame.quit()



