import pygame
import os

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







# Icons
watermelon_img = pygame.image.load('imgs/icons/melon_c.png')
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
bomb_images = convert_to_imgs('imgs/bomb')


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
    "Barrels" : barrel_images
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

def render_text(loc, word, surface, color="black"):
    col = loc[0]
    row = loc[1]

    divider = 0

    for letter in word:
        if letter == " ":
            divider += 1
            continue
        if color == "white":
            surface.blit(abc_white[letter.capitalize()].convert_alpha(), (col + divider * 7, row))
        elif color == "black":
            surface.blit(abc[letter.capitalize()].convert_alpha(), (col + divider * 7, row))
        elif color == "red":
            surface.blit(abc_red[letter.capitalize()].convert_alpha(), (col + divider * 7, row))
        divider += 1

def render_text_centered(loc, word, surface, color="black"):


    col = loc[0] - len(word) * 7 / 2
    row = loc[1]

    divider = 0

    for letter in word:
        if letter == " ":
            divider += 1
            continue
        if color == "white":
            surface.blit(abc_white[letter.capitalize()].convert_alpha(), (col + divider * 7, row))
        elif color == "black":
            surface.blit(abc[letter.capitalize()].convert_alpha(), (col + divider * 7, row))
        elif color == "red":
            surface.blit(abc_red[letter.capitalize()].convert_alpha(), (col + divider * 7, row))
        divider += 1



def lower_player(player):
    player.to_render.images = player.images[2::]

def raise_player(player):
    player.to_render.images = player.images


































A_img = pygame.image.load('imgs/a_2/A.png')
B_img = pygame.image.load('imgs/a_2/B.png')
C_img = pygame.image.load('imgs/a_2/C.png')
D_img = pygame.image.load('imgs/a_2/D.png')
E_img = pygame.image.load('imgs/a_2/E.png')
F_img = pygame.image.load('imgs/a_2/F.png')
G_img = pygame.image.load('imgs/a_2/G.png')
H_img = pygame.image.load('imgs/a_2/H.png')
I_img = pygame.image.load('imgs/a_2/I.png')
J_img = pygame.image.load('imgs/a_2/J.png')
K_img = pygame.image.load('imgs/a_2/K.png')
L_img = pygame.image.load('imgs/a_2/L.png')
M_img = pygame.image.load('imgs/a_2/M.png')
N_img = pygame.image.load('imgs/a_2/N.png')
O_img = pygame.image.load('imgs/a_2/O.png')
P_img = pygame.image.load('imgs/a_2/P.png')
Q_img = pygame.image.load('imgs/a_2/Q.png')
R_img = pygame.image.load('imgs/a_2/R.png')
S_img = pygame.image.load('imgs/a_2/S.png')
T_img = pygame.image.load('imgs/a_2/T.png')
U_img = pygame.image.load('imgs/a_2/U.png')
V_img = pygame.image.load('imgs/a_2/V.png')
W_img = pygame.image.load('imgs/a_2/W.png')
X_img = pygame.image.load('imgs/a_2/X.png')
Y_img = pygame.image.load('imgs/a_2/Y.png')
Z_img = pygame.image.load('imgs/a_2/Z.png')
ZERO_img = pygame.image.load('imgs/a_2/0.png')
ONE_img = pygame.image.load('imgs/a_2/1.png')
TWO_img = pygame.image.load('imgs/a_2/2.png')
THREE_img = pygame.image.load('imgs/a_2/3.png')
FOUR_img = pygame.image.load('imgs/a_2/4.png')
FIVE_img = pygame.image.load('imgs/a_2/5.png')
SIX_img = pygame.image.load('imgs/a_2/6.png')
SEVEN_img = pygame.image.load('imgs/a_2/7.png')
EIGHT_img = pygame.image.load('imgs/a_2/8.png')
NINE_img = pygame.image.load('imgs/a_2/9.png')
COLON_img = pygame.image.load('imgs/a_2/colon.png')
SLASH_img = pygame.image.load('imgs/a_2/slash.png')

