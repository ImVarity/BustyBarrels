import math
import pygame
from vector import Vector

class Circle:
    def __init__(self, center, radius, color):
        self.radius = radius
        self.center = center
        self.color = color
        self.vector = Vector((self.radius, 0), origin=center)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)


    def handle_collision(self, normals, box, screen):

        vertices = box.vertices

        circle_vertices = []

        for i in range(len(normals)):
            circle_vertices.append(normals[i] * self.radius + Vector((self.center)))


        circle_normals = self.normals(circle_vertices)


        pygame.draw.line(screen, (255, 255, 255), (circle_vertices[0] + Vector(self.center)).tail, (circle_vertices[1] + Vector(self.center)).tail)
        pygame.draw.line(screen, (255, 255, 255), (circle_vertices[1] + Vector(self.center)).tail, (circle_vertices[2] + Vector(self.center)).tail)
        pygame.draw.line(screen, (255, 255, 255), (circle_vertices[2] + Vector(self.center)).tail, (circle_vertices[3] + Vector(self.center)).tail)
        pygame.draw.line(screen, (255, 255, 255), (circle_vertices[3] + Vector(self.center)).tail, (circle_vertices[0] + Vector(self.center)).tail)

        projections = []
        projectionstwo = []

        # projecting self vertices onto self normals
        for i in range(len(vertices)):
            edgeProjection = [float('inf'), float('-inf')]
            for j in range(len(normals)):
                n = normals[i]
                projection = n.dotproduct(vertices[j])
                edgeProjection[0] = min(projection, edgeProjection[0])
                edgeProjection[1] = max(projection, edgeProjection[1])
            projections.append(edgeProjection)

        # # projecting self vertices onto another box normals
        # for i in range(len(vertices)):
        #     edgeProjection = [float('inf'), float('-inf')]
        #     for j in range(len(circle_normals)):
        #         n = circle_normals[i]
        #         projection = n.dotproduct(vertices[j])
        #         edgeProjection[0] = min(projection, edgeProjection[0])
        #         edgeProjection[1] = max(projection, edgeProjection[1])
        #     projections.append(edgeProjection)

        # projecting another box vertices onto self normals
        for i in range(len(circle_vertices)):
            edgeProjection = [float('inf'), float('-inf')]
            for j in range(len(normals)):
                n = normals[i]
                projection = n.dotproduct(circle_vertices[j])
                edgeProjection[0] = min(projection, edgeProjection[0])
                edgeProjection[1] = max(projection, edgeProjection[1])
            projectionstwo.append(edgeProjection)

        # # projecting another box vertices onto another box normals
        # for i in range(len(circle_vertices)):
        #     edgeProjection = [float('inf'), float('-inf')]
        #     for j in range(len(circle_normals)):
        #         n = circle_normals[i]
        #         projection = n.dotproduct(circle_vertices[j])
        #         edgeProjection[0] = min(projection, edgeProjection[0])
        #         edgeProjection[1] = max(projection, edgeProjection[1])
        #     projectionstwo.append(edgeProjection)

        # print("projections", projections)
        # print("projectionstwo", projectionstwo)

        collision = False
        hits = 0
        hitpoints = []

        # print()
        # print(projections)
        # print(projectionstwo)
        # print()

        for i in range(len(projections)):
            # if i < 4:
            #     self.draw_projection_intervals(screen, normals[i], abs(projections[i][0] - projections[i][1]))
            if self.intervals_overlap(projections[i], projectionstwo[i]):
                hits += 1
                hitpoints.append((projections[i], projectionstwo[i]))
            else:
                hits -= 1



        print("hits", hits)

        # intervals are overlapping in all 8 normals
        if hits == 4:
            collision = True
            print("collided")
        else:
            print("not")

    def intervals_overlap(self, interval1, interval2):
        a1, b1 = interval1
        a2, b2 = interval2


        return not (b1 < a2 or b2 < a1)
    


    def normals(self, vertices):
        edgeVectors = []
        normalVectors = []

        for i in range(4):
            if (i == 3):
                v = vertices[0]
                z = vertices[3]
                q = v - z
                edgeVectors.append(q)
                break

            v = vertices[i + 1]
            z = vertices[i]
            q = v - z

            edgeVectors.append(q)

        for edge in edgeVectors:
            v = Vector((-edge.y, edge.x))
            v = v.normalize()
            normalVectors.append(v)


        return normalVectors