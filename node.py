from random import choice

from ball import Ball

DENSITY = 1
SIZE = 16

class Node(Ball):
    
    def __init__(self, world, position, velocity = None, color = None, mass = SIZE / DENSITY, density = DENSITY):
        if color == None: color = choice(world.COLORS)
        super(Node, self).__init__(world = world, position = position, velocity = velocity,
                                   color = color, mass = mass, density = density, wrap = False)
    
    def update(self, millis):
        reverseGravity = None if self.wrap else False
        super(Node, self).update(millis, reverseGravity = reverseGravity)
        
        # start wrapping around screen if already onscreen
        if self.wrap == False:
            if ( self.position[0] > 0 and self.position[0] < self.world.width
                 and self.position[1] > 0 and self.position[1] < self.world.height ):
                self.wrap = True
        
        if self.world.player != None:
            self.checkPlayerCollision(self.world.player)
        
        # for node in [sprite for sprite in self.world.sprites if isinstance(sprite, Node)]:
        #     if node != self:
        #         if self.checkCollision(node): self.world.nodeNodeCollide(self, node)
    
    def checkPlayerCollision(self, player):
        radiusSq = (self.mass * self.density + player.mass * player.density)**2
        distSq = (self.position[0] - player.position[0])**2 + (self.position[1] - player.position[1])**2
        if distSq <= radiusSq:
            self.world.playerNodeCollide(self)