abc = {
    "A": A_img,
    "B": B_img,
    "C": C_img,
    "D": D_img,
    "E": E_img,
    "F": F_img,
    "G": G_img,
    "H": H_img,
    "I": I_img,
    "J": J_img,
    "K": K_img,
    "L": L_img,
    "M": M_img,
    "N": N_img,
    "O": O_img,
    "P": P_img,
    "Q": Q_img,
    "R": R_img,
    "S": S_img,
    "T": T_img,
    "U": U_img,
    "V": V_img,
    "W": W_img,
    "X": X_img,
    "Y": Y_img,
    "Z": Z_img,
    "0": ZERO_img,
    "1": ONE_img,
    "2": TWO_img,
    "3": THREE_img,
    "4": FOUR_img,
    "5": FIVE_img,
    "6": SIX_img,
    "7": SEVEN_img,
    "8": EIGHT_img,
    "9": NINE_img,
    ":": COLON_img,
    "^": up_arrow,
    "`": down_arrow,
    "<": left_arrow,
    ">": right_arrow,
    "/": SLASH_img
}
A_img_white = pygame.image.load('imgs/a_3/A.png')
B_img_white = pygame.image.load('imgs/a_3/B.png')
C_img_white = pygame.image.load('imgs/a_3/C.png')
D_img_white = pygame.image.load('imgs/a_3/D.png')
E_img_white = pygame.image.load('imgs/a_3/E.png')
F_img_white = pygame.image.load('imgs/a_3/F.png')
G_img_white = pygame.image.load('imgs/a_3/G.png')
H_img_white = pygame.image.load('imgs/a_3/H.png')
I_img_white = pygame.image.load('imgs/a_3/I.png')
J_img_white = pygame.image.load('imgs/a_3/J.png')
K_img_white = pygame.image.load('imgs/a_3/K.png')
L_img_white = pygame.image.load('imgs/a_3/L.png')
M_img_white = pygame.image.load('imgs/a_3/M.png')
N_img_white = pygame.image.load('imgs/a_3/N.png')
O_img_white = pygame.image.load('imgs/a_3/O.png')
P_img_white = pygame.image.load('imgs/a_3/P.png')
Q_img_white = pygame.image.load('imgs/a_3/Q.png')
R_img_white = pygame.image.load('imgs/a_3/R.png')
S_img_white = pygame.image.load('imgs/a_3/S.png')
T_img_white = pygame.image.load('imgs/a_3/T.png')
U_img_white = pygame.image.load('imgs/a_3/U.png')
V_img_white = pygame.image.load('imgs/a_3/V.png')
W_img_white = pygame.image.load('imgs/a_3/W.png')
X_img_white = pygame.image.load('imgs/a_3/X.png')
Y_img_white = pygame.image.load('imgs/a_3/Y.png')
Z_img_white = pygame.image.load('imgs/a_3/Z.png')
ZERO_img_white = pygame.image.load('imgs/a_3/0.png')
ONE_img_white = pygame.image.load('imgs/a_3/1.png')
TWO_img_white = pygame.image.load('imgs/a_3/2.png')
THREE_img_white = pygame.image.load('imgs/a_3/3.png')
FOUR_img_white = pygame.image.load('imgs/a_3/4.png')
FIVE_img_white = pygame.image.load('imgs/a_3/5.png')
SIX_img_white = pygame.image.load('imgs/a_3/6.png')
SEVEN_img_white = pygame.image.load('imgs/a_3/7.png')
EIGHT_img_white = pygame.image.load('imgs/a_3/8.png')
NINE_img_white = pygame.image.load('imgs/a_3/9.png')
COLON_img_white = pygame.image.load('imgs/a_3/colon.png')
SLASH_img_white = pygame.image.load('imgs/a_3/slash.png')

abc_white = {
    "A": A_img_white,
    "B": B_img_white,
    "C": C_img_white,
    "D": D_img_white,
    "E": E_img_white,
    "F": F_img_white,
    "G": G_img_white,
    "H": H_img_white,
    "I": I_img_white,
    "J": J_img_white,
    "K": K_img_white,
    "L": L_img_white,
    "M": M_img_white,
    "N": N_img_white,
    "O": O_img_white,
    "P": P_img_white,
    "Q": Q_img_white,
    "R": R_img_white,
    "S": S_img_white,
    "T": T_img_white,
    "U": U_img_white,
    "V": V_img_white,
    "W": W_img_white,
    "X": X_img_white,
    "Y": Y_img_white,
    "Z": Z_img_white,
    "0": ZERO_img_white,
    "1": ONE_img_white,
    "2": TWO_img_white,
    "3": THREE_img_white,
    "4": FOUR_img_white,
    "5": FIVE_img_white,
    "6": SIX_img_white,
    "7": SEVEN_img_white,
    "8": EIGHT_img_white,
    "9": NINE_img_white,
    ":": COLON_img_white,
    "/": SLASH_img_white
}


