import pygame
from pygame import display, mouse, key, event, time, font
from world import World

# constants

FRAME_RATE = 60
DISPLAY_FPS = True

def main():

    # initialize pygame

    pygame.init()
    
    # initialize screen
    
    info = display.Info()
    screenSize = (info.current_w, info.current_h)
    
    screen = display.set_mode(screenSize, pygame.FULLSCREEN)
    mouse.set_visible(False)

    # intialize clock

    clock = time.Clock()

    infoFont = font.Font(font.match_font('arial'), 24)

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
        
        world.update(clock.tick())
        
        # render game
        
        world.draw()

        # draw fps

        if DISPLAY_FPS:
            text = infoFont.render(str(int(round(clock.get_fps()))), True, (255, 255, 255))
            position = (screen.get_width() / 2 - text.get_width() / 2, 32)
            screen.blit(text, position)
        
        # flip buffer
    
        display.flip()

    # clean up

    pygame.quit()

if __name__ == "__main__":
    main()
