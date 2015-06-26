from ball import Ball
from random import randint, choice
from math import floor

class Particle(Ball):
    
    def __init__(self, world, position):
        color = choice(world.COLORS)#(randint(0, 255), randint(0, 255), randint(0, 255))
        
        super(Particle, self).__init__(world = world, position = position, color = color, mass = 1, affectsOthers = False, drawDepth = -1)
    
    def draw(self, surface):
        surface.set_at((int(self.position[0]), int(self.position[1])), self.color)