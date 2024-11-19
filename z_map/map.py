from z_extensions.render import *
from z_extensions.Square import Hitbox
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
        [2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
        [3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
        [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 1, 3, 1, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 3, 3, 3, 1, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 3, 1, 2, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
        [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0],
        [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        ]
    map_bl = [
        [2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
        [3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
        [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
        [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
        [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0],
        [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    ]
    map_tr = [
        [2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
        [3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
        [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1],
        [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
        [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0],
        [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    ]
    map_tl = [
        [2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
        [3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
        [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
        [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0],
        [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    ]

    def __init__(self) -> None:
        '''
        2 is land
        1 is water
        3 is grass patch
        '''

        self.tiles = []
        self.grass = []
        self.patch_count = 40

        for i in range(len(self.map_tl)):
            for j in range(len(self.map_tl[0])):
                if self.map_tl[i][j] == 2:
                    self.tiles.append(Tile((-(j * 48 + 48), -(i * 48 + 48)), 48, 48, white, grass_patch))
                elif self.map_tl[i][j] == 1:
                    self.tiles.append(Tile((-(j * 48 + 48), -(i * 48 + 48)), 48, 48, blue, flat_water_imgs if random.randint(0, 1) == 1 else split_water_imgs, type="water"))
                elif self.map_tl[i][j] == 3:
                    for _ in range(self.patch_count):
                        random_x = random.randint(-(j * 48 + 48) - 24, -(j * 48 + 48) + 24)
                        random_y = random.randint(-(i * 48 + 48) - 24, -(i * 48 + 48) + 24)
                        random_z = random.randint(0, len(grass_parts) - 1)
                        self.grass.append(Grass(random_x, random_y, grass_parts[random_z], ((random_x + grass_parts[random_z].get_width() // 2), (random_y + grass_parts[random_z].get_height() // 2 - grass_parts[random_z].get_height() // 2)), 5, 5, black))
                else:
                    continue


        for i in range(len(self.map_tr)):
            for j in range(len(self.map_tr[0])):
                if self.map_tr[i][j] == 2:
                    self.tiles.append(Tile(((j * 48), -(i * 48 + 48)), 48, 48, white, grass_patch))
                elif self.map_tr[i][j] == 1:
                    self.tiles.append(Tile(((j * 48), -(i * 48 + 48)), 48, 48, blue, flat_water_imgs if random.randint(0, 1) == 1 else split_water_imgs, type="water"))
                elif self.map_tr[i][j] == 3:
                    for _ in range(self.patch_count):
                        random_x = random.randint((j * 48) - 24, (j * 48) + 24)
                        random_y = random.randint(-(i * 48 + 48) - 24, -(i * 48 + 48) + 24)
                        random_z = random.randint(0, len(grass_parts) - 1)
                        self.grass.append(Grass(random_x, random_y, grass_parts[random_z], ((random_x + grass_parts[random_z].get_width() // 2), (random_y + grass_parts[random_z].get_height() // 2 - grass_parts[random_z].get_height() // 2)), 5, 5, black))
                else:
                    continue

        for i in range(len(self.map_bl)):
            for j in range(len(self.map_bl[0])):
                if self.map_bl[i][j] == 2:
                    self.tiles.append(Tile((-(j * 48 + 48), i * 48), 48, 48, white, grass_patch))
                elif self.map_bl[i][j] == 1:
                    self.tiles.append(Tile((-(j * 48 + 48), i * 48), 48, 48, blue, flat_water_imgs if random.randint(0, 1) == 1 else split_water_imgs, type="water"))
                elif self.map_bl[i][j] == 3:
                    for _ in range(self.patch_count):
                        random_x = random.randint(-(j * 48 + 48) - 24, -(j * 48 + 48) + 24)
                        random_y = random.randint(i * 48 - 24, i * 48 + 24)
                        random_z = random.randint(0, len(grass_parts) - 1)
                        self.grass.append(Grass(random_x, random_y, grass_parts[random_z], ((random_x + grass_parts[random_z].get_width() // 2), (random_y + grass_parts[random_z].get_height() // 2 - grass_parts[random_z].get_height() // 2)), 5, 5, black))
                else:
                    continue

        for i in range(len(self.map_br)):
            for j in range(len(self.map_br[0])):
                if self.map_br[i][j] == 2:
                    self.tiles.append(Tile((j * 48, i * 48), 48, 48, white, grass_patch))
                elif self.map_br[i][j] == 1:
                    self.tiles.append(Tile((j * 48, i * 48), 48, 48, blue, flat_water_imgs if random.randint(0, 1) == 1 else split_water_imgs, type="water"))
                elif self.map_br[i][j] == 3:
                    for _ in range(self.patch_count):
                        random_x = random.randint(j * 48 - 24, j * 48 + 24)
                        random_y = random.randint(i * 48 - 24, i * 48 + 24)
                        random_z = random.randint(0, len(grass_parts) - 1)
                        self.grass.append(Grass(random_x, random_y, grass_parts[random_z], ((random_x + grass_parts[random_z].get_width() // 2), (random_y + grass_parts[random_z].get_height() // 2 - grass_parts[random_z].get_height() // 2)), 5, 5, black))
                else:
                    continue
        




class Grass(Hitbox):
    def __init__(self, x, y, image, center, width, height, color):
        super().__init__(center, width, height, color)
        self.x = x
        self.y = y
        self.sway_angle = 0
        self.sway_direction = 0.1

        self.closeness = 15 # how close something can get before it starts moving
        self.force = 3 # how fast it rotates

        self.to_render = Render(image.convert_alpha(), center, self.angle)


    def updates(self, display, location):
        leaf_image = pygame.transform.rotate(self.to_render.images, self.to_render.angle).convert_alpha()
        # leaf_image = self.to_render.images.convert_alpha()

        diff_x = location[0] - (self.to_render.loc[0] + leaf_image.get_width() // 2)
        diff_y = location[1] - leaf_image.get_height() // 2 + leaf_image.get_height() // 2 - self.to_render.loc[1]


        if self.sway_angle > 10 or self.sway_angle < -10:
            self.sway_direction *= -1


        leaf_image = pygame.transform.rotate(leaf_image, self.sway_angle)
        self.sway_angle += self.sway_direction



        if -10 < diff_y < 10:
            if 0 < diff_x < self.closeness:
                angle = self.force * (self.closeness - diff_x)
                leaf_image = pygame.transform.rotate(leaf_image, angle + self.sway_angle)

            elif -self.closeness < diff_x < 0:
                angle = -self.force * (self.closeness + diff_x)
                leaf_image = pygame.transform.rotate(leaf_image, angle + self.sway_angle)


    
        display.blit(leaf_image, (self.to_render.loc[0] - leaf_image.get_width() // 2, self.to_render.loc[1] - leaf_image.get_height() // 2))


    def render(self, surf):
        self.to_render.render_single(surf)


    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        # self.to_render.angle = self.angle
