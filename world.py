from player import Player
from node import Node

BACKGROUND = (32, 32, 32)

class World:
    
    # constants

    COLORS = (
        (127, 127, 0),
        (0, 127, 127),
        (127, 0, 127)
    )
    
    G = 1   # gravitational constant
    
    def __init__(self, surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        
        self.sprites = []
        self.player = Player(self, [self.width / 2, self.height / 2])
        self.sprites.append(self.player)
    
    def update(self, keys):
        for sprite in self.sprites:
            sprite.update()
    
    def draw(self):
        self.surface.fill(BACKGROUND)
        
        for sprite in self.sprites:
            sprite.draw(self.surface)
    
    def playerNodeCollide(self, node):
        player.score(node)
        sprites.remove(node)
        