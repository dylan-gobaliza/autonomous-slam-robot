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
    ray_endpoints = [] # holds all ray end points for one loop, and then repeats frame after frame 

    start_angle = robot_angle - (FOV / 2) # finds angle of very first ray to the left of robot
    angle_step = FOV / (NUM_RAYS - 1) # calculates angle distance between each ray
    
    for i in range(NUM_RAYS):
        ray_angle_deg = start_angle + (i * angle_step) # finds the actual angle for each ray
        ray_angle = math.radians(ray_angle_deg) # converts to radians

        maximum_x = robot_x + MAX_RANGE * math.cos(ray_angle) # draws on 'MAX_RANGE' pixels out from robots position (robot_x, math.cos(rayangle))
        maximum_y = robot_y + MAX_RANGE * math.sin(ray_angle)

        ray_line = ((robot_x, robot_y), (maximum_x, maximum_y)) # line of the ray
        closest_hit = None
        min_distance = MAX_RANGE

        for rect in obstacles:
            hit = rect.clipline(ray_line)

            if hit:
                entry_x, entry_y = hit[0] # calls the first tuple pair (where the line first hit the obstacle) and assigns it to entry variables
                distance = math.hypot(entry_x - robot_x, entry_y - robot_y) # see assets/distance_formula

                if distance < min_distance:
                    # assigns the co-ordinates and distance to new values if needed
                    min_distance = distance 
                    closest_hit = (entry_x, entry_y)
  
        if closest_hit:
            hit_x, hit_y = closest_hit
            
            # 1. Append to current frame's ray rendering list
            ray_endpoints.append((hit_x, hit_y))
            
            # 2. Snap to grid resolution
            snapped_x = round(hit_x / GRID_RES) * GRID_RES
            snapped_y = round(hit_y / GRID_RES) * GRID_RES
            
            # 3. Add to persistent map set
            point_cloud.add((snapped_x, snapped_y))
        else:
            # No obstacle hit — ray extends to full range
            ray_endpoints.append((maximum_x, maximum_y))


    # --- D. RENDERING (BOTTOM TO TOP) ---
    # change screen colour
    screen.fill((30, 30, 30))
        
    for pt_x, pt_y in point_cloud:
        pygame.draw.circle(screen, (255, 50, 50), (int(pt_x), int(pt_y)), 1)
        
    for end_x, end_y in ray_endpoints:
        pygame.draw.line(screen, (0, 255, 100), (int(robot_x), int(robot_y)), (int(end_x), int(end_y)), 1)
    
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