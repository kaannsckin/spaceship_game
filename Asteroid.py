from Group import Group
import pygame 
from colors import Colors

#inheritance from Group class
class Asteroid(Group):
    #Constructor with more arguments
    def __init__(self, Asteroid_type, image, position_x, position_y, name="Asteroid", health=50, height=256, width=256, speed_x=10, speed_y=10, damage=10):
        #initialization of properties of the parent Group class
        super().__init__(image=image, position_x=position_x, position_y=position_y, name=name, health=health, height=height, width=width, speed_x=speed_x, speed_y=speed_y)
        #Asteroides have also type and damage properties
        self.Asteroid_type = Asteroid_type
        self.damage = damage


    def move_autonomously(self):
        #move left
        self.position_x=self.position_x-self.speed_x
        #if out of the screen
        if self.position_x<0:
            self.reset()

    def draw(self, screen):
        super().draw(screen)
        #draw also health
        #on the Group 
        pygame.draw.line(screen, Colors.GREEN_ALPHA, (int(self.position_x), int(self.position_y)), (int(self.position_x + (self.width*(self.health/self.MAX_HEALTH))), int(self.position_y)), 3)
     
    def __str__(self):
        #string returned from the parent constructor plus the new properties
        return super().__str__() + " Asteroid-type: {} Damage: {}".format(self.Asteroid_type, self.damage)

#inheritance from Asteroid class, name can be changed from the default one, Asteroid_type is fixed
class Pisces(Asteroid):
    def __init__(self, image, position_x, position_y, name="Pisces", health=40, height=256, width=256, speed_x=20, speed_y=20, damage=20):
        super().__init__(Asteroid_type="Pisces", image=image, position_x=position_x, position_y=position_y, name=name, health=health, height=height, width=width, speed_x=speed_x, speed_y=speed_y, damage=damage)

class Scorpion(Asteroid):
    def __init__(self, image, position_x, position_y, name="Scorpion", health=80, height=256, width=256, speed_x=10, speed_y=10, damage=30):
        super().__init__(Asteroid_type="Scorpion", image=image, position_x=position_x, position_y=position_y, name=name, health=health, height=height, width=width, speed_x=speed_x, speed_y=speed_y, damage=damage)

class Taurus(Asteroid):
    def __init__(self, image, position_x, position_y, name="Taurus", health=120, height=256, width=256, speed_x=8, speed_y=8, damage=50):
        super().__init__(Asteroid_type="Taurus", image=image, position_x=position_x, position_y=position_y, name=name, health=health, height=height, width=width, speed_x=speed_x, speed_y=speed_y, damage=damage)
