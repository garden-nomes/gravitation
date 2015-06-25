import pygame
from pygame import key, font, time
from random import choice, randint

from player import Player
from node import Node
from spawner import Spawner
from ball import Ball
from particle import Particle

BACKGROUND = (32, 32, 32)
GUI_COLOR = (224, 224, 224)

class World(object):
    
    # publicly accesible constants
    
    COLORS = (
        (127, 127, 0),
        (0, 127, 127),
        (127, 0, 127)
    )
    
    G = 1000   # gravitational constant
    
    MAX_NODES = 8
    PARTICLE_COUNT = 100
    
    def __init__(self, surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        
        self.reverseGravity = False
        
        self.sprites = []
        
        self.player = Player(world = self, position = [self.width / 2, self.height / 2])
        self.add(self.player)
        
        self.spawner = Spawner(self)
        for i in range(self.MAX_NODES):
            self.add(self.spawner.spawn())
        
        self.scoreFont = font.Font(font.match_font('arialblack'), 36)
    
    def add(self, sprite):
        self.sprites.append(sprite)
        self.sprites = sorted(self.sprites, key = lambda d: d.drawDepth)

    def addParticle(self):
        position = [randint(0, self.width), randint(0, self.height)]
        self.add(Particle(self, position))
    
    def update(self, millis):
        keys = key.get_pressed()
        self.reverseGravity = keys[pygame.K_LSHIFT] or keys[pygame.K_SPACE]
        
        for sprite in self.sprites:
            sprite.update(millis)
    
    def draw(self):
        self.surface.fill(BACKGROUND)
        
        for sprite in self.sprites:
            sprite.draw(self.surface)
        
        self.renderGui()
    
    def playerNodeCollide(self, node):
        self.player.score(node)
        self.sprites.remove(node)
        self.add(self.spawner.spawn())
    
    def nodeNodeCollide(self, node1, node2):
        if node1.color == node2.color:
            color = choice((node1.color, node2.color))
            velocity = [ node1.velocity[0] + node2.velocity[0],
                         node1.velocity[1] + node2.velocity[1] ]
            position = [ node1.position[0] + (node1.position[0] - node2.position[0]) / 2,
                         node1.position[1] + (node1.position[1] - node2.position[1]) / 2 ]
            mass = node1.mass + node2.mass
            density = (node1.density + node2.density) / 2
        
            self.sprites.remove(node1)
            self.sprites.remove(node2)
            self.add(Node(
                world = self,
                color = color,
                position = position,
                velocity = velocity,
                mass = mass,
                density = density,
            ))
    
    def renderGui(self):
        text = self.scoreFont.render(str(self.player.maxChain), True, GUI_COLOR)
        position = (self.width / 2 - text.get_width() / 2, self.height - text.get_height() - 36)
        self.surface.blit(text, position)
        