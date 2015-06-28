from random import choice
from math import sqrt, atan2, cos, sin
from pygame import draw, gfxdraw

class Ball(object):
    
    def __init__(self, world, position, velocity = None, color = None, mass = 16, density = 1, wrap = True, affectsOthers = True, drawDepth = 0):        
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
        self.drawDepth = drawDepth
    
    def update(self, millis, reverseGravity = None):
        # apply gravity
        if reverseGravity == None: reverseGravity = self.world.reverseGravity
        self.applyGravity([sprite for sprite in self.world.sprites if isinstance(sprite, Ball)], reverseGravity, millis)
        
        # update position
        self.position[0] += self.velocity[0] * millis / 1000
        self.position[1] += self.velocity[1] * millis / 1000

        # wrap around screen
        if self.wrap:
            radius = self.mass * self.density
            self.position[0] = (self.position[0] + radius) % (self.world.width + radius * 2) - radius
            self.position[1] = (self.position[1] + radius) % (self.world.height + radius * 2) - radius
            
    def applyForce(self, force):
        # add force to velocity
        self.velocity[0] += float(force[0]) / self.mass * 100.0;
        self.velocity[1] += float(force[1]) / self.mass * 100.0;
    
    def applyGravity(self, balls, reverse, millis):
        for ball in balls:
            if ball != self and ball.affectsOthers:
                # gravitational force: F = (g * mass * mass) / (distance * distance)
                diff = (ball.position[0] - self.position[0], ball.position[1] - self.position[1])
                distSq = diff[0]**2 + diff[1]**2
                distSq = max(distSq, (self.mass * self.density + ball.mass * ball.density)**2)
                dist = sqrt(distSq)
            
                strength = (self.mass * ball.mass * self.world.G) / distSq
                force = [ diff[0] / dist * strength * millis / 1000, diff[1] / dist * strength * millis / 1000, ]

                if reverse:
                     force = [ -force[0], -force[1] ]
                
                self.applyForce(force)
                
    
    def draw(self, surface):
        radius = self.mass * self.density
        draw.ellipse(
            surface,
            self.color,
            (   self.position[0] - radius,
                self.position[1] - radius,
                radius * 2, radius * 2      )
        )
    
    def checkCollision(self, ball):
        collisionDist = self.mass * self.density + ball.mass * ball.density
        distSq = (self.position[0] - ball.position[0])**2 + (self.position[1] - ball.position[1])**2
        return distSq < collisionDist**2
