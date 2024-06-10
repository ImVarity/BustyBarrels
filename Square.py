import pygame
import math
from vector import Vector


cos_45 = math.cos(45 * math.pi / 180)
sin_45 = math.sin(45 * math.pi / 180)

class Square:
    def __init__(self, center, width, height):
        self.width = width
        self.height = height
        self.center = Vector((center[0], center[1]))
        
        self.vertices = [Vector((self.center.x - width / 2, self.center.y - height / 2), position=[self.center.x, self.center.y]),
                         Vector((self.center.x + width / 2, self.center.y - height / 2), position=[self.center.x, self.center.y]),
                         Vector((self.center.x + width / 2, self.center.y + height / 2), position=[self.center.x, self.center.y]),
                         Vector((self.center.x - width / 2, self.center.y + height / 2), position=[self.center.x, self.center.y])]
        
    


        self.angle = 0
        self.rotationspeed = 0.05
        self.velocity = 5
        
    def draw(self, screen):
        pygame.draw.line(screen, (255,69,0), self.vertices[0].tail, self.vertices[1].tail)
        pygame.draw.line(screen, (255,69,0), self.vertices[1].tail, self.vertices[2].tail)
        pygame.draw.line(screen, (255,69,0), self.vertices[2].tail, self.vertices[3].tail)
        pygame.draw.line(screen, (255,69,0), self.vertices[3].tail, self.vertices[0].tail)

    
    def normals(self):
        edgeVectors = []
        normalVectors = []

        for i in range(4):
            if (i == 3):
                v = self.vertices[0]
                z = self.vertices[3]
                q = v - z
                edgeVectors.append(q)
                break
            v = self.vertices[i + 1]
            z = self.vertices[i]
            q = v - z

            edgeVectors.append(q)

        for edge in edgeVectors:
            v = Vector((-edge.y, edge.x))
            v = v.normalize()
            normalVectors.append(v)

        



        return normalVectors


    def transform(self):
        for i in range(len(self.vertices)):
            
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.angle) + (self.vertices[i].y - self.center.y) * -math.sin(self.angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.angle) + (self.vertices[i].y - self.center.y) * math.cos(self.angle) + self.center.y


    def move(self, input):


        # input = self.check_collision(input)

        if input["up"] and input["right"]:
            self.center = self.center + Vector((cos_45, -sin_45)) * self.velocity
        elif input["up"] and input["left"]:
            self.center += Vector((-cos_45, -sin_45)) * self.velocity
        elif input["down"] and input["right"]:
            self.center += Vector((cos_45, sin_45)) * self.velocity
        elif input["down"] and input["left"]:
            self.center += Vector((-cos_45, sin_45)) * self.velocity

        elif input["right"]:
            self.center += Vector((self.velocity, 0))
        elif input["left"]:
            self.center -= Vector((self.velocity, 0))
        elif input["up"]:
            self.center -= Vector((0, self.velocity))
        elif input["down"]:
            self.center += Vector((0, self.velocity))


        if input["counterclockwise"]:
            self.angle += self.rotationspeed
        if input["clockwise"]:
            self.angle -= self.rotationspeed
        

        self.vertices = [Vector((self.center.x - self.width / 2, self.center.y - self.height / 2), position=[self.center.x, self.center.y]),
                         Vector((self.center.x + self.width / 2, self.center.y - self.height / 2), position=[self.center.x, self.center.y]),
                         Vector((self.center.x + self.width / 2, self.center.y + self.height / 2), position=[self.center.x, self.center.y]),
                         Vector((self.center.x - self.width / 2, self.center.y + self.height / 2), position=[self.center.x, self.center.y])]
        

        self.transform()

    # def check_collision(self, input, b1, b2):   
    #     pass
    #     v1 = b1.vertices
    #     v2 = b2.vertices


    #     projections = []
    #     projectionstwo = []


    #     for i in range(len(v1)):
    #         edgeProjection = [999999, -999999]
    #         for j in range(len(normals)):
    #             projection = dotproduct(v1[j], normalize([0, 0], normals[i]))
    #             edgeProjection[0] = min(projection, edgeProjection[0])
    #             edgeProjection[1] = max(projection, edgeProjection[1])
    #         projections.append(edgeProjection)

    #     for i in range(len(v1)):
    #         edgeProjection = [999999, -999999]
    #         for j in range(len(normalstwo)):
    #             projection = dotproduct(v1[j], normalize([0, 0], normalstwo[i]))
    #             edgeProjection[0] = min(projection, edgeProjection[0])
    #             edgeProjection[1] = max(projection, edgeProjection[1])
    #         projections.append(edgeProjection)


    #     for i in range(len(v2)):
    #         edgeProjection = [999999, -999999]
    #         for j in range(len(normals)):
    #             projection = dotproduct(v2[j], normalize([0, 0], normals[i]))
    #             edgeProjection[0] = min(projection, edgeProjection[0])
    #             edgeProjection[1] = max(projection, edgeProjection[1])
    #         projectionstwo.append(edgeProjection)

    #     for i in range(len(v2)):
    #         edgeProjection = [999999, -999999]
    #         for j in range(len(normalstwo)):
    #             projection = dotproduct(v2[j], normalize([0, 0], normalstwo[i]))
    #             edgeProjection[0] = min(projection, edgeProjection[0])
    #             edgeProjection[1] = max(projection, edgeProjection[1])
    #         projectionstwo.append(edgeProjection)





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




