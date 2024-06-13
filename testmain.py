import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Circular Clip Example")

# Define colors
background_color = (0, 0, 0)  # Black
circle_color = (255, 255, 255) # White

# Create a circular mask
mask_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
pygame.draw.circle(mask_surface, (255, 255, 255, 255), (screen_width // 2, screen_height // 2), 150)
mask = pygame.mask.from_surface(mask_surface)
mask_surface = mask.to_surface(setcolor=(255, 255, 255, 255))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the background color
    screen.fill(background_color)

    pygame.draw.rect(mask_surface, (34, 34, 34), pygame.Rect(screen_width / 2, screen_height / 2, 50, 50))
    # Blit the mask surface onto the main screen
    screen.blit(mask_surface, (0, 0))


    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
