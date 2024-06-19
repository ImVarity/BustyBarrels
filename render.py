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





abc = {
    "A": pygame.image.load('imgs/alphabet/A.png'),
    "B": pygame.image.load('imgs/alphabet/B.png'),
    "C": pygame.image.load('imgs/alphabet/C.png'),
    "D": pygame.image.load('imgs/alphabet/D.png'),
    "E": pygame.image.load('imgs/alphabet/E.png'),
    "F": pygame.image.load('imgs/alphabet/F.png'),
    "G": pygame.image.load('imgs/alphabet/G.png'),
    "H": pygame.image.load('imgs/alphabet/H.png'),
    "I": pygame.image.load('imgs/alphabet/I.png'),
    "J": pygame.image.load('imgs/alphabet/J.png'),
    "K": pygame.image.load('imgs/alphabet/K.png'),
    "L": pygame.image.load('imgs/alphabet/L.png'),
    "M": pygame.image.load('imgs/alphabet/M.png'),
    "N": pygame.image.load('imgs/alphabet/N.png'),
    "O": pygame.image.load('imgs/alphabet/O.png'),
    "P": pygame.image.load('imgs/alphabet/P.png'),
    "Q": pygame.image.load('imgs/alphabet/Q.png'),
    "R": pygame.image.load('imgs/alphabet/R.png'),
    "S": pygame.image.load('imgs/alphabet/S.png'),
    "T": pygame.image.load('imgs/alphabet/T.png'),
    "U": pygame.image.load('imgs/alphabet/U.png'),
    "V": pygame.image.load('imgs/alphabet/V.png'),
    "W": pygame.image.load('imgs/alphabet/W.png'),
    "X": pygame.image.load('imgs/alphabet/X.png'),
    "Y": pygame.image.load('imgs/alphabet/Y.png'),
    "Z": pygame.image.load('imgs/alphabet/Z.png')
}