def convert_to_imgs_t(directory):
    directory = directory
    files = [img for img in os.listdir(directory) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    files = sorted(files, reverse=True)
    images = [pygame.transform.scale(pygame.image.load(os.path.join(directory, img)), (48, 48)) for img in files]

    return images


flat_water_imgs = convert_to_imgs_t('imgs/water/flat')
split_water_imgs = convert_to_imgs_t('imgs/water/split')
hole_water_imgs = convert_to_imgs_t('imgs/water/hole')


A_img_red = pygame.image.load('imgs/a_4/A.png')
B_img_red = pygame.image.load('imgs/a_4/B.png')
C_img_red = pygame.image.load('imgs/a_4/C.png')
D_img_red = pygame.image.load('imgs/a_4/D.png')
E_img_red = pygame.image.load('imgs/a_4/E.png')
F_img_red = pygame.image.load('imgs/a_4/F.png')
G_img_red = pygame.image.load('imgs/a_4/G.png')
H_img_red = pygame.image.load('imgs/a_4/H.png')
I_img_red = pygame.image.load('imgs/a_4/I.png')
J_img_red = pygame.image.load('imgs/a_4/J.png')
K_img_red = pygame.image.load('imgs/a_4/K.png')
L_img_red = pygame.image.load('imgs/a_4/L.png')
M_img_red = pygame.image.load('imgs/a_4/M.png')
N_img_red = pygame.image.load('imgs/a_4/N.png')
O_img_red = pygame.image.load('imgs/a_4/O.png')
P_img_red = pygame.image.load('imgs/a_4/P.png')
Q_img_red = pygame.image.load('imgs/a_4/Q.png')
R_img_red = pygame.image.load('imgs/a_4/R.png')
S_img_red = pygame.image.load('imgs/a_4/S.png')
T_img_red = pygame.image.load('imgs/a_4/T.png')
U_img_red = pygame.image.load('imgs/a_4/U.png')
V_img_red = pygame.image.load('imgs/a_4/V.png')
W_img_red = pygame.image.load('imgs/a_4/W.png')
X_img_red = pygame.image.load('imgs/a_4/X.png')
Y_img_red = pygame.image.load('imgs/a_4/Y.png')
Z_img_red = pygame.image.load('imgs/a_4/Z.png')
ZERO_img_red = pygame.image.load('imgs/a_4/0.png')
ONE_img_red = pygame.image.load('imgs/a_4/1.png')
TWO_img_red = pygame.image.load('imgs/a_4/2.png')
THREE_img_red = pygame.image.load('imgs/a_4/3.png')
FOUR_img_red = pygame.image.load('imgs/a_4/4.png')
FIVE_img_red = pygame.image.load('imgs/a_4/5.png')
SIX_img_red = pygame.image.load('imgs/a_4/6.png')
SEVEN_img_red = pygame.image.load('imgs/a_4/7.png')
EIGHT_img_red = pygame.image.load('imgs/a_4/8.png')
NINE_img_red = pygame.image.load('imgs/a_4/9.png')
COLON_img_red = pygame.image.load('imgs/a_4/colon.png')


abc_red = {
    "A": A_img_red,
    "B": B_img_red,
    "C": C_img_red,
    "D": D_img_red,
    "E": E_img_red,
    "F": F_img_red,
    "G": G_img_red,
    "H": H_img_red,
    "I": I_img_red,
    "J": J_img_red,
    "K": K_img_red,
    "L": L_img_red,
    "M": M_img_red,
    "N": N_img_red,
    "O": O_img_red,
    "P": P_img_red,
    "Q": Q_img_red,
    "R": R_img_red,
    "S": S_img_red,
    "T": T_img_red,
    "U": U_img_red,
    "V": V_img_red,
    "W": W_img_red,
    "X": X_img_red,
    "Y": Y_img_red,
    "Z": Z_img_red,
    "0": ZERO_img_red,
    "1": ONE_img_red,
    "2": TWO_img_red,
    "3": THREE_img_red,
    "4": FOUR_img_red,
    "5": FIVE_img_red,
    "6": SIX_img_red,
    "7": SEVEN_img_red,
    "8": EIGHT_img_red,
    "9": NINE_img_red,
    ":": COLON_img_red
}
