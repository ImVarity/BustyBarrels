import pygame


class HealthBar:
    def __init__(self, health, color):
        self.health = health
        self.maxhealth = health
        self.color = color
        self.width = 16


    def draw(self, surface, center, height):
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(center.x - 9, center.y + height / 2 + 1, 18, 5))
        pygame.draw.rect(surface, self.color, pygame.Rect(center.x - 8, center.y + height / 2 + 2, self.width, 3))

    def damage(self, damage):
        self.health -= damage
        self.width = self.health / self.maxhealth * 16
