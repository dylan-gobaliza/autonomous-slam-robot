import math
import pygame

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_res = 2
        
        # obstacles matching your v2 layout
        self.obstacles = [

            pygame.Rect(0, 0, 900, 10),         # top wall
            pygame.Rect(0, 700 - 10, 900, 10), # bottom wall
            pygame.Rect(0, 0, 10, 700),      # left wall
            pygame.Rect(900 - 10, 0, 10, 700), # right wall (Middle Divider)

            pygame.Rect(150, 100, 120, 300),
            pygame.Rect(700, 200, 150, 250),
            pygame.Rect(400, 500, 250, 100),

        ]
        
        self.point_cloud = set()

    # following section taken from line 63 onwards in 'v2_automatic' - see for comment logic
    def cast_rays(self, robot_x, robot_y, robot_angle, FOV, NUM_RAYS, MAX_RANGE):
        ray_endpoints = []
        
        start_angle = robot_angle - (FOV / 2)
        angle_step = FOV / (NUM_RAYS - 1)

        for i in range(NUM_RAYS):
            ray_angle_deg = start_angle + (i * angle_step)
            ray_angle = math.radians(ray_angle_deg)

            maximum_x = robot_x + MAX_RANGE * math.cos(ray_angle)
            maximum_y = robot_y + MAX_RANGE * math.sin(ray_angle)

            ray_line = ((robot_x, robot_y), (maximum_x, maximum_y))
            closest_hit = None
            min_distance = MAX_RANGE

            for rect in self.obstacles:
                hit = rect.clipline(ray_line)
                
                if hit:
                    entry_x, entry_y = hit[0]
                    distance = math.hypot(entry_x - robot_x, entry_y - robot_y)
                    
                    if distance < min_distance:
                        min_distance = distance
                        closest_hit = (entry_x, entry_y)

            if closest_hit:
                hit_x, hit_y = closest_hit
                ray_endpoints.append((hit_x, hit_y))
                
                snapped_x = round(hit_x / self.grid_res) * self.grid_res
                snapped_y = round(hit_y / self.grid_res) * self.grid_res
                self.point_cloud.add((snapped_x, snapped_y))
            else:
                ray_endpoints.append((maximum_x, maximum_y))

        return ray_endpoints

    def draw_ground_truth(self, screen):
        for rect in self.obstacles:
            pygame.draw.rect(screen, (60, 60, 75), rect)
        
        for pt_x, pt_y in self.point_cloud:
            pygame.draw.circle(screen, (255, 50, 50), (int(pt_x), int(pt_y)), 2)

    def draw_occupancy_map(self, screen, offset_x):
        # Draw obstacles
        for rect in self.obstacles:
            pygame.draw.rect(screen, (60, 60, 75), rect)
        
        # Draw point cloud map
        for pt_x, pt_y in self.point_cloud:
            pygame.draw.circle(screen, (255, 50, 50), (int(pt_x) + offset_x, int(pt_y)), 2)