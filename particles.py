import pygame
import random


red = [203,53,61]
yellow = [249,182,78]
orange = [237,98,64]
brown = [86,61,67]
brownish = [106,74,87]

b_p = [191, 64, 191]
iris = [93, 63, 211]
l_p = [207, 159, 255]
blue = [65,105,225]

# colors_start = [b_p, iris, l_p, blue] # not bad
colors_start_red = [red, yellow, orange]
colors_end =[brown, brownish]
colors_start_purple = [b_p, iris, l_p, blue]


def square_surf(width, height, color):
    # Create a surface with an alpha channel (transparency)
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Draw the rectangle on the surface
    pygame.draw.rect(surf, color, pygame.Rect(0, 0, width, height))
    return surf

class Particle:
    def __init__(self, loc, vel, size, type="explosion", lighting=False) -> None:
        self.loc = loc
        self.vel = vel
        self.size = size

        self.shrink_rate = 1
        self.gravity = .5

        self.lighting = lighting

        self.time = self.size / self.shrink_rate

        if type == "explosion":
            self.start_color = colors_start_red[(random.randint(0, len(colors_start_red) - 1))].copy()
            self.end_color = colors_end[(random.randint(0, len(colors_end) - 1))].copy()
        if type == "dust":
            self.start_color = [255, 255, 255]
            self.end_color = [255, 255, 255]
        if type == "celebrate":
            self.start_color = colors_start_purple[(random.randint(0, len(colors_start_purple) - 1))].copy()
            self.end_color = colors_end[(random.randint(0, len(colors_end) - 1))].copy()



        self.r = (self.start_color[0] - self.end_color[0]) / self.time
        self.g = (self.start_color[1] - self.end_color[1]) / self.time
        self.b = (self.start_color[2] - self.end_color[2]) / self.time
        

        self.start_change = False
        self.counter = 0

    def shrink(self):
        self.size -= self.shrink_rate
        self.loc[0] += self.shrink_rate / 2
        self.loc[1] += self.shrink_rate / 2
    
    def move(self):
        self.loc[0] += self.vel[0]
        self.loc[1] += self.vel[1]

        self.vel[1] += self.gravity

    def color(self):
        self.counter += 1
        if self.counter == self.time * self.shrink_rate / 2:
            self.start_change = True
        if self.start_change:
            self.start_color[0] -= self.r
            self.start_color[1] -= self.g
            self.start_color[2] -= self.b

            if self.start_color[0] > 255:
                self.start_color[0] = 255
            if self.start_color[1] > 255:
                self.start_color[1] = 255
            if self.start_color[2] > 255:
                self.start_color[2] = 255

            if self.start_color[0] < 0:
                self.start_color[0] = 0
            if self.start_color[1] < 0:
                self.start_color[1] = 0
            if self.start_color[2] < 0:
                self.start_color[2] = 0


    def draw(self, surface):
        color = (int(self.start_color[0]), int(self.start_color[1]), int(self.start_color[2]))
        pygame.draw.rect(surface, color, pygame.Rect(self.loc[0], self.loc[1], self.size, self.size))
        if self.lighting:
            surface.blit(square_surf(self.size * 2, self.size * 2, (20, 20, 20)), (self.loc[0] - self.size / 2, self.loc[1] - self.size / 2), special_flags=pygame.BLEND_RGB_ADD)


    def dead(self):
        if self.size <= 0:
            return True
        return False

    def all(self, surface):


        self.shrink()
        self.move()
        self.color()
        self.draw(surface)
    



def dust(particles, loc, direction):

    # v_x = random.randint(-200, 400) / 500 * direction.x * -2 * 2
    # v_y = random.randint(0, 400) / 500 * direction.y * -1 * 2

    for i in range(2):
        v_x = random.randint(-100, 400) / 500 * direction.x * -2 * 2
        v_y = random.randint(0, 400) / 500 * direction.y * -1 * 2
        p = Particle([loc[0], loc[1] + 4], [v_x, v_y], random.randint(3, 5), "dust")
        p.gravity = -.02
        p.shrink_rate = .08
        particles.append(p)