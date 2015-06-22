import os, sys, random, math
import pygame

# constants

WIDTH = 1440
HEIGHT = 900
BACKGROUND = [0, 0, 0]
G = 1

COLORS = (
    (127, 127, 0),
    (0, 127, 127),
    (127, 0, 127)
)

class Ball(pygame.sprite.Sprite):
    
    location = [0, 0]
    velocity = [0, 0]
    
    def __init__(self, location = [WIDTH / 2, HEIGHT / 2], mass = 16, density = 1, color = (127, 0, 0), wrap = True):
        self.location = location
        self.velocity = [0, 0]
        self.mass = mass
        self.density = density
        self.color = color
        self.wrap = wrap
    
    def update(self):
        # update location
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        
        # wrap around screen
        if self.wrap:
            radius = self.mass * self.density
            self.location[0] = (self.location[0] + radius) % (WIDTH + radius * 2) - radius
            self.location[1] = (self.location[1] + radius) % (HEIGHT + radius * 2) - radius
    
    def applyForce(self, force):
        # add force to velocity
        self.velocity[0] += force[0] / self.mass * 16;
        self.velocity[1] += force[1] / self.mass * 16;
    
    def applyGravity(self, balls):
        for ball in balls:
            if ball != self:
                # gravitational force: F = (g * mass * mass) / (distance * distance)
                diff = (ball.location[0] - self.location[0], ball.location[1] - self.location[1])
                distSq = diff[0]**2 + diff[1]**2
                distSq = max(distSq, (self.mass * self.density + ball.mass * ball.density)**2)
                
                
                strength = (self.mass * ball.mass * G) / distSq
                angle = math.atan2(diff[1], diff[0])
                force = [ math.cos(angle) * strength, math.sin(angle) * strength ]
                
                # reverse gravitational force if balls are of the same color
                # if ball.color == self.color:
                #     force = [ -force[0], -force[1] ]
                
                self.applyForce(force)
                
    
    def draw(self, surface):
        radius = self.mass * self.density
        pygame.draw.ellipse(
            surface,
            self.color,
            (self.location[0] - radius, self.location[1] - radius, radius * 2, radius * 2)
        )
    
    def checkCollisions(self, balls):
        return False

class Player(Ball):
    
    PLAYER_COLOR = (127, 0, 0)
    PLAYER_SIZE = 24
    ACC = 1
    DENSITY = 0.25
    
    def __init__(self, location = [WIDTH / 2, HEIGHT / 2], size = PLAYER_SIZE,
                 color = PLAYER_COLOR, acceleration = ACC, maxChain = 3):
                 
        self.color = COLORS[random.randint(0, 2)]
        self.acceleration = acceleration
        self.maxChain = maxChain
        self.baseMass = size / self.DENSITY
        
        self.chain = 0
        self.baseChainAngle = 0
        
        super(Player, self).__init__(location=location, mass=size / self.DENSITY, color=self.color, density=self.DENSITY)
        
    def draw(self, surface):
        super(Player, self).draw(surface)
        
        angle = self.baseChainAngle
        radius = self.mass * self.density
        for i in range(self.chain):
            x = self.location[0] + math.cos(angle) * radius * 2
            y = self.location[1] + math.sin(angle) * radius * 2
            size = radius / 4
            pygame.draw.ellipse(
                surface,
                self.color,
                [x - size, y - size, size * 2, size * 2]
            )
            angle += math.pi * 2 / self.chain
            angle %= math.pi * 2
    
    def update(self):
        # get input
        keys = pygame.key.get_pressed()
        
        # move based in key input
        if keys[pygame.K_LEFT]:
            self.applyForce([ -self.acceleration, 0 ])
        if keys[pygame.K_RIGHT]:
            self.applyForce([ self.acceleration, 0 ])
        if keys[pygame.K_UP]:
            self.applyForce([ 0, -self.acceleration ])
        if keys[pygame.K_DOWN]:
            self.applyForce([ 0, self.acceleration ])
        
        # update position
        super(Player, self).update()
        
        # rotate score chain
        self.baseChainAngle = (self.baseChainAngle + math.pi / 512) % (math.pi * 2)
    
    def score(self, ball):
        if self.color == ball.color:
            self.chain += 1
            if self.chain > self.maxChain:
                self.mass = self.baseMass
                self.chain = 0
                self.maxChain += 1
            else:
                self.mass += ball.mass
        else:
            self.mass = self.baseMass
            self.chain = 0
            self.color = ball.color
        
class Node(Ball):
    DENSITY = 1
    
    def __init__(self, location, color = (255, 255, 255), size = 16):
        super(Node, self).__init__(location=location, color=COLORS[random.randint(0, 2)],
                                   mass=size / self.DENSITY, density=self.DENSITY)
    
    def draw(self, surface):
        super(Node, self).draw(surface)
    
    def update(self):
        super(Node, self).update()
    
    def checkCollisions(self, balls):
        for ball in balls:
            if ball != self:
                if isinstance(ball, Player):
                    radiusSq = (self.mass * self.density + ball.mass * ball.density)**2
                    distSq = (self.location[0] - ball.location[0])**2 + (self.location[1] - ball.location[1])**2
                    if distSq <= radiusSq:
                        ball.score(self)
                        return True
        
        return False
        

def main():

    # initialize pygame

    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)

    # initialize game objects

    #ball = Ball(WIDTH / 2, HEIGHT / 2)
    player = Player()
    balls = [ player ]
    
    font = pygame.font.Font(pygame.font.match_font('arialblack'), 36)

    # begin main game loop
    
    nodes = []
    done = False
    while not done:
    
        # check for program exit signal
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                balls.append(Node([ random.randint(0, WIDTH), random.randint(0, HEIGHT) ]))

        # check for input
        
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True
    
        # draw background
    
        screen.fill(BACKGROUND)
        
        # update game objects
        for ball in balls:
            if ball.checkCollisions(balls): balls.remove(ball)
            ball.applyGravity(balls)
            ball.update()
    
        # draw game objects
        for ball in balls:
            ball.draw(screen)
        
        text = font.render(str(player.maxChain), True, (255, 255, 255))
        textpos = (WIDTH / 2 - text.get_width() / 2, 16)
        screen.blit(text, textpos)
        #ball.draw(screen)
        #for node in nodes: node.draw(screen)
    
        # flip buffer
    
        pygame.display.flip()

    # clean up

    pygame.quit()

if __name__ == "__main__":
    main()