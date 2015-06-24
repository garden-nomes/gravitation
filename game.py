import pygame
from pygame import display, mouse, key, event

from world import World

# constants

WIDTH = 1440
HEIGHT = 900

def main():

    # initialize pygame

    pygame.init()
    
    # initialize screen
    
    info = display.Info()
    screenSize = (info.current_w, info.current_h)
    
    screen = display.set_mode(screenSize, pygame.FULLSCREEN)
    mouse.set_visible(False)

    # initialize game world
    
    world = World(screen)

    # begin main game loop

    done = False
    while not done:
    
        # check for program exit signal
    
        for e in event.get():
            if e.type == pygame.QUIT:
                done = True

        # check for input
        
        keys = key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            done = True
    
        # update game
        
        world.update()
        
        # render game
        
        world.draw()
    
        # flip buffer
    
        display.flip()

    # clean up

    pygame.quit()

if __name__ == "__main__":
    main()