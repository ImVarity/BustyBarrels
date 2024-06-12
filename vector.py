import math
# Vector class that allows to choose origin point to make things easier


class Vector:
    def __init__(self, tail, origin=[0, 0]) -> None:
        self.origin = origin
        self.x = tail[0]
        self.y = tail[1]


    def dotproduct(self, other):
        return self.x * other.x + self.y * other.y

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            new_x = self.origin[0] + (self.x * other)
            new_y = self.origin[1] + (self.y * other)
            return Vector((new_x, new_y), origin=self.origin)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector) or isinstance(other, float):
            new_x = self.x + other.x
            new_y = self.y + other.y
            return Vector((new_x, new_y), origin=self.origin)
        return NotImplemented

            
    def __sub__(self, other):
        if isinstance(other, Vector):
            new_x = self.x - other.x
            new_y = self.y - other.y
            return Vector((new_x, new_y), origin=self.origin)
        return NotImplemented
    

    # might have to fix, dont want to change self.x, self.y and return another vector
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
            return Vector((self.x, self.y), origin=self.origin)
            
        else:
            self.x = vx / magnitude
            self.y = vy / magnitude
            return Vector((self.x, self.y), origin=self.origin)

        
    def setorigin(self, x, y):
        self.origin[0] = x
        self.origin[1] = y


    @property
    def tail(self):
        return list([self.x, self.y])
    
    @property
    def head(self):
        return list(self.origin)


    def __str__(self):
        return f"Vector(x={self.x}, y={self.y}, origin={self.origin})"
    
    def __repr__(self):
        return self.__str__()