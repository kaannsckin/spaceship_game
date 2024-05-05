from Group import Group 

class Booster(Group):
    """ generic powerup """
    def __init__(self, booster_type, health_increase, collision_protection_time, image, position_x, position_y, name="Booster", health=50, height=256, width=256, speed_x=10, speed_y=10):
        #initialization of properties of the parent Group class
        super().__init__(image=image, position_x=position_x, position_y=position_y, name=name, health=health, height=height, width=width, speed_x=speed_x, speed_y=speed_y)
        #other
        self.booster_type = booster_type
        self.health_increase = health_increase
        self.collision_protection_time = collision_protection_time


    def move_autonomously(self):
        #move left
        self.position_x=self.position_x-self.speed_x
        #if out of the screen
        if self.position_x<0:
            self.reset()
    
    def draw(self, screen):
        super().draw(screen)
        #draw also health
     
    #to print the object
    def __str__(self):
        return super().__str__() + " Booster '{}' Increasing {} and Protecting for {}".format(self.booster_type, self.health_increase, self.collision_protection_time)
        
        

class Saturn(Booster):
    """ has more protection time than health increase"""
    def __init__(self, image, position_x, position_y, health_increase=10, collision_protection_time=10, name="Saturn", health=50, height=256, width=256, speed_x=10, speed_y=10):
        super().__init__(booster_type="Saturn", health_increase=health_increase, collision_protection_time=collision_protection_time, image=image, position_x=position_x, position_y=position_y, name=name, health=health, height=height, width=width, speed_x=speed_x, speed_y=speed_y)

class BloodyMoon(Booster):
    """ has more health increase """
    def __init__(self, image, position_x, position_y, health_increase=90, collision_protection_time=5, name="BloodyMoon", health=50, height=256, width=256, speed_x=10, speed_y=10):
        super().__init__(booster_type="BloodyMoon",  health_increase=health_increase, collision_protection_time=collision_protection_time, image=image, position_x=position_x, position_y=position_y, name=name, health=health, height=height, width=width, speed_x=speed_x, speed_y=speed_y)
        
