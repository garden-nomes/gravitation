import pygame
from pygame import key, font, time, mixer
from random import choice, randint
from math import sqrt

from player import Player
from node import Node
from spawner import Spawner
from ball import Ball
from particle import Particle
from text import Text

BACKGROUND = (32, 32, 32)
GUI_COLOR = (0, 0, 0)
HITS = 6

class World(object):
    
    # publicly accesible constants
    
    COLORS = (
        (189, 125, 15),
        (125, 15, 188),
        (15, 188, 125)
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
        
        self.background = BACKGROUND
        
        self.spawner = Spawner(self)
        for i in range(self.MAX_NODES):
            self.add(self.spawner.spawn())
        
        self.text = Text(self)
        self.text.flash()
        self.text.showTutorial()  
              
        self.collisionSound = mixer.Sound("resources/chime.aif")
        self.hitSounds = []
        for i in range(1, HITS + 1):
            self.hitSounds.append(mixer.Sound("resources/hit" + str(i) + ".aif"))
    
    def add(self, sprite):
        self.sprites.append(sprite)
        self.sprites = sorted(self.sprites, key = lambda d: d.drawDepth)

    def addParticle(self):
        position = [randint(0, self.width), randint(0, self.height)]
        self.add(Particle(self, position))
    
    def update(self, millis):
        keys = key.get_pressed()
        self.reverseGravity = keys[pygame.K_LSHIFT] or keys[pygame.K_SPACE]
        
        self.text.update(millis)
        
        for sprite in self.sprites:
            sprite.update(millis)
    
    def draw(self):
        self.surface.fill(self.background)
        
        for sprite in self.sprites:
            sprite.draw(self.surface)
        
        self.text.draw(self.surface)
        
    
    def playerNodeCollide(self, node):
        self.player.score(node)
        self.sprites.remove(node)
        self.add(self.spawner.spawn())
        self.dink(self.player, node)
    
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
    
    def dong(self):
        self.collisionSound.play()
    
    def dink(self, ball1, ball2):
        diff = [ball1.velocity[0] - ball2.velocity[0], ball1.velocity[1] - ball2.velocity[1]]
        dist = sqrt(diff[0]**2 + diff[1]**2)
        volume = dist / 500
        if volume > 1: volume = 1
        sound = choice(self.hitSounds)
        sound.set_volume(volume)
        sound.play()
