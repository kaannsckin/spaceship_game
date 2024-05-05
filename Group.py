import pygame
import os

class Group(pygame.sprite.Sprite):
    def __init__(self, image, position_x, position_y, name="Group", health=100, height=256, width=256, speed_x=1, speed_y=1):
        super().__init__() 
        self.image = image
        self.position_x = position_x
        self.position_y = position_y
        self.name = name
        self.health = health
        self.MAX_HEALTH = health
        self.height = height
        self.width = width
        self.speed_x = speed_x
        self.speed_y = speed_y
        #save the initial creation position
        self.initial_pos_x = position_x
        self.initial_pos_y = position_y

        #creates surface, loading image, and creating a faster copy considering transparency (alpha)
        self.Group_surface = pygame.image.load(os.path.join('img', self.image)).convert_alpha()
        #scale to desired size
        self.Group_surface = pygame.transform.smoothscale(self.Group_surface, (self.width, self.height))
        #get rectangle around for collision detection es:<rect(0, 0, 60, 60)>
        #has to be called "rect"
        self.rect = self.Group_surface.get_rect()
        #move the rectangle to the current position of the obj
        self.rect.update(self.position_x, self.position_y,self.width, self.height)
        #print(self.rect) 

    def update_rect(self):
        self.rect.update(self.position_x, self.position_y,self.width, self.height)


    def draw(self, screen):
        #draw itself on screen
        screen.blit(self.Group_surface, (self.position_x,self.position_y))

    def get_position(self):
        return (self.position_x, self.position_y)

    def set_position(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    #MOVEMENT 
    #moves the Group, player or enemy to a direction, within the screen
    def up(self):
        self.position_y = self.position_y - self.speed_y
        if self.position_y<0:
            self.position_y=0

    def down(self):
        self.position_y = self.position_y + self.speed_y
        if self.position_y>pygame.display.get_window_size()[1]-self.height:
            self.position_y=pygame.display.get_window_size()[1]-self.height

    def left(self):
         self.position_x = self.position_x - self.speed_x
         if self.position_x<0:
            self.position_x=0

    def right(self):
        self.position_x = self.position_x + self.speed_x
        if self.position_x>pygame.display.get_window_size()[0]-self.width:
            self.position_x=pygame.display.get_window_size()[0]-self.width

    def move_autonomously(self):
        print("move_autonomously not implemented")
        #to be overridden

    def lose_health(self, loss, reset_at_death=True):
        self.health = self.health - loss
        if not self.is_alive():
            self.kill()
            if reset_at_death:
                self.reset()
        return self.is_alive()

    def gain_health(self, gain):
        self.health = self.health + gain
        if self.health > 100:
            self.health = 100

    def reset(self):
        self.health = self.MAX_HEALTH
        #move back to initial position
        self.position_x = self.initial_pos_x
        self.position_y = self.initial_pos_y

    def kill(self):
        self.health=0
        return "Group killed"

    def is_alive(self):
        return self.health > 0
       
    #to print the object
    def __str__(self):
    	return "Group named '{}' at: {},{} Health: {} Speed: {},{}".format(self.name, self.position_x, self.position_y, self.health, self.speed_x, self.speed_y)
