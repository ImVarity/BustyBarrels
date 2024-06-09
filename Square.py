import pygame
import math
from vector import Vector

class Square:
    def __init__(self, center, width, height):
        self.center = center
        self.width = width
        self.height = height
        self.vertices = [[self.center[0] - width / 2, self.center[1] - height / 2],
                         [self.center[0] + width / 2, self.center[1] - height / 2],
                         [self.center[0] + width / 2, self.center[1] + height / 2],
                         [self.center[0] - width / 2, self.center[1] + height / 2]]
        self.angle = 0
        self.rotationspeed = 0.009
        
    def draw(self, screen):
        pygame.draw.line(screen, (25, 53, 75), self.vertices[0], self.vertices[1])
        pygame.draw.line(screen, (25, 53, 75), self.vertices[1], self.vertices[2])
        pygame.draw.line(screen, (25, 53, 75), self.vertices[2], self.vertices[3])
        pygame.draw.line(screen, (25, 53, 75), self.vertices[3], self.vertices[0])


    
    def normals(self):
        edgeVectors = []
        normalVectors = []

        for i in range(4):
            if (i == 3):
                edgeVectors.append([self.vertices[0][0] - self.vertices[3][0], self.vertices[0][1] - self.vertices[3][1]])
                break
            edgeVectors.append([self.vertices[i + 1][0] - self.vertices[i][0], self.vertices[i + 1][1] - self.vertices[i][1]])

        for edge in edgeVectors:
            normalVectors.append(self.normalize([0, 0], [-edge[1], edge[0]]))

        return normalVectors
    
    def testnormals(self):
        edgeVectors = []
        normalVectors = []

        for i in range(4):
            if (i == 3):
                edgeVectors.append([self.vertices[0][0] - self.vertices[3][0], self.vertices[0][1] - self.vertices[3][1]])
                break
            edgeVectors.append([self.vertices[i + 1][0] - self.vertices[i][0], self.vertices[i + 1][1] - self.vertices[i][1]])

        for edge in edgeVectors:
            v = Vector((-edge[1], edge[0]))
            v = v.normalize()
            normalVectors.append(v)

        return normalVectors


    def transform(self):
        for i in range(len(self.vertices)):
            self.vertices[i] = [(self.vertices[i][0] - self.center[0]) * math.cos(self.angle) + (self.vertices[i][1] - self.center[1]) * -math.sin(self.angle) + self.center[0], 
            (self.vertices[i][0] - self.center[0]) * math.sin(self.angle) + (self.vertices[i][1] - self.center[1]) * math.cos(self.angle) + self.center[1]]

    def move(self, input):
        if input["right"]:
            self.center[0] += 1
        if input["left"]:
            self.center[0] -= 1
        if input["up"]:
            self.center[1] -= 1
        if input["down"]:
            self.center[1] += 1


        if input["counterclockwise"]:
            self.angle += self.rotationspeed
        if input["clockwise"]:
            self.angle -= self.rotationspeed

        self.vertices = [[self.center[0] - self.width / 2, self.center[1] - self.height / 2],
                    [self.center[0] + self.width / 2, self.center[1] - self.height / 2],
                    [self.center[0] + self.width / 2, self.center[1] + self.height / 2],
                    [self.center[0] - self.width / 2, self.center[1] + self.height / 2]]

        self.transform()


    def rotate(self):
        self.angle = self.rotationspeed


    def normalize(self, p1, p2):
        # Calculate the vector components from p1 to p2
        vx = p2[0] - p1[0]
        vy = p2[1] - p1[1]
        
        # Calculate the magnitude of the vector
        magnitude = math.sqrt(vx ** 2 + vy ** 2)
        
        # Normalize the vector components
        if magnitude == 0:
            return [0, 0]  # To handle the case where p1 and p2 are the same point
        else:
            return [vx / magnitude, vy / magnitude]




