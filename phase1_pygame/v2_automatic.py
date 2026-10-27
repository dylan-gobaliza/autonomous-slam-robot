import pygame, sys, math, random

pygame.init()
pygame.font.init()

# set up dual-view window dimensions
VIEW_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_WIDTH = VIEW_WIDTH * 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Sim - Dual-View Mapping (Ground Truth vs Robot Map)")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 18, bold=True)

# ------------------------------------------------------------

# movement speeds
robot_angle = 0.0
robot_speed = 2.5
turn_speed = 2.5

# robot position
robot_x = 450
robot_y = 350
robot_radius = 10
line_length = 20

# rays
FOV = 90.0
NUM_RAYS = 15
MAX_RANGE = 350.0


point_cloud = set()    # set() prevents duplicate points
GRID_RES = 2           # snaps hit points to a 2px grid

# obstacles creation
obstacles = [
    
    pygame.Rect(0, 0, VIEW_WIDTH, 10),         # top wall
    pygame.Rect(0, SCREEN_HEIGHT - 10, VIEW_WIDTH, 10), # bottom wall
    pygame.Rect(0, 0, 10, SCREEN_HEIGHT),      # left wall
    pygame.Rect(VIEW_WIDTH - 10, 0, 10, SCREEN_HEIGHT), # right wall (Middle Divider)
    
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

# --- RUN SENSORS FIRST SO THAT ROBOT CAN "SEE"

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

            # i. Append to current frame's ray rendering list
            ray_endpoints.append((hit_x, hit_y))
            
            # ii. Snap to grid resolution
            snapped_x = round(hit_x / GRID_RES) * GRID_RES
            snapped_y = round(hit_y / GRID_RES) * GRID_RES
            
            # iii. Add to persistent map set
            point_cloud.add((snapped_x, snapped_y))
        else:
            # No obstacle hit — ray extends to full range
            ray_endpoints.append((maximum_x, maximum_y))

# --- 2. AUTONOMOUS REACTIVE STEERING LOGIC (With Corridor / Gap Entry) ---
    ray_distances = [math.hypot(ex - robot_x, ey - robot_y) for ex, ey in ray_endpoints]
    
    left_clearance = min(ray_distances[0:5])
    front_clearance = min(ray_distances[5:10])
    right_clearance = min(ray_distances[10:15])

    SAFETY_DISTANCE = 70.0
    CRITICAL_DISTANCE = 40.0

    # i. Trapped check (backup)
    if front_clearance < CRITICAL_DISTANCE or (front_clearance < SAFETY_DISTANCE and left_clearance < SAFETY_DISTANCE and right_clearance < SAFETY_DISTANCE):
        nudge = random.uniform(-0.5, 0.5)
        robot_speed = -1.5
        if left_clearance > right_clearance:
            robot_angle -= (turn_speed * 1.5) + nudge
        else:
            robot_angle += (turn_speed * 1.5) + nudge
            
    # ii. Blocked directly in front
    elif front_clearance < SAFETY_DISTANCE:
        robot_speed = 0.0
        if left_clearance > right_clearance:
            robot_angle -= turn_speed
        else:
            robot_angle += turn_speed
            
    # iii. LOOKING INTO A GAP / CORRIDOR: If front is deep/clear, ignore side walls and drive in!
    elif front_clearance > 120:
        robot_speed = 2.0
        # No side-steering here, let it drive straight through the entrance

    # iv. Normal open space wall correction
    else:
        robot_speed = 2.0
        if left_clearance < SAFETY_DISTANCE / 2:
            robot_angle += turn_speed / 2
        elif right_clearance < SAFETY_DISTANCE / 2:
            robot_angle -= turn_speed / 2

    # Update position
    rad = math.radians(robot_angle)
    
    drift_x = random.uniform(-0.1, 0.1)
    drift_y = random.uniform(-0.1, 0.1)
    heading_drift = random.uniform(-0.2, 0.2)

    robot_x += (robot_speed * math.cos(rad)) + drift_x
    robot_y += (robot_speed * math.sin(rad)) + drift_y
    robot_angle += heading_drift

    # Boundary clamp
    robot_x = max(robot_radius + 10, min(VIEW_WIDTH - robot_radius - 10, robot_x))
    robot_y = max(robot_radius + 10, min(SCREEN_HEIGHT - robot_radius - 10, robot_y))

    # Update actual position based on autonomous movement decision
    rad = math.radians(robot_angle)
    robot_x += robot_speed * math.cos(rad)
    robot_y += robot_speed * math.sin(rad)

    # --- D. RENDERING (BOTTOM TO TOP) ---
    
    # change screen colour
    screen.fill((30, 30, 30))

    head_x = robot_x + line_length * math.cos(rad)
    head_y = robot_y + line_length * math.sin(rad)

    # LEFT PANEL: GROUND TRUTH VIEW (WORLD)

    # 1. Draw Obstacles
    for rect in obstacles:
        pygame.draw.rect(screen, (60, 60, 75), rect)

    # 2. Draw Point Cloud on Left Side
    for pt_x, pt_y in point_cloud:
        pygame.draw.circle(screen, (255, 50, 50), (int(pt_x), int(pt_y)), 1)

    # 3. Draw Active Sonar Rays
    for end_x, end_y in ray_endpoints:
        pygame.draw.line(screen, (0, 255, 100), (int(robot_x), int(robot_y)), (int(end_x), int(end_y)), 1)

    # 4. Draw Robot Body & Heading Line
    pygame.draw.circle(screen, (0, 150, 255), (int(robot_x), int(robot_y)), robot_radius)
    pygame.draw.line(screen, (225, 225, 225), (int(robot_x), int(robot_y)), (int(head_x), int(head_y)), 2)

    # RIGHT PANEL: ROBOT'S GENERATED MAP (RViz View)

    # 1. Draw Point Cloud shifted by VIEW_WIDTH (+1000px)
    for pt_x, pt_y in point_cloud:
        pygame.draw.circle(screen, (255, 50, 50), (int(pt_x) + VIEW_WIDTH, int(pt_y)), 1)

    # 2. Draw Robot Position on Map View
    right_robot_x = int(robot_x) + VIEW_WIDTH
    right_head_x = int(head_x) + VIEW_WIDTH
    pygame.draw.circle(screen, (0, 150, 255), (right_robot_x, int(robot_y)), robot_radius)
    pygame.draw.line(screen, (225, 225, 225), (right_robot_x, int(robot_y)), (right_head_x, int(head_y)), 2)


    # ============================================================
    # HUD / OVERLAYS & DIVIDER
    # ============================================================
    # Vertical Dividing Line
    pygame.draw.line(screen, (100, 100, 100), (VIEW_WIDTH, 0), (VIEW_WIDTH, SCREEN_HEIGHT), 3)

    # Header Labels
    left_label = font.render("[ GROUND TRUTH WORLD ]", True, (200, 200, 200))
    right_label = font.render("[ ROBOT OCCUPANCY MAP ]", True, (200, 200, 200))
    screen.blit(left_label, (20, 15))
    screen.blit(right_label, (VIEW_WIDTH + 20, 15))


    # refresh display & limit to 60 frames per second
    pygame.display.flip()
    clock.tick(60)

# quit Pygame cleanly
pygame.quit()
sys.exit()