from pygame.locals import *
import pygame
import random
from z_extensions.render import *
import time
from game import GameLoop
from sfx.sounds import SFX
import json

flags = DOUBLEBUF
screen_width, screen_height = 800, 800


pygame.init()
pygame.mixer.init()

sounds = SFX()

pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(loops=-1)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN,pygame.KEYUP])

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, 32)
pygame.display.set_caption('Busty Barrels')

display_width, display_height = 400, 400
display_width_c, display_height_c = display_width, display_height
mid_x, mid_y = display_width / 2, display_height /2
display = pygame.Surface([display_width_c, display_height_c])


npc_color = (47,79,79, 100)
npc_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha()
npc_surface.fill(npc_color)


main_menu_color = (0, 0, 0, 100)
main_menu_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha()
main_menu_surface.fill(main_menu_color)


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
        "interact" : False,
        "heal" : False
    },
    "Admin" : {
        "hitboxes" : False
    },
    "HUD" : {
        "stats" : False,
        "next" : False
    },
    "Tests" : {
        "click" : False,
        "hold" : False
    }
}



data = {
    "player" : {
        "location" : [],
        "abilities" : {
            "bomber" : False
        }
    },
    "barrels" : {
        "locations" : [],
        "health" : []
    },
    "bosses_killed" : [],
    "summon_barrels" : 0,
    "barrels_busted" : 0
}



screen_shake = 0
pre_time = time.perf_counter()
last_time = time.time()

running = True
paused = False
intro_paused_timer = 0
Game = GameLoop()
Game.sounds = sounds
song = "bg"


saving_game = False
background_color = (0, 0, 0)
grass_objects = []


frame = 0
frame_counter_og = 5
frame_counter = frame_counter_og
frame_speed = 1

underline_full = False
new_underline = True
underline_length = 0
underline_max_length = main_menu_saved_files.get_width()
underline_inc = 5




main_menu_selects = ["play", "saved files"]
file_selects = ["None", "FILE1", "FILE2"]
file = 0
select = 0



loading_timer = 120
loading = False
loading_color = (255,255,255)
loading_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha()
loading_surface.fill(loading_color)



# ----------------------------------------------------- Main loop ------------------------------------------------------------------

while running:
    now_time = time.perf_counter()
    dt = now_time - pre_time
    dt *= 60

    # dt *= 1.5 # could do this when fighting a boss?

    pre_time = time.perf_counter()


    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x, mouse_y = mouse_x // 2, mouse_y // 2

    # screen is the 800 x 800
    # display is the 400 x 400
    screen.fill(background_color)
    display.fill(background_color)



    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    fps = clock.get_fps()
    FPS_text = "FPS:" + str(int(fps))




