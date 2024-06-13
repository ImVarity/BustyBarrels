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

# 1 * [0, 0, 1]
# [0, 0, 1]

# 0 * [0.5, 0.5, 0.5]
# [0, 0, 0]

# -2 *  [-0.5, 1, 0.5]
# [1, -2, -1]

# [1, -2, 0]
