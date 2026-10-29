import pygame, sys, random, math, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from v3_oop.robot import Robot
from v3_oop.world import World

# Initialize Pygame
pygame.init()
pygame.font.init

VIEW_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_WIDTH = VIEW_WIDTH * 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Sim - OOP Automatic (v3)")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 18, bold=True)

# Instantiate objects
robot = Robot(300, 250)
world = World(VIEW_WIDTH, SCREEN_HEIGHT)

FOV = 90
NUM_RAYS = 15
MAX_RANGE = 350.0

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 1. Cast Rays using World
    ray_endpoints = world.cast_rays(robot.x, robot.y, robot.angle, FOV, NUM_RAYS, MAX_RANGE)

    # 2. AUTONOMOUS REACTIVE STEERING LOGIC
    ray_distances = [math.hypot(ex - robot.x, ey - robot.y) for ex, ey in ray_endpoints]
    
    left_clearance = min(ray_distances[0:5])
    front_clearance = min(ray_distances[5:10])
    right_clearance = min(ray_distances[10:15])

    SAFETY_DISTANCE = 70.0
    CRITICAL_DISTANCE = 40.0

    # i. Trapped check (backup)
    if front_clearance < CRITICAL_DISTANCE or (front_clearance < SAFETY_DISTANCE and left_clearance < SAFETY_DISTANCE and right_clearance < SAFETY_DISTANCE):
        nudge = random.uniform(-0.5, 0.5)
        robot.speed = -1.5
        if left_clearance > right_clearance:
            robot.angle -= (robot.turn_speed * 1.5) + nudge
        else:
            robot.angle += (robot.turn_speed * 1.5) + nudge
            
    # ii. Blocked directly in front
    elif front_clearance < SAFETY_DISTANCE:
        robot.speed = 0.0
        if left_clearance > right_clearance:
            robot.angle -= robot.turn_speed
        else:
            robot.angle += robot.turn_speed
            
    # iii. LOOKING INTO A GAP / CORRIDOR
    elif front_clearance > 120:
        robot.speed = 2.0

    # iv. Normal open space wall correction
    else:
        robot.speed = 2.0
        if left_clearance < SAFETY_DISTANCE / 2:
            robot.angle += robot.turn_speed / 2
        elif right_clearance < SAFETY_DISTANCE / 2:
            robot.angle -= robot.turn_speed / 2

    # 3. Update Robot Movement Position
    robot.move()

    # Boundary clamping
    robot.x = max(20, min(VIEW_WIDTH - 20, robot.x))
    robot.y = max(20, min(SCREEN_HEIGHT - 20, robot.y))

    # 4. RENDERING SCREEN
    screen.fill((25, 25, 30))

    # ============================================================
    # LEFT PANEL: GROUND TRUTH VIEW (WORLD)
    # ============================================================
    world.draw_ground_truth(screen)
    
    # Draw Active Sonar Rays
    for end_x, end_y in ray_endpoints:
        pygame.draw.line(screen, (0, 255, 100), (int(robot.x), int(robot.y)), (int(end_x), int(end_y)), 1)

    # Draw Robot Body & Heading Line (Ground Truth)
    robot.draw(screen, offset_x=0)

    # ============================================================
    # RIGHT PANEL: ROBOT'S GENERATED MAP (RViz View)
    # ============================================================
    world.draw_occupancy_map(screen, VIEW_WIDTH)
    
    # Draw Robot Position on Map View (Ghost robot localization)
    robot.draw(screen, offset_x=VIEW_WIDTH)

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

    # Refresh display & limit to 60 frames per second
    pygame.display.flip()
    clock.tick(60)