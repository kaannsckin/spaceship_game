import pygame
from Group import Group
from colors import Colors
import time
import os

#inheritance from Group class
class Apollon(Group):
    """ The player """
    #Constructor 
    def __init__(self, image, position_x, position_y, name="Apollon", health=100, height=256, width=256, speed_x=1, speed_y=1):
        #initialization of properties of the parent Group class
        super().__init__(image=image, position_x=position_x, position_y=position_y, name=name, health=health, height=height, width=width, speed_x=speed_x, speed_y=speed_y)
        self.score = 0
        self.protected_till = 0 # moment till which the player is protected
        #load bubble 
        self.bubble_surface = pygame.image.load(os.path.join('img', "bubble.png")).convert_alpha()
        #scale to desired size
        self.bubble_surface = pygame.transform.smoothscale(self.bubble_surface, (self.width, self.height))

    def move_autonomously(self):
        #player doesn't need to move autonomously cause it's controlled by events
        pass

    def set_protected_sec(self, seconds):
        self.protected_till = time.time()+seconds

    def is_protected(self):
        now = time.time()
        return now < self.protected_till

    def gain_score(self, score_gained):
        self.score = self.score+score_gained
        return self.score

    def reset(self):
        self.score=0
        super().reset()

    #override lose health
    def lose_health(self, loss, reset_at_death=False):
        if not self.is_protected():
            super().lose_health(loss, reset_at_death)


    def draw(self, screen):
        super().draw(screen)
        if self.is_protected():
            screen.blit(self.bubble_surface, (self.position_x,self.position_y))
        #draw also health
        #bar on the Group 
        #pygame.draw.line(screen, Colors.GREEN, (int(self.position_x), int(self.position_y)), (int(self.position_x + (self.width*(self.health/self.MAX_HEALTH))), int(self.position_y)), 3)
        #bar on the screen
        window_size=pygame.display.get_window_size()[0]
        health_x1 = window_size/2
        health_y1 = 15
        health_x2 = window_size/6
        health_y2 = 15
        pygame.draw.line(screen, Colors.BLACK, (health_x1 , health_y1), (int(health_x2), health_y2), 20)
        pygame.draw.line(screen, Colors.GREEN, (health_x1 , health_y1), (int(health_x1 - ((health_x1-health_x2)*(self.health/self.MAX_HEALTH))), health_y2), 20)
        # health font
        font = pygame.font.SysFont(None, 24)
        health_surface = font.render(f"Health: {self.health}", True, Colors.WHITE)
        screen.blit(health_surface, (health_x2+30,10))
