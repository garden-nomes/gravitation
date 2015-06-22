from ball import Ball

class Node(Ball):
    DENSITY = 1
    
    def __init__(self, position, color = (255, 255, 255), size = 16):
        super(Node, self).__init__(position=position, color=COLORS[random.randint(0, 2)],
                                   mass=size / self.DENSITY, density=self.DENSITY)
    
    def draw(self, surface):
        super(Node, self).draw(surface)
    
    def update(self):
        if world.player: checkPlayerCollision(world.player)
        
        super(Node, self).update()
    
    def checkPlayerCollision(self, player):
        radiusSq = (self.mass * self.density + player.mass * player.density)**2
        distSq = (self.position[0] - ball.position[0])**2 + (self.position[1] - ball.position[1])**2
        if distSq <= radiusSq:
            world.playerNodeCollide(self)