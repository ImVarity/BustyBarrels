import pygame
import sys
from vector import Vector
import random
from particles import Particle

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
background_color = (0, 0, 0)  # Black

#     position      direction     size
particles = []

clock = pygame.time.Clock()

shrink_rate = 1
gravity = .5

# Main loop

tracker = 0

running = True
while running:
    screen.fill(background_color)
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tracker += 1
    # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(pos[0], pos[1], 50, 50))
    if tracker % 30 == 0:
        direction_x = -1
        direction_y = 0


        for i in range(20):
            v_x = random.randint(-200, 400) / 500 * direction_x * -random.randint(3, 5)
            v_y = random.randint(0, 400) / 500 * direction_y * -1
            p = Particle([pos[0], pos[1]], [v_x, v_y], random.randint(3, 5), "dust")
            p.gravity = -.02
            p.shrink_rate = .1
            particles.append(p)



    # for i in range(10):
    #     v_x = random.randint(0, 100) / 500 * direction.x * -random.randint(7, 8)
    #     v_y = random.randint(0, 340) / 500 * direction.y * -random.randint(1, 2)
    #     p = Particle([loc[0], loc[1]], [v_x, v_y], random.randint(3, 5), "dust")
    #     p.gravity = -.02
    #     p.shrink_rate = .1
    #     particles.append(p)

    for i in range(len(particles) -1, -1, -1):
        particle = particles[i]
        particle.all(screen)

        if particle.dead():
            particles.remove(particle)




    



    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
