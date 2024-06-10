import math
# Vector class that allows to choose origin point to make things easier


class Vector:
    def __init__(self, tail, position=[0, 0]) -> None:
        self.position = position
        self.x = tail[0]
        self.y = tail[1]


    def dotproduct(self, other):
        return self.x * other.x + self.y * other.y

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            new_x = self.position[0] + (self.x * other)
            new_y = self.position[1] + (self.y * other)
            return Vector((new_x, new_y), position=self.position)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector) or isinstance(other, float):
            new_x = self.x + other.x
            new_y = self.y + other.y
            return Vector((new_x, new_y), position=self.position)
        return NotImplemented

            
    def __sub__(self, other):
        if isinstance(other, Vector):
            new_x = self.x - other.x
            new_y = self.y - other.y
            return Vector((new_x, new_y), position=self.position)
        return NotImplemented
            
    def normalize(self):
        # Calculate the vector components from p1 to p2
        vx = self.x
        vy = self.y
        
        # Calculate the magnitude of the vector
        magnitude = math.sqrt(vx ** 2 + vy ** 2)
        
        # Normalize the vector components
        if magnitude == 0: # To handle the case where p1 and p2 are the same point
            self.x = 0
            self.y = 0
            return Vector((self.x, self.y), position=self.position)
            
        else:
            self.x = vx / magnitude
            self.y = vy / magnitude
            return Vector((self.x, self.y), position=self.position)

        
    def setPosition(self, x, y):
        self.position[0] = x
        self.position[1] = y


    @property
    def tail(self):
        return list([self.x, self.y])
    
    @property
    def head(self):
        return list(self.position)


    def __str__(self):
        return f"Vector(x={self.x}, y={self.y}, position={self.position})"
    
    def __repr__(self):
        return self.__str__()