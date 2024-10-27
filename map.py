from render import *
from Square import Hitbox
import random


class Tile(Hitbox):
    def __init__(self, center, width, height, color, images, type="land"):
        super().__init__(center, width, height, color)
        self.type = type
        if type == "water":
            self.images = [img.convert_alpha() for img in images]
        else:
            self.images = images.convert_alpha()
        self.to_render = Render(self.images, center, self.angle)

    def render(self, surf):
        self.to_render.render_single(surf)


    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle



class Tilemap:


    map_br = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    map_bl = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    map_tr = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    map_tl = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    def __init__(self) -> None:
        '''
        1 is land
        0 is water
        '''

        self.tiles = []

        for i in range(len(self.map_tl)):
            for j in range(len(self.map_tl[0])):
                if self.map_tl[i][j] == 1:
                    self.tiles.append(Tile((-(j * 48 + 48), -(i * 48 + 48)), 48, 48, white, grass_img))
                else:
                    self.tiles.append(Tile((-(j * 48 + 48), -(i * 48 + 48)), 48, 48, blue, flat_water_imgs if random.randint(0, 1) == 1 else split_water_imgs, type="water"))


        for i in range(len(self.map_tr)):
            for j in range(len(self.map_tr[0])):
                if self.map_tr[i][j] == 1:
                    self.tiles.append(Tile(((j * 48), -(i * 48 + 48)), 48, 48, white, grass_img))
                else:
                    self.tiles.append(Tile(((j * 48), -(i * 48 + 48)), 48, 48, blue, flat_water_imgs if random.randint(0, 1) == 1 else split_water_imgs, type="water"))

        for i in range(len(self.map_bl)):
            for j in range(len(self.map_bl[0])):
                if self.map_bl[i][j] == 1:
                    self.tiles.append(Tile((-(j * 48 + 48), i * 48), 48, 48, white, grass_img))
                else:
                    self.tiles.append(Tile((-(j * 48 + 48), i * 48), 48, 48, blue, flat_water_imgs if random.randint(0, 1) == 1 else split_water_imgs, type="water"))

        for i in range(len(self.map_br)):
            for j in range(len(self.map_br[0])):
                if self.map_br[i][j] == 1:
                    self.tiles.append(Tile((j * 48, i * 48), 48, 48, white, grass_img))
                else:
                    self.tiles.append(Tile((j * 48, i * 48), 48, 48, blue, flat_water_imgs if random.randint(0, 1) == 1 else split_water_imgs, type="water"))

