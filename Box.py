import pygame
import math

class Square:
    def __init__(self, x=400, y=300, width=100, height=100, velocity=4):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.velocity = velocity
        self.direction = 0
        self.angle = 0

        self.mass = .5

        self.vec = [0, 0]

        self.verticalKE = 0
        self.horiztonalKE = 0

        self.KE = 0



    def VtoKE(self, V, MASS):
        return ((MASS * V ** 2) / 2)

    def KEtoV(self, KE, MASS):
        return math.sqrt(2 * KE / MASS)
    

    def checkCollision(self, shape):

        # Using given collision
        if (self.rect.colliderect(shape.rect)):
            self.transferMomentum(shape)


    def transferMomentum(self, shape):
        # Checks if you move in another direction after pushing so it doesnt stick
        if (abs(shape.vec[0] - self.vec[0]) == 2):
            return
        if (abs(shape.vec[1] - self.vec[1] == 2)):
            return
        else:
            print(self.vec, shape.vec)

            magnitudeself = math.sqrt(self.vec[0] ** 2 + self.vec[1] ** 2)
            magnitudeshape = math.sqrt(shape.vec[0] ** 2 + shape.vec[1] ** 2)

            self.KE = self.VtoKE(magnitudeself, self.mass)
            shape.KE = self.VtoKE(magnitudeshape, shape.mass)

            # If colliding in the same direction
            if self.vec[0] == 1 and shape.vec[0] == 0:
                shape.vec[0] = self.vec[0]
                shape.KE = self.KE
                self.KE = self.kinetic_energy_lost(self.mass, self.vec[0] * self.velocity, shape.mass, 0)

            # If collidion in opposite directions

            if self.vec[0] == 1 and shape.vec[0] == -1:
                pass
                




            
            # if shape.vec[0] > self.vec[0]:
            #     self.vec[0] = shape.vec[0]
            #     shape.KE = self.KE
            #     print("pink hits grey")
            # elif shape.vec[0] < self.vec[0]: # grey hits pink
            #     shape.vec[0] = self.vec[0]
            #     self.KE = shape.KE
            #     print("grey hits pink")
            # if shape.vec[1] > self.vec[1]:
            #     self.vec[1] = shape.vec[1]
            #     shape.KE = self.KE
            # elif shape.vec[1] < self.vec[1]:
            #     shape.vec[1] = self.vec[1]
            #     self.KE = shape.KE
                print('4')

            # self.KE = self.VtoKE(self.velocity, self.mass)
            # shape.velocity = self.VtoKE(self.KE, shape.mass)


            
    def kinetic_energy_lost(self, m1, v1, m2, v2):
        # Initial kinetic energy
        KE_initial = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
        
        # Final velocity after collision (conservation of momentum)
        vf = (m1 * v1 + m2 * v2) / (m1 + m2)
        
        # Final kinetic energy
        KE_final = 0.5 * (m1 + m2) * vf**2
        
        # Kinetic energy lost
        KE_lost = KE_initial - KE_final
        
        return KE_lost

    # Bounces shapes off walls
    def wallCollision(self):
        if self.rect.x < 0 or self.rect.x + self.width > 800 :
            self.vec[0] *= -1
        if self.rect.y < 0 or self.rect.y + self.height > 600:
            self.vec[1] *= -1



    def updateMovement(self):
        self.rect.x += self.vec[0] * self.KEtoV(self.KE, self.mass)
        self.rect.y += self.vec[1] * self.KEtoV(self.KE, self.mass)

    
    def handleInput(self, input):
        
        if (input["right"]):
            self.vec[0] = 1
            self.KE += 1
        elif (input["left"]):
            self.vec[0] = -1


        if (input["down"]):
            self.vec[1] = 1
        elif (input["up"]):
            self.vec[1] = -1



        if (input["clockwise"]):
            self.angle -= 5
        if (input["counterclockwise"]):
            self.angle += 5

        if (input["reset"]):
            self.angle = 0

        
        input = {
            "right": False,
            "left" : False,
            "down" : False,
            "up": False,
            "clockwise" : False,
            "counterclockwise": False,
            "reset": False
        }
        
        return input



    def center(self):
        return [self.rect.x + (self.width / 2), self.rect.y + (self.height / 2)]
    
    def getDir(self):
        return self.direction
    