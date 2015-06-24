from random import randint

import node
from node import Node

VELOCITY_DIVISOR = 300

class Spawner:
    
    def __init__(self, world):
        self.world = world
    
    def spawn(self):
        # determine random offscreen location
        spawnRange = node.SIZE
        
        # left/right or top/bottom
        if randint(0, 1) == 1:
            #top/bottom
            x = randint(0, self.world.width + spawnRange * 2) - spawnRange
            
            # top or bottom
            if randint(0, 1) == 1:
                y = -spawnRange
            else:
                y = self.world.height + spawnRange
        else:
            # left/right
            y = randint(0, self.world.height + spawnRange * 2) - spawnRange
            
            # left or right
            if randint(0, 1) == 1:
                x = -spawnRange
            else:
                x = self.world.width + spawnRange
        
        position = [x, y]
        
        # launch node onscreen
        diff = [self.world.width / 2 - position[0], self.world.height / 2 - position[1]]
        diff = [i / VELOCITY_DIVISOR for i in diff]
        
        # create node
        return Node(world = self.world, position = position, velocity = diff)