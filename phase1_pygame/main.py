import pygame
import sys
import math

pygame.init()

# set up the game window
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("pygame sim - phase 1")

clock = pygame.time.Clock()

# ------------------------------------------------------------

# movement speeds
robot_angle = 0.0
robot_speed = 3.0
turn_speed = 2.5

# robot position
robot_x = 500
robot_y = 350
robot_radius = 10
line_length = 20

# rays
FOV = 90.0
NUM_RAYS = 15
MAX_RANGE = 350.0


point_cloud = set()    # set() prevents duplicate points
GRID_RES = 2           # Snaps hit points to a 2px grid

# obstacles creation
obstacles = [
    pygame.Rect(150, 100, 120, 300),
    pygame.Rect(700, 200, 150, 250),
    pygame.Rect(400, 500, 250, 100),
]

# ------------------------------------------------------------

running = True
while running:
    # QUIT GAME
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# robot movement and radian conversion
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        robot_angle -= turn_speed
    if key[pygame.K_d]:
        robot_angle += turn_speed

    rad = math.radians(robot_angle) # convert to radians so that trig can be used

    if key[pygame.K_w]:
        robot_x += robot_speed * math.cos(rad) # change in x = speed * cos(theta)
        robot_y += robot_speed * math.sin(rad) # change in y = speed * sin(theta)
    if key[pygame.K_s]:
        robot_x -= robot_speed * math.cos(rad)
        robot_y -= robot_speed * math.sin(rad)


    # --- C. SENSOR CALCULATIONS & MAP UPDATES ---
    # TODO: Create a temporary list to hold ray end points for rendering this frame
    # TODO: Calculate start_angle (robot_angle - FOV/2) and angle_step across NUM_RAYS
    
    # TODO: Loop through each of the 15 rays:
    #   1. Compute ray angle in radians
    #   2. Compute max-range end coordinates (end_x, end_y) using trig
    #   3. Check ray collision against all obstacle rects (e.g., rect.clipline())
    #   4. Find the closest hit point along the ray
    #   5. IF hit:
    #        - Append hit point to temporary ray list
    #        - Snap hit point using GRID_RES
    #        - Add snapped tuple to persistent point cloud set
    #      ELSE:
    #        - Append max-range end point to temporary ray list


    # --- D. RENDERING (BOTTOM TO TOP) ---
    # change screen colour
    screen.fill((30, 30, 30))
    
    # TODO: Draw obstacles (loop through rect list)
    
    # TODO: Draw persistent point cloud (loop through point set and draw tiny circles)
    
    # TODO: Draw active sonar rays (loop through temporary ray end points and draw lines)
    
    # draw robot and heading line (blue circle)
    head_x = robot_x + line_length * math.cos(rad)
    head_y = robot_y + line_length * math.sin(rad)

    pygame.draw.circle(screen, (0, 150, 255), (robot_x, robot_y), robot_radius)
    pygame.draw.line(screen, (225, 225, 225), (robot_x, robot_y), (head_x, head_y), 2)


    # refresh display & limit to 60 frames per second
    pygame.display.flip()
    clock.tick(60)

# quit Pygame cleanly
pygame.quit()
sys.exit()