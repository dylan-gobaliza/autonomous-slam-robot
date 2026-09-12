# import and initialise pygame
import pygame
import sys

pygame.init()

# set up the game window
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Sonar SLAM Robot Sandbox - Phase 1")

# caps frame rate at 60 FPS
clock = pygame.time.Clock()

# robot starting position - center of screen: x=(1000/2), y=(700/2)
robot_x = 500
robot_y = 350
robot_radius = 10

# sim loop
running = True
while running:
    # 1. quit game if press quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. change screen to dark grey (RGB)
    screen.fill((30, 30, 30))

    # 3. draw robot (blue circle)
    pygame.draw.circle(screen, (0, 150, 255), (robot_x, robot_y), robot_radius)

    # 4. refresh display & limit to 60 frames per second
    pygame.display.flip()
    clock.tick(60)

# quit Pygame cleanly
pygame.quit()
sys.exit()