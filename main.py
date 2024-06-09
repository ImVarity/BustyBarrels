import pygame
import sys
from Square import Square
import math
from vector import Vector

screen_width = 800
screen_height = 800

heather = (210, 145, 255)
indigo = (75, 0, 130)
origin = [screen_width / 2, screen_height / 2]

# -3 * [0, 1] + 2 * [-1, 0]
# [0, -3] + [-2, 0]

def transform(a, b, origin):
    return [(a[0] - origin[0]) * b[0][0] + (a[1] - origin[1]) * b[1][0] + origin[0], 
            (a[0] - origin[0]) * b[0][1] + (a[1] - origin[1]) * b[1][1] + origin[1]]




def add3dvector(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def Variablex3DVector(a, b):
    return [a * b[0], a * b[1], a * b[2]]

def multiply3Dmatrix(input, transform):
    a = Variablex3DVector(input[0], transform[0])
    b = Variablex3DVector(input[1], transform[1])
    c = Variablex3DVector(input[2], transform[2])

    return add3dvector(add3dvector(a, b), c)




def normalize(p1, p2):
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




def multiplyVector(magnitude, p1):
    return [magnitude * p1[0], magnitude * p1[1]]




def dotproduct(a, b):
    return a[0] * b[0] + a[1] * b[1]


def intervals_overlap(interval1, interval2):
    a1, b1 = interval1
    a2, b2 = interval2
    # if not (b1 < a2 or b2 < a1):
    #     print(interval1, interval2)

    return not (b1 < a2 or b2 < a1)


def project_onto_normal(vertices, normal):
    for i in range(len(vertices)):
        edgeProjection = [999999, -999999]
        for j in range(len(normal)):
            projection = dotproduct(box.vertices[j], normalize([0, 0], normal[i]))
            edgeProjection[0] = min(projection, edgeProjection[0])
            edgeProjection[1] = max(projection, edgeProjection[1])
        projections.append(edgeProjection)


rotation = .01




# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Collision')

white = (255, 255, 255)

# squareOne = Square(x=150, y=200, width=100, height=100)
# squareTwo = Square(x=300, y=200, width=100, height=100)

# Initialize the surface for squareOne
# one_surface = pygame.Surface((squareOne.width, squareOne.height), pygame.SRCALPHA)  # Use SRCALPHA for transparency
# one_surface.fill((55, 55, 55))


mousePos = pygame.mouse.get_pos()

keys_held = set()


origin = [300, 200]




# | 0  -1 | 
# | 1   0 |

ccMatrix = ((0, 1), (-1, 0))


# | 0  -1 | 
# | 1   0 |

cMatrix = ((0, -1), (0, 1))


# DefaultMatrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

TDMatrix = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]
FDMatrix = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]

box_origin = [300, 300, 300]


btl = [-1, -1, 1] # -> [-1, -1, -1] -> [1, -1, -1] -> [1, -1, 1]
btr = [1, -1, 1]  # -> [-1, -1, 1] -> [-1, -1, -1] -> [1, -1, -1]
bbl = [-1, 1, 1]  # -> [-1, 1, -1] -> [1, 1, -1]   -> [1, 1, 1]
bbr = [1, 1, 1]   # -> [-1, 1, 1]  -> [-1, 1, -1]  -> [1, 1, -1]

ftl = [-1, -1, -1] # -> [-1, 1, -1]
ftr = [1, -1, -1]
fbl = [-1, 1, -1]
fbr = [1, 1, -1]



input = {
    "right": False,
    "left" : False,
    "down" : False,
    "up": False,
    "clockwise" : False,
    "counterclockwise": False,
    "reset": False
}



box = Square([400, 400], 100, 100)
normals = box.normals()

boxtwo = Square([250, 350], 100, 100)
normalstwo = boxtwo.normals()

testnormals = box.testnormals()