# ------------------------------------------------------- Handling input ------------------------------------------------------------------
    inputs["Action"]["shoot"] = False
    inputs["Action"]["throw"] = False
    inputs["Action"]["interact"] = False
    inputs["Action"]["heal"] = False
    inputs["Tests"]["click"] = False

    pressed = False

    npc_input = { # in main loop so that it only registers once per click
        "up" : False,
        "down" : False,
        "confirm" : False
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # remove this is temp
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
            if event.key == pygame.K_h:
                inputs["Action"]["heal"] = True
            if event.key == pygame.K_c:
                inputs["Tests"]["click"] = True
            
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

        if event.type == pygame.MOUSEBUTTONUP:
            pressed = True

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

    inputs["Tests"]["hold"] = keys[pygame.K_8]
    # pressed = pygame.mouse.get_pressed()[0]


    # ------------- Game -------------


    Game.npc_input = npc_input
    Game.inputs = inputs
    Game.paused = paused
    Game.to_render_sorted = [Game.player]
    Game.to_render = [Game.player]

    
    Game.main(dt, display)
    direction = Game.direction



    Game.update_tiles()
    Game.update_grass()


    if Game.stage == "grasslands":
        background_color = grass_green
        Game.render_tiles(display)
        Game.render_grass(display)
    elif Game.stage == "blank":
        background_color = white
        screen.fill(black)
    elif Game.stage == "blink":
        background_color = black
        screen.fill(white)


# ------------------------------------------------ Handling Music ------------------------------------------------------------------

    Game.render_all(display)
    if song != Game.song:
        pygame.mixer.stop()
        pygame.mixer.music.load(f'{Game.song}')
        pygame.mixer.music.play(loops=-1)
        song = Game.song



# ------------------------------------------------ Main Menu ------------------------------------------------------------------

    
    if frame_counter < 0:
        frame += 1
        frame_counter = frame_counter_og

    frame_counter -= frame_speed * dt
    frame = frame % len(main_menu_titles)

    if inputs["Tests"]["click"]:
        select += 1
        select = select % len(main_menu_selects)
        new_underline = True
        underline_full = False


    if not Game.GameStart:
        display.blit(main_menu_titles[frame].convert_alpha(), (mid_x - main_menu_titles[frame].get_width() // 2, mid_y - main_menu_titles[frame].get_height() // 2 - 100))

        margin = 9

        # hovering over the play button
        if mouse_y > 220 - margin and mouse_y < 220 + margin + main_menu_play.get_height():
            if select != 0:
                select = 0
                new_underline = True
                underline_full = False
                sounds.menu_click.play()
            

        # hovering over the saved files button
        if mouse_y > 250 - margin and mouse_y < 250 + margin + main_menu_saved_files.get_height():
            if select != 1:
                select = 1
                new_underline = True
                underline_full = False
                sounds.menu_click.play()

        if file_selects[file] == "None":
            pass
            
        if file == 1:
            display.blit(file1selected.convert_alpha(), (140 + main_menu_saved_files.get_width() + margin, 220))

        if file == 2:
            display.blit(file2selected.convert_alpha(), (140 + main_menu_saved_files.get_width() + margin, 220))


        if main_menu_selects[select] == "play":
            if pressed:
                if file_selects[file] != "None":
                    try:
                        Game = GameLoop()
                        Game.sounds = sounds
                        song = "bg"
                        with open(f'{file_selects[file]}.txt') as save_file:
                            data = json.load(save_file)
                            Game.load_data(data)
                        loading = True
                    except:
                        print("no current save file")
                Game.GameStart = True


            if new_underline:
                new_underline = False
                underline_length = 0
                underline_inc = 5

            
            display.blit(main_menu_play.convert_alpha(), (140, 220))
            display.blit(main_menu_saved_files.convert_alpha(), (140, 250))
            pygame.draw.rect(display, white,  pygame.Rect(140, 234, underline_length, 3))


        elif main_menu_selects[select] == "saved files":
            if new_underline:
                new_underline = False
                underline_length = 0
                underline_inc = 5


            if mouse_y >= (270 + main_menu_saved_files.get_height()) - 5 and mouse_y <= (270 + main_menu_saved_files.get_height()) + file1.get_height() + 5:
                pygame.draw.rect(display, white, pygame.Rect(180, 250 + main_menu_saved_files.get_height() + 20 + file1.get_height() + 2, file1.get_width(), 2))
                if pressed:
                    sounds.menu_click.play()
                    file = 1 if file != 1 else 0

            if mouse_y >= (280 + main_menu_saved_files.get_height() + margin) - 5 and mouse_y <= (280 + main_menu_saved_files.get_height() + margin) + file2.get_height() + 5:
                pygame.draw.rect(display, white, pygame.Rect(180, 280 + main_menu_saved_files.get_height() + margin + file2.get_height() + 2, file2.get_width(), 2))
                if pressed:
                    sounds.menu_click.play()
                    file = 2 if file != 2 else 0

            display.blit(main_menu_play.convert_alpha(), (140,220))
            display.blit(main_menu_saved_files.convert_alpha(), (140, 250))

            display.blit(file1.convert_alpha(), (180, 250 + main_menu_saved_files.get_height() + 20))
            if file == 1:
                pygame.draw.rect(display, white, pygame.Rect(180, 250 + main_menu_saved_files.get_height() + 20 + file1.get_height() + 2, file1.get_width(), 2))
            


            display.blit(file2.convert_alpha(), (180, 250 + main_menu_saved_files.get_height() + 20 + margin + 10))
            if file == 2:
                pygame.draw.rect(display, white, pygame.Rect(180, 250 + main_menu_saved_files.get_height() + 20 + margin + 10 + file2.get_height() + 2, file2.get_width(), 2))



            pygame.draw.rect(display, white,  pygame.Rect(140, 264, underline_length, 3))

        
        if not underline_full:
            underline_length += underline_inc
            underline_inc += 1
        if underline_length >= underline_max_length:
            underline_length = underline_max_length
            underline_full = True
        





# ------------------------------- Handle the keybind introductions that pause the game -------------------------------------------


    if Game.intro_paused_timer > 0:
        intro_paused_timer = Game.intro_paused_timer + 60
        if intro_paused_timer == 1:
            paused = False
            intro_paused_timer = -1
        Game.intro_paused_timer = 0

    if intro_paused_timer:
        intro_paused_timer -= 1 * dt
        if intro_paused_timer < 60:
            intro_paused_timer = -1
        paused = True
        
    if intro_paused_timer < 0:
        paused = False
        intro_paused_timer = 0

    

# ------------------------------------------------ Display ------------------------------------------------------------------

    if loading:
        display.blit(loading_surface, (0, 0))
        # render_text_centered((mid_x, mid_y), "Loading", display, "black", scale=2)
        if loading_timer <= 120:
            display.blit(load_barrel.convert_alpha(), (mid_x - load_barrel.get_width() // 2 - 5 - load_barrel.get_width(), mid_y - load_barrel.get_height() // 2))
        if loading_timer <= 80:
            display.blit(load_barrel.convert_alpha(), (mid_x - load_barrel.get_width() // 2, mid_y - load_barrel.get_height() // 2))
        if loading_timer <= 40:
            display.blit(load_barrel.convert_alpha(), (mid_x + load_barrel.get_width() // 2 + 5, mid_y - load_barrel.get_height() // 2))

        loading_timer -= 1 * dt
    if loading_timer <= 0:
        loading = False


    if Game.GameStart:
        render_text((350, 12), FPS_text, display)
    # render_text((12, 380), f"{int(Game.player.center.x - Game.spawnpoint.center.x)} {int(Game.player.center.y - Game.spawnpoint.center.y)}", display)

    if paused:
        if not intro_paused_timer:
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
        render_offset[0] = random.randint(0, Game.shake_magnitude) - Game.shake_magnitude / 2
        render_offset[1] = random.randint(0, Game.shake_magnitude) - Game.shake_magnitude / 2
    Game.screen_shake = screen_shake

    
        

    if saving_game:
        running = False
        
    screen.blit(pygame.transform.scale(display, screen.get_size()), render_offset)
    pygame.display.flip()
    clock.tick(60)

    
    


# After exiting game


data = Game.save_data(data)
# with open('save_files.txt', 'w') as save_file:
#     json.dump(data, save_file, indent=4)
if file_selects[file] != "None":
    with open(f'{file_selects[file]}.txt', 'w') as save_file:
        json.dump(data, save_file, indent=4)


pygame.quit()



