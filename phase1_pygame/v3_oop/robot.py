import math, pygame 

class Robot: 
    def __init__(self, x, y):
        # assign variables
        self.x = x
        self.y = y

        self.radius = 10
        self.angle = 0.0
        self.speed = 2.5
        self.turn_speed = 2.5

    def move(self): 
        rad = math.radians(self.angle)
        
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)

    def draw(self, screen, offset_x=0):
        # robot body
        pygame.draw.circle(screen, (0, 150, 255), (int(self.x) + offset_x, int(self.y)), self.radius)
        
        # heading line
        rad = math.radians(self.angle)
        
        end_x = self.x + (self.radius * 1.5) * math.cos(rad)
        end_y = self.y + (self.radius * 1.5) * math.sin(rad)
        pygame.draw.line(screen, (255, 255, 255), (int(self.x) + offset_x, int(self.y)), (int(end_x) + offset_x, int(end_y)), 2)