# Main loop
running = True
while running:
    
    keys = pygame.key.get_pressed()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                pass

            

    if (keys[pygame.K_e]):
        input["counterclockwise"] = True
    else:
        input["counterclockwise"] = False
    if (keys[pygame.K_q]):
        input["clockwise"] = True
    else:
        input["clockwise"] = False

    if (keys[pygame.K_d]):
        input["right"] = True
    else:
        input["right"] = False
    if (keys[pygame.K_a]):
        input["left"] = True
    else:
        input["left"] = False
    if (keys[pygame.K_w]):
        input["up"] = True
    else:
        input["up"] = False
    if (keys[pygame.K_s]):
        input["down"] = True
    else:
        input["down"] = False

    if (keys[pygame.K_z]):
        input["reset"] = True
    

    if (keys[pygame.K_y]):
        pass





    mousePos = pygame.mouse.get_pos()

    screen.fill(white)


    box.rotate()
    box.transform()
    normals = box.normals()
    testnormals = box.testnormals()
    box.draw(screen)

    
    # box.rotate
    normalstwo = boxtwo.normals()
    boxtwo.draw(screen)

    boxtwo.move(input)

    one = normalize([400, 400], box.vertices[0])
    two = normalize([400, 400], box.vertices[1])
    three = normalize([400, 400], box.vertices[2])
    four = normalize([400, 400], box.vertices[3])

    vOne = Vector((box.vertices[0][0] - 400, box.vertices[0][1] - 400), position=[400, 400])
    vTwo = Vector((box.vertices[1][0] - 400, box.vertices[1][1] - 400), position=[400, 400])
    vThree = Vector((box.vertices[2][0] - 400, box.vertices[2][1] - 400), position=[400, 400])
    vFour = Vector((box.vertices[3][0] - 400, box.vertices[3][1] - 400), position=[400, 400])
    nOne = vOne.normalize()
    nTwo = vTwo.normalize()
    nThree = vThree.normalize()
    nFour = vFour.normalize()
    

    # normal of top projected to the left
    pygame.draw.line(screen, indigo, vOne.position, (nOne * 40).tail)
    # draws one line in one direction
    pygame.draw.line(screen, heather, (nOne * 350).tail, ((nOne * 350) + (testnormals[0] * 1000)).tail)
    # draws another line in the other direction
    pygame.draw.line(screen, heather, (nOne * 350).tail, ((nOne * 350) + (testnormals[0] * -1000)).tail)
    

    # normal of the right projected to the top
    pygame.draw.line(screen , indigo, vTwo.position, (nTwo * 40).tail)
    pygame.draw.line(screen, heather, (nTwo * 350).tail, ((nTwo * 350) + (testnormals[1] * 1000)).tail)
    pygame.draw.line(screen, heather, (nTwo * 350).tail, ((nTwo * 350) + (testnormals[1] * -1000)).tail)

    # normal of the bottom projected to the right
    pygame.draw.line(screen, indigo, vThree.position, (nThree * 40).tail)
    pygame.draw.line(screen, heather, (nThree * 350).tail, ((nThree * 350) + (testnormals[2] * 1000)).tail)
    pygame.draw.line(screen, heather, (nThree * 350).tail, ((nThree * 350) + (testnormals[2] * -1000)).tail)

    # normal of the left projected to the bottom
    pygame.draw.line(screen, indigo, vFour.position, (nFour * 40).tail)
    pygame.draw.line(screen, heather, (nFour * 350).tail, ((nFour * 350) + (testnormals[3] * 1000)).tail)
    pygame.draw.line(screen, heather, (nFour * 350).tail, ((nFour * 350) + (testnormals[3] * -1000)).tail)


    projections = []
    projectionstwo = []



    for i in range(len(box.vertices)):
        edgeProjection = [999999, -999999]
        for j in range(len(normals)):
            projection = dotproduct(box.vertices[j], normalize([0, 0], normals[i]))
            edgeProjection[0] = min(projection, edgeProjection[0])
            edgeProjection[1] = max(projection, edgeProjection[1])
        projections.append(edgeProjection)

    for i in range(len(box.vertices)):
        edgeProjection = [999999, -999999]
        for j in range(len(normalstwo)):
            projection = dotproduct(box.vertices[j], normalize([0, 0], normalstwo[i]))
            edgeProjection[0] = min(projection, edgeProjection[0])
            edgeProjection[1] = max(projection, edgeProjection[1])
        projections.append(edgeProjection)


    for i in range(len(boxtwo.vertices)):
        edgeProjection = [999999, -999999]
        for j in range(len(normals)):
            projection = dotproduct(boxtwo.vertices[j], normalize([0, 0], normals[i]))
            edgeProjection[0] = min(projection, edgeProjection[0])
            edgeProjection[1] = max(projection, edgeProjection[1])
        projectionstwo.append(edgeProjection)

    for i in range(len(boxtwo.vertices)):
        edgeProjection = [999999, -999999]
        for j in range(len(normalstwo)):
            projection = dotproduct(boxtwo.vertices[j], normalize([0, 0], normalstwo[i]))
            edgeProjection[0] = min(projection, edgeProjection[0])
            edgeProjection[1] = max(projection, edgeProjection[1])
        projectionstwo.append(edgeProjection)



    # print("projections", projections)
    # print("projectionstwo", projectionstwo)

    collision = False
    hits = 0
    hitpoints = []

    for i in range(len(projections)):
        if intervals_overlap(projections[i], projectionstwo[i]):
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




    # Update the display
    pygame.display.flip()

    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()






# 1 * [0, 0, 1]
# [0, 0, 1]

# 0 * [0.5, 0.5, 0.5]
# [0, 0, 0]

# -2 *  [-0.5, 1, 0.5]
# [1, -2, -1]

# [1, -2, 0]

