from random import choice
from math import atan2, cos, sin
from pygame import draw

class Ball(object):
    
    def __init__(self, world, position, velocity = None, color = None, mass = 16, density = 1, wrap = True, affectsOthers = True):        
        self.world = world
        self.position = position
        if velocity == None: velocity = [0, 0]
        self.velocity = velocity
        self.mass = mass
        self.density = density
        if color == None:
            self.color = random.choice(world.COLORS)
        else:
            self.color = color
        self.wrap = wrap
        self.affectsOthers = affectsOthers
    
    def update(self):
        # apply gravity
        self.applyGravity([sprite for sprite in self.world.sprites if isinstance(sprite, Ball)], self.world.reverseGravity)
        
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
            if ball != self and ball.affectsOthers:
                # gravitational force: F = (g * mass * mass) / (distance * distance)
                diff = (ball.position[0] - self.position[0], ball.position[1] - self.position[1])
                distSq = diff[0]**2 + diff[1]**2
                if (distSq > 1000):
                    distSq = max(distSq, (self.mass * self.density + ball.mass * ball.density)**2)
                
                
                    strength = (self.mass * ball.mass * self.world.G) / distSq
                    angle = atan2(diff[1], diff[0])
                    force = [ cos(angle) * strength, sin(angle) * strength ]

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
    
    def checkCollision(self, ball):
        collisionDist = self.mass * self.density + ball.mass * ball.density
        distSq = (self.position[0] - ball.position[0])**2 + (self.position[1] - ball.position[1])**2
        return distSq < collisionDist**2