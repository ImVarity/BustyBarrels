import pygame
import math
from vector import Vector

heather = (210, 145, 255)
indigo = (75, 0, 130)

cos_45 = math.cos(45 * math.pi / 180)
sin_45 = math.sin(45 * math.pi / 180)


display_center_x = 200
display_center_y = 200

class Hitbox:
    def __init__(self, center, width, height, color):
        self.color = color
        self.width = width
        self.height = height
        self.center = Vector(center[0], center[1])
        
        self.vertices = [
            Vector(self.center.x - width / 2, self.center.y - height / 2),
            Vector(self.center.x + width / 2, self.center.y - height / 2),
            Vector(self.center.x + width / 2, self.center.y + height / 2),
            Vector(self.center.x - width / 2, self.center.y + height / 2)
        ]
        self.rotation_speed = 0
        self.rotationspeed_degrees = 2
        self.rotationspeed = self.rotationspeed_degrees * math.pi / 180
        self.rotation_speed = 0
        self.direction = Vector(0, 0)
        self.last_looked = Vector(0, 0)
        self.angle = 0
        self.angle_looking = 0
        self.velocity = 2 # the speed the player moves at, so basically the speed the whole game moves at

        self.dt = 1


        
    def draw_hitbox(self, screen):
        pygame.draw.line(screen, self.color, self.vertices[0].point, self.vertices[1].point, 1)
        pygame.draw.line(screen, self.color, self.vertices[1].point, self.vertices[2].point, 1)
        pygame.draw.line(screen, self.color, self.vertices[2].point, self.vertices[3].point, 1)
        pygame.draw.line(screen, self.color, self.vertices[3].point, self.vertices[0].point, 1)

    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)

    
    def get_direction(self, input):
        if not input["lock"]:
            if input["up"] and input["right"]:
                self.direction = Vector(cos_45, -sin_45)
                self.last_looked = self.direction
            elif input["up"] and input["left"]:
                self.direction = Vector(-cos_45, -sin_45)
                self.last_looked = self.direction
            elif input["down"] and input["right"]:
                self.direction = Vector(cos_45, sin_45)
                self.last_looked = self.direction
            elif input["down"] and input["left"]:
                self.direction = Vector(-cos_45, sin_45)
                self.last_looked = self.direction
            elif input["right"]:
                self.direction = Vector(1, 0)
                self.last_looked = self.direction
            elif input["left"]:
                self.direction = Vector(-1, 0)
                self.last_looked = self.direction
            elif input["up"]:
                self.direction = Vector(0, -1)
                self.last_looked = self.direction
            elif input["down"]:
                self.direction = Vector(0, 1)
                self.last_looked = self.direction
            else:
                self.direction = Vector(0, 0)
        else:
            if input["up"] and input["right"]:
                self.direction = Vector(cos_45, -sin_45)
            elif input["up"] and input["left"]:
                self.direction = Vector(-cos_45, -sin_45)
            elif input["down"] and input["right"]:
                self.direction = Vector(cos_45, sin_45)
            elif input["down"] and input["left"]:
                self.direction = Vector(-cos_45, sin_45)

            elif input["right"]:
                self.direction = Vector(1, 0)
            elif input["left"]:
                self.direction = Vector(-1, 0)
            elif input["up"]:
                self.direction = Vector(0, -1)
            elif input["down"]:
                self.direction = Vector(0, 1)
            else:
                self.direction = Vector(0, 0)

        self.angle_looking = math.atan2(self.last_looked.y, self.last_looked.x) + self.angle * math.pi / 180
        



        return self.direction

    def move(self, direction):
        self.translate(direction)

    def move_distance(self, direction, distance):
        self.center += direction * distance
        for i in range(len(self.vertices)):
            self.vertices[i] += direction * distance

    def set_delta_time(self, dt):
        self.dt = dt


    # moves everything opposite direction to simulate movement of a static player
    def handle_rotation(self, rotation_input, player=False):
        if rotation_input["reset"]:
            if self.angle != 0:
                self.reset_rotation()
                self.angle = 0
        if rotation_input["counterclockwise"] or rotation_input["clockwise"]:
            if rotation_input["counterclockwise"]:
                self.rotation_speed = -self.rotationspeed * self.dt
                self.angle += self.rotationspeed_degrees * self.dt

            elif rotation_input["clockwise"]:
                self.rotation_speed = self.rotationspeed
                self.angle -= self.rotationspeed_degrees * self.dt

            if player:
                self.self_rotation()
            else:
                self.rotation()



    def translate(self, direction):
        self.center += direction * self.velocity
        for i in range(len(self.vertices)):
            self.vertices[i] += direction * self.velocity


    def rotation(self):
        self.center.x, self.center.y = (self.center.x - display_center_x) * math.cos(self.rotation_speed * self.dt) + (self.center.y - display_center_x) * -math.sin(self.rotation_speed * self.dt) + display_center_x, (self.center.x - display_center_x) * math.sin(self.rotation_speed * self.dt) + (self.center.y - display_center_x) * math.cos(self.rotation_speed * self.dt) + display_center_x
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - display_center_x) * math.cos(self.rotation_speed * self.dt) + (self.vertices[i].y - display_center_x) * -math.sin(self.rotation_speed * self.dt) + display_center_x, (self.vertices[i].x - display_center_x) * math.sin(self.rotation_speed * self.dt) + (self.vertices[i].y - display_center_x) * math.cos(self.rotation_speed * self.dt) + display_center_x

    def self_rotation(self):
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - self.center.x) * math.cos(self.rotation_speed * self.dt) + (self.vertices[i].y - self.center.y) * -math.sin(self.rotation_speed * self.dt) + self.center.x, (self.vertices[i].x - self.center.x) * math.sin(self.rotation_speed * self.dt) + (self.vertices[i].y - self.center.y) * math.cos(self.rotation_speed * self.dt) + self.center.y

    def reset_rotation(self):
        back = self.angle * math.pi / 180
        self.center.x, self.center.y = (self.center.x - display_center_x) * math.cos(back) + (self.center.y - display_center_x) * -math.sin(back) + display_center_x, (self.center.x - display_center_x) * math.sin(back) + (self.center.y - display_center_x) * math.cos(back) + display_center_x
        for i in range(len(self.vertices)):
            self.vertices[i].x, self.vertices[i].y = (self.vertices[i].x - display_center_x) * math.cos(back) + (self.vertices[i].y - display_center_x) * -math.sin(back) + display_center_x, (self.vertices[i].x - display_center_x) * math.sin(back) + (self.vertices[i].y - display_center_x) * math.cos(back) + display_center_x
        


    def normals(self):
        edgeVectors = []
        normalVectors = []

        for i in range(4):
            if (i == 3):
                v = self.vertices[0]
                z = self.vertices[3]
                q = v - z # gets edge
                edgeVectors.append(q)
                break

            v = self.vertices[i + 1]
            z = self.vertices[i]
            q = v - z # gets edge

            edgeVectors.append(q)



        # returns normal vectors that are normalized
        for edge in edgeVectors:
            v = Vector(-edge.y, edge.x)
            v = v.normalize()
            normalVectors.append(v)

        return normalVectors

    # SAT collision
    def handle_collision(self, normals, normalstwo, boxtwo):

        normal = normals[0]
        depth = float('inf')


        for i in range(len(self.vertices)):

            # projecting self vertices onto self normals
            minA, maxA = self.project_vertices(self.vertices, normals[i])
            # projecting another box vertices onto self normals
            minB, maxB = self.project_vertices(boxtwo.vertices, normals[i])

            # checking overlap
            if (minA >= maxB or minB >= maxA):
                return False, depth, normal
            
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
                return False, depth, normal
            
            axisDepth = min(maxB - minA, maxA - minB)

            if axisDepth < depth:
                depth = axisDepth
                normal = normalstwo[i]


        centerA = self.center
        centerB = boxtwo.center

        direction = centerA - centerB
        
        if direction.dotproduct(normal) < 0:
            normal = normal * -1
        
        return (True, depth, normal)


    def project_vertices(self, vertices, axis):
        edgeProjection = [float('inf'), float('-inf')]
        for j in range(len(vertices)):
            projection = axis.dotproduct(vertices[j])
            edgeProjection[0] = min(projection, edgeProjection[0])
            edgeProjection[1] = max(projection, edgeProjection[1])
        return edgeProjection

    def intervals_overlap(self, interval1, interval2):
        a1, b1 = interval1
        a2, b2 = interval2

        return not (b1 < a2 or b2 < a1)
    


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


    def get_angle(self):
        return self.angle

