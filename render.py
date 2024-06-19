import pygame
import os

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




# Terrain
grass_img = pygame.image.load('imgs/terrain/grass_patch.png')

paused_img = pygame.image.load('imgs/paused_screen/paused.png')
paused_controls_img = pygame.image.load('imgs/paused_screen/controls.png')

# Uno
shuriken_img = pygame.image.load('imgs/boss_uno/attacks/shuriken.png')
# shuriken_img = pygame.transform.scale(shuriken_img, (3, 3)) # can use these for leave or soemthing

arrow_img = pygame.image.load('imgs/player/arrow/arrow_white.png')
barrel_images = convert_to_imgs('imgs/barrel')
player_images = convert_to_imgs('imgs/box')
arrow_images = convert_to_imgs('imgs/arrow')
watermelon_images = convert_to_imgs('imgs/watermelon')



class Render:
    def __init__(self, images, loc, angle, spread=0):
        self.images = images
        self.loc = loc
        self.angle = angle
        self.spread = spread

    def render_stack(self, surf, hover=False):
        for i, img in enumerate(self.images):
            img.convert_alpha()
            rotated_img = pygame.transform.rotate(img, self.angle)
            surf.blit(rotated_img, (self.loc[0] - rotated_img.get_width() // 2 , self.loc[1] - rotated_img.get_height() // 2 - i * self.spread))

    def render_single(self, surf):
        rotated_img = pygame.transform.rotate(self.images, self.angle)
        surf.blit(rotated_img, (self.loc[0] - rotated_img.get_width() // 2 , self.loc[1] - rotated_img.get_height() // 2))



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



A_img = pygame.image.load('imgs/alphabet/A.png')
B_img = pygame.image.load('imgs/alphabet/B.png')
C_img = pygame.image.load('imgs/alphabet/C.png')
D_img = pygame.image.load('imgs/alphabet/D.png')
E_img = pygame.image.load('imgs/alphabet/E.png')
F_img = pygame.image.load('imgs/alphabet/F.png')
G_img = pygame.image.load('imgs/alphabet/G.png')
H_img = pygame.image.load('imgs/alphabet/H.png')
I_img = pygame.image.load('imgs/alphabet/I.png')
J_img = pygame.image.load('imgs/alphabet/J.png')
K_img = pygame.image.load('imgs/alphabet/K.png')
L_img = pygame.image.load('imgs/alphabet/L.png')
M_img = pygame.image.load('imgs/alphabet/M.png')
N_img = pygame.image.load('imgs/alphabet/N.png')
O_img = pygame.image.load('imgs/alphabet/O.png')
P_img = pygame.image.load('imgs/alphabet/P.png')
Q_img = pygame.image.load('imgs/alphabet/Q.png')
R_img = pygame.image.load('imgs/alphabet/R.png')
S_img = pygame.image.load('imgs/alphabet/S.png')
T_img = pygame.image.load('imgs/alphabet/T.png')
U_img = pygame.image.load('imgs/alphabet/U.png')
V_img = pygame.image.load('imgs/alphabet/V.png')
W_img = pygame.image.load('imgs/alphabet/W.png')
X_img = pygame.image.load('imgs/alphabet/X.png')
Y_img = pygame.image.load('imgs/alphabet/Y.png')
Z_img = pygame.image.load('imgs/alphabet/Z.png')
ZERO_img = pygame.image.load('imgs/alphabet/0.png')
ONE_img = pygame.image.load('imgs/alphabet/1.png')
TWO_img = pygame.image.load('imgs/alphabet/2.png')
THREE_img = pygame.image.load('imgs/alphabet/3.png')
FOUR_img = pygame.image.load('imgs/alphabet/4.png')
FIVE_img = pygame.image.load('imgs/alphabet/5.png')
SIX_img = pygame.image.load('imgs/alphabet/6.png')
SEVEN_img = pygame.image.load('imgs/alphabet/7.png')
EIGHT_img = pygame.image.load('imgs/alphabet/8.png')
NINE_img = pygame.image.load('imgs/alphabet/9.png')

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
}
