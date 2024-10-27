import pygame
import os

from vector import Vector

green = (0, 161, 82)
heather = (210, 145, 255)
indigo = (75, 0, 130)
pink = (255, 182, 193)
blue = (30, 144, 255)
white = (255, 255, 255)
black = (0, 0, 0)
linen = (250, 240, 230)
slate_grey = (174, 198, 224)
lime_green = (50, 205, 50)
grass_green = (142, 200, 64)
red = (220, 20, 60)
purple = (112, 41, 99)
npc_color = (47,79,79, 100)
damage_color = (255, 0, 0, 20)

screen_width, screen_height = 800, 800
display_width, display_height = 400, 400

mid_x = 200
mid_y = 200


def render_stack(surf, images, pos, rotation, spread):
    for i, img in enumerate(images):
        rotated_img = pygame.transform.rotate(img, rotation)
        surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2 , pos[1] - rotated_img.get_height() // 2 - i * spread))

def convert_to_imgs(directory):
    directory = directory
    files = [img for img in os.listdir(directory) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    files = sorted(files, reverse=True)
    images = [pygame.image.load(os.path.join(directory, img)) for img in files]

    return images

def extract_number(s, beginning):
    return int(s[len(beginning):-4])

def convert_to_imgs_numbers(directory, beginning):
    directory = directory
    files = [img for img in os.listdir(directory) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    files_sorted = sorted(files, key=lambda img: extract_number(img, beginning))
    images = [pygame.image.load(os.path.join(directory, img)) for img in files_sorted]

    return images




# Cards
a_o_d_img = pygame.image.load('imgs/diamonds/ace.png')


# Icons
watermelon_img = pygame.image.load('imgs/icons/watermelon_icon_3.png')
barrel_img = pygame.image.load('imgs/icons/barrel_icon.png')


# Terrain
grass_img = pygame.image.load('imgs/terrain/grass_patch.png')
rock_images = convert_to_imgs('imgs/rock')

# Car
alpha_images = convert_to_imgs_numbers('imgs/car', "car")

# Paused
paused_img = pygame.image.load('imgs/paused_screen/paused.png')
paused_controls_img = pygame.image.load('imgs/paused_screen/controls.png')

# Uno
Uno_images = convert_to_imgs('imgs/boss_uno/sprites')
shuriken_img = pygame.image.load('imgs/boss_uno/attacks/shuriken.png')

# Slime
slime_images = convert_to_imgs('imgs/slime')

# King
swordshot_image = pygame.image.load('imgs/swordshot/swordshot.png')
swordshot_image_black = pygame.image.load('imgs/swordshot/swordshot_black.png')
barrelking_images = convert_to_imgs_numbers('imgs/barrelking', 'BarrelKingDesign')

# NPC
dialogue_box = pygame.image.load('imgs/npc/dialogue_box.png')
dialogue_box = pygame.transform.scale(dialogue_box, (350, dialogue_box.get_height()))
quest_box = pygame.image.load('imgs/npc/quest_box.png')
quest_box_o = pygame.image.load('imgs/npc/quest_box_o.png')

# shuriken_img = pygame.transform.scale(shuriken_img, (3, 3)) # can use these for leave or soemthing

arrow_img = pygame.image.load('imgs/player/arrow/arrow_white.png')
barrel_images = convert_to_imgs('imgs/barrel')
player_images = convert_to_imgs('imgs/box')
arrow_images = convert_to_imgs('imgs/arrow')
watermelon_images = convert_to_imgs('imgs/watermelon')
banana_images = convert_to_imgs_numbers('imgs/banana', 'banana')
bomb_images = convert_to_imgs('imgs/bomb')

# Currency
coin_img = pygame.image.load('imgs/currency/coin.png')


# bridge
# bridge_part_0_images = convert_to_imgs_bridge('imgs/bridge/part_0')

# Butterfly
butterfly_images_stack = [convert_to_imgs('imgs/butterfly_stack/butterfly'),
                          convert_to_imgs('imgs/butterfly_stack/b_c_1'),
                          convert_to_imgs('imgs/butterfly_stack/b_c_2'),
                          convert_to_imgs('imgs/butterfly_stack/b_c_3'),
                          convert_to_imgs('imgs/butterfly_stack/b_c_4'),
                          convert_to_imgs('imgs/butterfly_stack/b_c_5')]



bigger_bomb_images = []
for i in range(len(bomb_images)):
    n = pygame.transform.scale(bomb_images[i], (bomb_images[i].get_width() + 20, bomb_images[i].get_height() + 20))
    bigger_bomb_images.append(n)

images = {
    "Arrows" : arrow_images,
    "Barrels" : barrel_images,
    "Bananas" : banana_images
}

# arrow keys
up_arrow = pygame.image.load('imgs/arrowkeys/up_arrow.png')
down_arrow = pygame.image.load('imgs/arrowkeys/down_arrow.png')
left_arrow = pygame.image.load('imgs/arrowkeys/left_arrow.png')
right_arrow = pygame.image.load('imgs/arrowkeys/right_arrow.png')
return_arrow = pygame.image.load('imgs/arrowkeys/return_arrow.png')
return_arrow = pygame.transform.scale(return_arrow, (return_arrow.get_width() + 4, return_arrow.get_height() + 3))


empty_image = pygame.image.load('imgs/arrow/arrow_0.png')


class Render:
    def __init__(self, images, loc, angle, spread=0):
        self.images = images
        self.loc = loc
        self.angle = angle
        self.spread = spread

        self.timer = 0
        try:
            self.frames = len(self.images)
        except:
            self.frames = 1

        self.frame_duration = 10
        self.current_frame = 0

        self.reversing = 1



    def render_stack(self, surf, hover=False):
        for i, img in enumerate(self.images):
            rotated_img = pygame.transform.rotate(img, self.angle)
            rotated_img.convert_alpha()
            surf.blit(rotated_img, (self.loc[0] - rotated_img.get_width() // 2 , self.loc[1] - rotated_img.get_height() // 2 - i * self.spread))

    def render_single(self, surf):
        rotated_img = pygame.transform.rotate(self.images, self.angle)
        surf.blit(rotated_img, (self.loc[0] - rotated_img.get_width() // 2 , self.loc[1] - rotated_img.get_height() // 2))

    def animate(self, surface, dt, type="single"):
        self.timer += dt
        

        if self.timer >= self.frame_duration:
            self.timer = 0
            
            # if self.current_frame == self.frames - 1:
            #     self.images = self.images[::-1]
            self.current_frame = (self.current_frame + self.reversing) % self.frames


                
        



        if type == "single":
            self.render_single_animation(surface)
        elif type == "stack":
            self.render_stack_animation(surface)
    
    def render_single_animation(self, surf):
        rotated_img = pygame.transform.rotate(self.images[self.current_frame], self.angle)
        surf.blit(rotated_img, (self.loc[0] - rotated_img.get_width() // 2 , self.loc[1] - rotated_img.get_height() // 2))

    def render_stack_animation(self, surf):
        for i, img in enumerate(self.images[self.current_frame]):
            rotated_img = pygame.transform.rotate(img, self.angle)
            rotated_img.convert_alpha()
            surf.blit(rotated_img, (self.loc[0] - rotated_img.get_width() // 2 , self.loc[1] - rotated_img.get_height() // 2 - i * self.spread))




# returns true if they are out of range
def limit_render(object, render_radius):
    mid_x, mid_y = 200, 200
    if object.center.x > mid_x + render_radius or object.center.x < mid_x - render_radius:
        return True
    if object.center.y > mid_y + render_radius or object.center.y < mid_y - render_radius:
        return True
    


def limit_collision(object, collision_center, collision_radius, collidables):
    # split these into two ifs and it becomes a t
    # if you combine them, becomes a square
    if object.center.x  <= collision_center.center.x + collision_radius and object.center.x >= collision_center.center.x - collision_radius and object.center.y <= collision_center.center.y + collision_radius and object.center.y >= collision_center.center.y - collision_radius:
        collidables.append(object)

def limit_collision_T(object, collision_center, collision_radius, collidables):
    if object.center.x  <= collision_center.center.x + collision_radius and object.center.x >= collision_center.center.x - collision_radius:
        collidables.append(object)
    if object.center.y <= collision_center.center.y + collision_radius and object.center.y >= collision_center.center.y - collision_radius:
        collidables.append(object)

def render_text(loc, word, surface, color="black", scale=1):
    col = loc[0]
    row = loc[1]

    divider = 0

    for letter in word:
        if letter == " ":
            divider += 1
            continue
        
        char = abc[letter.capitalize()][color]
        char = pygame.transform.scale(char, (char.get_width() * scale, char.get_height() * scale))
        surface.blit(char.convert_alpha(), (col + divider * (7 * scale), row))

        divider += 1

def render_text_centered(loc, word, surface, color="black", scale=1):


    col = loc[0] - len(word) * (7 * scale) / 2
    row = loc[1]

    divider = 0

    for letter in word:
        if letter == " ":
            divider += 1
            continue
        
        char = abc[letter.capitalize()][color]
        char = pygame.transform.scale(char, (char.get_width() * scale, char.get_height() * scale))
        surface.blit(char.convert_alpha(), (col + divider * (7 * scale), row))

        divider += 1


# Returns vector to mid from given vector
def vec_to_mid(point):
    return Vector(200 - point[0], 200 - point[1]).normalize()


def lower_player(player):
    player.to_render.images = player.images[2::]

def raise_player(player):
    player.to_render.images = player.images


black_text_folder = 'imgs/a_2/'
white_text_folder = 'imgs/a_3/'
red_text_folder = 'imgs/a_4/'

abc = {}

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    abc[letter] = {
        "black": pygame.image.load(f'{black_text_folder}{letter}.png'),
        "white": pygame.image.load(f'{white_text_folder}{letter}.png'),
        "red": pygame.image.load(f'{red_text_folder}{letter}.png')
    }


for number in "0123456789":
    abc[number] = {
        "black": pygame.image.load(f'{black_text_folder}{number}.png'),
        "white": pygame.image.load(f'{white_text_folder}{number}.png'),
        "red": pygame.image.load(f'{red_text_folder}{number}.png')
    }


abc[":"] = {
    "black": pygame.image.load(f'{black_text_folder}colon.png'),
    "white": pygame.image.load(f'{white_text_folder}colon.png'),
    "red": pygame.image.load(f'{red_text_folder}colon.png')
}

abc["/"] = {
    "black": pygame.image.load(f'{black_text_folder}slash.png'),
    "white": pygame.image.load(f'{white_text_folder}slash.png')
}

abc["-"] = {"black" : pygame.image.load(f'{black_text_folder}dash.png')}


abc["^"] = {"black" : up_arrow}
abc["`"] = {"black" : down_arrow}
abc["<"] = {"black" : left_arrow}
abc[">"] = {"black" : right_arrow}



def convert_to_imgs_t(directory):
    directory = directory
    files = [img for img in os.listdir(directory) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    files = sorted(files, reverse=True)
    images = [pygame.transform.scale(pygame.image.load(os.path.join(directory, img)), (48, 48)) for img in files]

    return images


flat_water_imgs = convert_to_imgs_t('imgs/water/flat')
split_water_imgs = convert_to_imgs_t('imgs/water/split')
hole_water_imgs = convert_to_imgs_t('imgs/water/hole')
