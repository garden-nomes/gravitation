from random import choice
from pygame import draw, sprite

class Ball(sprite.Sprite):
    
    def __init__(self, world, position, color = None, velocity = [0, 0], mass = 16, density = 1, wrap = True):
        self.world = world
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.density = density
        if color == None:
            self.color = random.choice(world.COLORS)
        else:
            self.color = color
        self.wrap = wrap
    
    def update(self):
        # update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # wrap around screen
        if self.wrap:
            radius = self.mass * self.density
            self.position[0] = (self.position[0] + radius) % (self.world.width + radius * 2) - radius
            self.position[1] = (self.position[1] + radius) % (self.world.height + radius * 2) - radius
    
    def applyForce(self, force):
        # add force to velocity
        self.velocity[0] += force[0] / self.mass * 16;
        self.velocity[1] += force[1] / self.mass * 16;
    
    def applyGravity(self, balls, reverse = False):
        for ball in balls:
            if ball != self:
                # gravitational force: F = (g * mass * mass) / (distance * distance)
                diff = (ball.position[0] - self.position[0], ball.position[1] - self.position[1])
                distSq = diff[0]**2 + diff[1]**2
                distSq = max(distSq, (self.mass * self.density + ball.mass * ball.density)**2)
                
                
                strength = (self.mass * ball.mass * self.world.G) / distSq
                angle = math.atan2(diff[1], diff[0])
                force = [ math.cos(angle) * strength, math.sin(angle) * strength ]
                
                # reverse gravitational force if balls are of the same color
                if reverse:
                     force = [ -force[0], -force[1] ]
                
                self.applyForce(force)
                
    
    def draw(self, surface):
        radius = self.mass * self.density
        draw.ellipse(
            surface,
            self.color,
            (self.position[0] - radius, self.position[1] - radius, radius * 2, radius * 2)
        )
    
    def checkCollisions(self, balls):
        return False