from pygame import font

BASE_BRIGHTNESS = 0.0
FLASH_BRIGHTNESS = 255.0
FLASH_TIME = 1.0

TUTORIAL = "Collect 3 balls of the same color"
TUTORIAL_TIME = 5.0

class Text(object):
    def __init__(self, world):
        self.font = font.Font(font.match_font('arialblack'), 36)
        self.brightness = BASE_BRIGHTNESS
        self.world = world
        self.tutorial = False
        self.tutorialBrightness = BASE_BRIGHTNESS
        
    def update(self, millis):
        if self.brightness > BASE_BRIGHTNESS:
            self.brightness -= (FLASH_BRIGHTNESS - BASE_BRIGHTNESS) *  millis / (1000 * FLASH_TIME)
            if self.brightness < BASE_BRIGHTNESS: self.brightness = BASE_BRIGHTNESS
        
        if self.tutorial:
            self.tutorialBrightness -= (FLASH_BRIGHTNESS - BASE_BRIGHTNESS) * millis / (1000 * TUTORIAL_TIME)
            if self.tutorialBrightness < BASE_BRIGHTNESS: self.tutorialBrightness = BASE_BRIGHTNESS
    
    def draw(self, surface):
        if self.tutorial:
            text = self.font.render(TUTORIAL, True,
                                        (self.tutorialBrightness, self.tutorialBrightness, self.tutorialBrightness))
            position = (self.world.width / 2 - text.get_width() / 2, 36)
            surface.blit(text, position)

        text = self.font.render(str(self.world.player.maxChain), True, (self.brightness, self.brightness, self.brightness))
        position = (self.world.width / 2 - text.get_width() / 2, self.world.height - text.get_height() - 36)
        surface.blit(text, position)
    
    def flash(self):
        self.tutorial = False
        self.brightness = FLASH_BRIGHTNESS
    
    def showTutorial(self):
        self.flash()
        self.tutorial = True
        self.tutorialBrightness = FLASH_BRIGHTNESS
        