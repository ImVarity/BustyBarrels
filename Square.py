import pygame
import math
from vector import Vector

heather = (210, 145, 255)
indigo = (75, 0, 130)

cos_45 = math.cos(45 * math.pi / 180)
sin_45 = math.sin(45 * math.pi / 180)


display_center_x = 200
display_center_y = 200

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

        self.rotation_speed = 0
        self.rotationspeed_degress = 2
        self.rotationspeed = self.rotationspeed_degress * math.pi / 180
        self.rotation_speed = 0
        self.velocity = 2
        self.direction = Vector((0, 0))
        self.angle = 0

        self.distance_from_center = math.sqrt((display_center_x - self.center.x) ** 2 + (display_center_x - self.center.y) ** 2)


        
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.vertices[0].tail, self.vertices[1].tail, 1)
        pygame.draw.line(screen, self.color, self.vertices[1].tail, self.vertices[2].tail, 1)
        pygame.draw.line(screen, self.color, self.vertices[2].tail, self.vertices[3].tail, 1)
        pygame.draw.line(screen, self.color, self.vertices[3].tail, self.vertices[0].tail, 1)

    
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
    
    def get_direction(self, input):

        direction = Vector((0, 0))

        if input["up"] and input["right"]:
            direction = (Vector((cos_45, -sin_45)))
        elif input["up"] and input["left"]:
            direction = (Vector((-cos_45, -sin_45)))
        elif input["down"] and input["right"]:
            direction = (Vector((cos_45, sin_45)))
        elif input["down"] and input["left"]:
            direction = (Vector((-cos_45, sin_45)))

        elif input["right"]:
            direction = (Vector((1, 0)))
        elif input["left"]:
            direction = (Vector((-1, 0)))
        elif input["up"]:
            direction = (Vector((0, -1)))
        elif input["down"]:
            direction = (Vector((0, 1)))


        return direction
        

    def move(self, direction):
        self.translate(direction)




    def handle_rotation(self, rotation_input, player=False):
        if rotation_input["reset"]:
            self.angle = 0
        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.rotation_speed = self.rotationspeed
                self.angle -= self.rotationspeed_degress
            elif rotation_input["clockwise"]:
                self.rotation_speed = -self.rotationspeed
                self.angle += self.rotationspeed_degress
            if player:
                self.self_rotation()
            else:
                self.rotation()

    


    def translate(self, direction):
        self.center += direction * self.velocity
        self.distance_from_center = math.sqrt((display_center_x - self.center.x) ** 2 + (display_center_x - self.center.y) ** 2)
        for i in range(len(self.vertices)):
            self.vertices[i] += direction * self.velocity

    def rotation(self):
        self.center.x, self.center.y = (self.center.x - display_center_x) * math.cos(self.rotation_speed) + (self.center.y - display_center_x) * -math.sin(self.rotation_speed) + display_center_x, (self.center.x - display_center_x) * math.sin(self.rotation_speed) + (self.center.y - display_center_x) * math.cos(self.rotation_speed) + display_center_x
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - display_center_x) * math.cos(self.rotation_speed) + (self.vertices[i].y - display_center_x) * -math.sin(self.rotation_speed) + display_center_x, (self.vertices[i].x - display_center_x) * math.sin(self.rotation_speed) + (self.vertices[i].y - display_center_x) * math.cos(self.rotation_speed) + display_center_x

    def self_rotation(self):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.rotation_speed) + (self.vertices[i].y - self.center.y) * -math.sin(self.rotation_speed) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.rotation_speed) + (self.vertices[i].y - self.center.y) * math.cos(self.rotation_speed) + self.center.y



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


    # SAT collision
    def handle_collision(self, normals, normalstwo, boxtwo):

        normal = normals[0]
        depth = float('inf')
        collided = True

        for i in range(len(self.vertices)):

            # projecting self vertices onto self normals
            minA, maxA = self.project_vertices(self.vertices, normals[i])
            # projecting another box vertices onto self normals
            minB, maxB = self.project_vertices(boxtwo.vertices, normals[i])

            # checking overlap
            if (minA >= maxB or minB >= maxA):
                collided = False
            
            axisDepth = min(maxB - minA, maxA - minB)

            if axisDepth < depth:
                depth = axisDepth
                normal = normals[i]

                
        for i in range(len(boxtwo.vertices)):

            # projecting self vertices onto another box normals
            minA, maxA = self.project_vertices(self.vertices, normalstwo[i])
            # projecting another box vertices onto another box normals
            minB, maxB = self.project_vertices(boxtwo.vertices, normalstwo[i])

            # checking overlap
            if (minA >= maxB or minB >= maxA):
                collided = False
            
            axisDepth = min(maxB - minA, maxA - minB)

            if axisDepth < depth:
                depth = axisDepth
                normal = normalstwo[i]

        
        # centerA = self.find_arithmetic_mean(self.vertices)
        # centerB = self.find_arithmetic_mean(boxtwo.vertices)

        centerA = self.center
        centerB = boxtwo.center

        direction = centerA - centerB
        
        if direction.dotproduct(normal) < 0:
            normal = normal * -1
        
        return (collided, depth, normal)


    def project_vertices(self, vertices, axis):
        edgeProjection = [float('inf'), float('-inf')]
        for j in range(len(vertices)):
            projection = axis.dotproduct(vertices[j])
            edgeProjection[0] = min(projection, edgeProjection[0])
            edgeProjection[1] = max(projection, edgeProjection[1])
        return edgeProjection


    def find_arithmetic_mean(self, vertices):
        sumX = 0
        sumY = 0

        for i in range(len(vertices)):
            sumX += vertices[i].x + vertices[i].origin[0]
            sumY += vertices[i].y + vertices[i].origin[1]

        return Vector((sumX / len(vertices), sumY / len(vertices)))


    def intervals_overlap(self, interval1, interval2):
        a1, b1 = interval1
        a2, b2 = interval2

        return not (b1 < a2 or b2 < a1)
    
    def draw_intervals(self, interval, screen):
        pass



    def rotate(self):
        self.rotation_speed = self.rotationspeed


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




