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

# --- B. INPUT & ROBOT MOVEMENT ---
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        robot_angle -= turn_speed
    if key[pygame.K_d]:
        robot_angle += turn_speed
    # TODO: Convert robot_angle to radians using math.radians()
    # TODO: Update robot_x and robot_y along cos/sin vectors when 'W' or 'S' is pressed


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
    # TODO: Clear screen with background color
    
    # TODO: Draw obstacles (loop through rect list)
    
    # TODO: Draw persistent point cloud (loop through point set and draw tiny circles)
    
    # TODO: Draw active sonar rays (loop through temporary ray end points and draw lines)
    
    # TODO: Draw robot body (circle) and heading line (line in direction of angle)

# quit Pygame cleanly
pygame.quit()
sys.exit()