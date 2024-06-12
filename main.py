import pygame
import sys
from Square import Square
import math
from vector import Vector
from Circle import Circle

screen_width = 800
screen_height = 800

heather = (210, 145, 255)
indigo = (75, 0, 130)
origin = [screen_width / 2, screen_height / 2]
pink = (255, 182, 193)
blue = (30, 144, 255)

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
    "reset": False
}

rotation_input = {
    "clockwise" : False,
    "counterclockwise" : False
}



box = Square([400, 400], 100, 100, blue)
normals = box.normals()

boxtwo = Square([400, 400], 100, 100, pink)
normalstwo = boxtwo.normals()

circle = Circle((400, 200), 30, indigo)



# Main loop
running = True
while running:
    screen.fill(white)
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                pass

    rotation_input["counterclockwise"] = keys[pygame.K_e]
    rotation_input["clockwise"] = keys[pygame.K_q]

    input["up"] = keys[pygame.K_w]
    input["down"] = keys[pygame.K_s]
    input["left"] = keys[pygame.K_a]
    input["right"] = keys[pygame.K_d]

    input["reset"] = keys[pygame.K_z]

    
    


    # box.rotate()
    # box.transform()
    normals = box.normals()
    box.draw(screen)

    
    # box.rotate
    # boxtwo.transform()
    normalstwo = boxtwo.normals()
    boxtwo.draw(screen)

    # box.move(input)
    boxtwo.move(input)
    boxtwo.handle_rotation(rotation_input)
    box.handle_rotation(rotation_input)
    


    boxtwo.draw_projection(screen, normalstwo)
    box.draw_projection(screen, normals)
    box.handle_collision(normals, normalstwo, boxtwo, screen)





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

    # # normal of top projected to the left
    # pygame.draw.line(screen, indigo, box.center.tail, (nOne * 40).tail)
    # # draws one line in one direction
    # pygame.draw.line(screen, heather, ((nOne * 350 + box.center) - Vector((400, 400))).tail, ((nOne * 350) + (normals[0] * 1000)).tail)
    # # draws another line in the other direction
    # pygame.draw.line(screen, heather, ((nOne * 350 + box.center) - Vector((400, 400))).tail, ((nOne * 350) + (normals[0] * -1000)).tail)
    

    # # normal of the right projected to the top
    # pygame.draw.line(screen , indigo, box.center.tail, (nTwo * 40).tail)
    # pygame.draw.line(screen, heather, ((nTwo * 350 + box.center) - Vector((400, 400))).tail, ((nTwo * 350) + (normals[1] * 1000)).tail)
    # pygame.draw.line(screen, heather, ((nTwo * 350 + box.center) - Vector((400, 400))).tail, ((nTwo * 350) + (normals[1] * -1000)).tail)

    # # normal of the bottom projected to the right
    # pygame.draw.line(screen, indigo, box.center.tail, (nThree * 40).tail)
    # pygame.draw.line(screen, heather, ((nThree * 350 + box.center) - Vector((400, 400))).tail, ((nThree * 350) + (normals[2] * 1000)).tail)
    # pygame.draw.line(screen, heather, ((nThree * 350 + box.center) - Vector((400, 400))).tail, ((nThree * 350) + (normals[2] * -1000)).tail)

    # # normal of the left projected to the bottom
    # pygame.draw.line(screen, indigo, box.center.tail, (nFour * 40).tail)
    # pygame.draw.line(screen, heather, ((nFour * 350 + box.center) - Vector((400, 400))).tail, ((nFour * 350) + (normals[3] * 1000)).tail)
    # pygame.draw.line(screen, heather, ((nFour * 350 + box.center) - Vector((400, 400))).tail, ((nFour * 350) + (normals[3] * -1000)).tail)