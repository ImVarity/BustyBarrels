import pygame
import sys
from vector import Vector
import random
from particles import Particle
from render import *

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
def square_surf(width, height, color):
    # Create a surface with an alpha channel (transparency)
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Draw the rectangle on the surface
    pygame.draw.rect(surf, color, pygame.Rect(0, 0, width, height))
    return surf


r = Render((water_sprites[2]), (400, 400), 0)

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
    if tracker % 120 == 0:
        direction_x = -1
        direction_y = 0


        for i in range(20):
            p = Particle([pos[0], pos[1]], [random.randint(-324, 324) / 100 / 2, random.randint(-324, 0) / 100], random.randint(10, 20), "explosion")
            p.shrink_rate = .01
            p.gravity = 0.00
            particles.append(p)



    r.render_single(screen)
        



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
# import pygame
# import time

# # Initialize Pygame
# pygame.init()

# # Screen dimensions
# WIDTH, HEIGHT = 800, 600

# # Set up the screen
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Day-Night Cycle Simulation")

# # Create an overlay surface
# overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# # Function to update the overlay color
# def update_overlay(hour):
#     # Calculate color and alpha based on time
#     if 6 <= hour < 18:
#         # Daytime: transparent overlay
#         alpha = max(0, 255 - int((hour - 6) / 12 * 255))
#         color = (255, 255, 255, alpha)
#     else:
#         # Nighttime: dark overlay
#         alpha = min(255, int((hour - 18) / 12 * 255) if hour >= 18 else int((6 + hour) / 12 * 255))
#         color = (0, 0, 64, alpha)
    
#     overlay.fill(color)

# # Main game loop
# running = True
# hour = 6  # Starting at 6 AM
# last_time = time.time()

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Update the hour every second
#     current_time = time.time()
#     if current_time - last_time >= 1:
#         hour = (hour + 1) % 24
#         update_overlay(hour)
#         last_time = current_time

#     # Fill the screen with a base color
#     screen.fill((135, 206, 235))  # Sky blue color
#     print(hour)
#     # Draw the overlay
#     screen.blit(overlay, (0, 0))

#     # Update the display
#     pygame.display.flip()

# # Quit Pygame
# pygame.quit()
