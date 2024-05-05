import pygame
import os

class Background():
    #Constructor 
    def __init__(self, image, width, height, speed = 0):
        self.width = width
        self.height = height
        self.speed = speed
        #creates surface, loading image, and creating a faster copy considering transparency (alpha)
        self.surface = pygame.image.load(os.path.join('img', image)).convert_alpha()
        #scale to desired size
        self.surface = pygame.transform.smoothscale(self.surface, (self.width, self.height))
        #rectangle
        self.rect = self.surface.get_rect()

    def move(self):
        self.rect.move_ip(-self.speed,0)
        #if position is out of the screen 
        if self.rect[0]<-self.width: 
            self.rect[0]=0

    def draw(self, screen):
        #draw itself on screen
        screen.blit(self.surface, self.rect)
     
    def __str__(self):
        return "Background Image: {}".format(self.surface)




class ScrollingBackground(Background):
    #Constructor 
    def __init__(self, image, width, height, speed = 1):
        super().__init__(image, width, height, speed)
    
    def draw(self, screen):
        #draw itself on screen
        screen.blit(self.surface, self.rect)
        #draw a copy on the position "itself moved on right its width"
        screen.blit(self.surface, self.rect.move(self.width,0))
