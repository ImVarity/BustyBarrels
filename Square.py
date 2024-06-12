import pygame
import math
from vector import Vector

heather = (210, 145, 255)
indigo = (75, 0, 130)

cos_45 = math.cos(45 * math.pi / 180)
sin_45 = math.sin(45 * math.pi / 180)

class Square:
    def __init__(self, center, width, height, color):
        self.color = color
        self.width = width
        self.height = height
        self.center = Vector((center[0], center[1]))
        
        self.vertices = [Vector((self.center.x - width / 2, self.center.y - height / 2), origin=[self.center.x, self.center.y]),
                         Vector((self.center.x + width / 2, self.center.y - height / 2), origin=[self.center.x, self.center.y]),
                         Vector((self.center.x + width / 2, self.center.y + height / 2), origin=[self.center.x, self.center.y]),
                         Vector((self.center.x - width / 2, self.center.y + height / 2), origin=[self.center.x, self.center.y])]
        
    


        self.angle = 0
        self.rotationspeed = 0.05
        self.velocity = 5
        
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.vertices[0].tail, self.vertices[1].tail, 4)
        pygame.draw.line(screen, self.color, self.vertices[1].tail, self.vertices[2].tail, 4)
        pygame.draw.line(screen, self.color, self.vertices[2].tail, self.vertices[3].tail, 4)
        pygame.draw.line(screen, self.color, self.vertices[3].tail, self.vertices[0].tail, 4)

    
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


    

    def move(self, input):


        # input = self.check_collision(input)

        if input["up"] and input["right"]:
            self.translate(Vector((cos_45, -sin_45)))
        elif input["up"] and input["left"]:
            self.translate(Vector((-cos_45, -sin_45)))
        elif input["down"] and input["right"]:
            self.translate(Vector((cos_45, sin_45)))
        elif input["down"] and input["left"]:
            self.translate(Vector((-cos_45, sin_45)))

        elif input["right"]:
            self.translate(Vector((1, 0)))
        elif input["left"]:
            self.translate(Vector((-1, 0)))
        elif input["up"]:
            self.translate(Vector((0, -1)))
        elif input["down"]:
            self.translate(Vector((0, 1)))

        if input["counterclockwise"] or input["clockwise"]:
            if input["counterclockwise"]:
                self.angle = self.rotationspeed
            if input["clockwise"]:
                self.angle = -self.rotationspeed
            self.rotation()
        
        


    def translate(self, direction):
        self.center += direction * self.velocity
        for i in range(len(self.vertices)):
            self.vertices[i] += direction * self.velocity

    def rotation(self):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.angle) + (self.vertices[i].y - self.center.y) * -math.sin(self.angle) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.angle) + (self.vertices[i].y - self.center.y) * math.cos(self.angle) + self.center.y

            

    def draw_projection(self, screen, normals):
        push_out_0 = Vector((-normals[0].y, normals[0].x))
        push_out_1 = Vector((-normals[1].y, normals[1].x))
        push_out_2 = Vector((-normals[2].y, normals[2].x))
        push_out_3 = Vector((-normals[3].y, normals[3].x))
        
        pygame.draw.line(screen, heather, (self.center + (push_out_0 * 250)).tail, (self.center + (push_out_0 * 250) + normals[0] * 500).tail)
        pygame.draw.line(screen, heather, (self.center + (push_out_0 * 250)).tail, (self.center + (push_out_0 * 250) + normals[0] * -500).tail)

        pygame.draw.line(screen, heather, (self.center + (push_out_1 * 250)).tail, (self.center + (push_out_1 * 250) + normals[1] * 500).tail)
        pygame.draw.line(screen, heather, (self.center + (push_out_1 * 250)).tail, (self.center + (push_out_1 * 250) + normals[1] * -500).tail)

        pygame.draw.line(screen, heather, (self.center + (push_out_2 * 250)).tail, (self.center + (push_out_2 * 250) + normals[2] * 500).tail)
        pygame.draw.line(screen, heather, (self.center + (push_out_2 * 250)).tail, (self.center + (push_out_2 * 250) + normals[2] * -500).tail)

        pygame.draw.line(screen, heather, (self.center + (push_out_3 * 250)).tail, (self.center + (push_out_3 * 250) + normals[3] * 500).tail)
        pygame.draw.line(screen, heather, (self.center + (push_out_3 * 250)).tail, (self.center + (push_out_3 * 250) + normals[3] * -500).tail)



    def draw_projection_intervals(self, screen, normal, length):


        push_out_0 = Vector((-normal.y, normal.x))
        
        pygame.draw.line(screen, self.color, (self.center + (push_out_0 * 230)).tail, (self.center + (push_out_0 * 230) + normal * (length / 2)).tail)
        pygame.draw.line(screen, self.color, (self.center + (push_out_0 * 230)).tail, (self.center + (push_out_0 * 230) + normal * (-length / 2)).tail)


    def handle_collision(self, normals, normalstwo, boxtwo, screen):
        projections = []
        projectionstwo = []


        for i in range(len(self.vertices)):
            edgeProjection = [float('inf'), float('-inf')]
            for j in range(len(normals)):
                n = normals[i].normalize()
                projection = n.dotproduct(self.vertices[j])
                edgeProjection[0] = min(projection, edgeProjection[0])
                edgeProjection[1] = max(projection, edgeProjection[1])
            projections.append(edgeProjection)

        for i in range(len(self.vertices)):
            edgeProjection = [float('inf'), float('-inf')]
            for j in range(len(normalstwo)):
                n = normalstwo[i].normalize()
                projection = n.dotproduct(self.vertices[j])
                edgeProjection[0] = min(projection, edgeProjection[0])
                edgeProjection[1] = max(projection, edgeProjection[1])
            projections.append(edgeProjection)


        for i in range(len(boxtwo.vertices)):
            edgeProjection = [float('inf'), float('-inf')]
            for j in range(len(normals)):
                n = normals[i].normalize()
                projection = n.dotproduct(boxtwo.vertices[j])
                edgeProjection[0] = min(projection, edgeProjection[0])
                edgeProjection[1] = max(projection, edgeProjection[1])
            projectionstwo.append(edgeProjection)

        for i in range(len(boxtwo.vertices)):
            edgeProjection = [float('inf'), float('-inf')]
            for j in range(len(normalstwo)):
                n = normalstwo[i].normalize()
                projection = n.dotproduct(boxtwo.vertices[j])
                edgeProjection[0] = min(projection, edgeProjection[0])
                edgeProjection[1] = max(projection, edgeProjection[1])
            projectionstwo.append(edgeProjection)




        # print("projections", projections)
        # print("projectionstwo", projectionstwo)

        collision = False
        hits = 0
        hitpoints = []

        # print(projections)

        for i in range(len(projections)):
            self.draw_projection_intervals(screen, normals[1], abs(projections[1][0] - projections[1][1]))
            self.draw_projection_intervals(screen, normals[1], abs(projectionstwo[1][0] - projectionstwo[1][1]))
            
            if self.intervals_overlap(projections[i], projectionstwo[i]):
                hits += 1
                hitpoints.append((projections[i], projectionstwo[i]))
            else:
                hits -= 1


        # intervals are overlapping in all 8 normals
        if hits == 8:
            collision = True
            print("collided")
        else:
            print("not")

    def intervals_overlap(self, interval1, interval2):
        a1, b1 = interval1
        a2, b2 = interval2


        return not (b1 < a2 or b2 < a1)
    
    def draw_intervals(self, interval, screen):
        pass



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




