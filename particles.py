import pygame
import random

red = [203,53,61]
yellow = [249,182,78]
orange = [237,98,64]
brown = [86,61,67]
brownish = [106,74,87]



colors_start = [red, yellow, orange]
colors_end =[brown, brownish]


class Particle:
    def __init__(self, loc, vel, size, type="explosion") -> None:
        self.loc = loc
        self.vel = vel
        self.size = size

        self.shrink_rate = 1
        self.gravity = .5


        self.time = self.size / self.shrink_rate

        if type == "explosion":
            self.start_color = colors_start[(random.randint(0, 2))].copy()
            self.end_color = colors_end[(random.randint(0, 1))].copy()
        if type == "dust":
            self.start_color = [255, 255, 255]
            self.end_color = [255, 255, 255]


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


    def dead(self):
        if self.size <= 0:
            return True
        return False

    def all(self, surface):


        self.shrink()
        self.move()
        self.color()
        self.draw(surface)
    