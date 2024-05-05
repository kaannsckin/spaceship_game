#IMPORTS
import sys, os
import random
import pygame
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
)
from colors import Colors
from Apollon import Apollon
from Bullet import *
from Asteroid import *
from Booster import *
from Background import Background

class Game():
    """main Game"""
    def __init__(self):
        #MACROS
        self.SIZE = self.WIDTH, self.HEIGHT = 1280, 720
        self.PLAYER_SIZE = 100
        self.PLAYER_SPEED = 5
        self.BULLET_SIZE = 40
        self.ROCKET_SIZE = 50
        self.BULLET_SPEED = 5
        self.BULLET_NUMBER = 3
        self.ENEMY_SIZE = 30
        self.Scorpion_SIZE = 50
        self.Taurus_SIZE = 80
        self.ENEMY_SPEED = 4
        self.ENEMY_NUMBER = 5
        self.POWERUP_SIZE = 50
        self.POWERUP_SPEED = 5

        #initialize modules
        pygame.mixer.pre_init(44100, 32, 2, 4096)
        pygame.init()
        self.clock = pygame.time.Clock()

        #music play
        if pygame.mixer:
            music_path = os.path.join('sounds', "bgm.wav")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1) #-1 reapeat

        #create a graphical window 
        self.screen = pygame.display.set_mode(self.SIZE)
        #caption
        pygame.display.set_caption("ApollON Fire")
        #icon
        icon = pygame.image.load(os.path.join('img', 'Apollon.png')).convert_alpha()
        icon = pygame.transform.smoothscale(icon, (64, 64))
        pygame.display.set_icon(icon)

        #fonts
        self.font = pygame.font.SysFont(None, 24)
        self.font_big = pygame.font.SysFont(None, 64)

        #create background
        self.background = Background(image="bg.png", width=self.WIDTH, height=self.HEIGHT)
        self.backgr_particles = Background(image="particles_red.png", width=self.WIDTH, height=self.HEIGHT, speed=2)

        print("\t #### CREATING GAME ELEMENTS ####")
        #create game_elements group
        self.game_elements_group = pygame.sprite.Group()

        #create player
        self.player = Apollon('Apollon.png', position_x=20, position_y=20, height=self.PLAYER_SIZE, width=self.PLAYER_SIZE, speed_x=self.PLAYER_SPEED, speed_y=self.PLAYER_SPEED)
        self.game_elements_group.add(self.player)


        #create bullets
        self.bullets_and_rocket_group = pygame.sprite.Group()
        self.r = Rocket("Rocket.png", position_x=self.WIDTH/2+80+self.ROCKET_SIZE, position_y=5, height=self.ROCKET_SIZE, width=self.ROCKET_SIZE, speed_x=2, speed_y=2)
        self.bullets_and_rocket_group.add(self.r)
        self.game_elements_group.add(self.r)
        self.bullets_group = pygame.sprite.Group()
        for num_bullet in range(self.BULLET_NUMBER):
            b = Laser("Apollon.png", position_x=self.WIDTH/2+30+self.BULLET_SIZE*num_bullet, position_y=5, height=self.BULLET_SIZE, width=self.BULLET_SIZE, speed_x=self.BULLET_SPEED)
            self.bullets_group.add(b)
            self.bullets_and_rocket_group.add(b)
            self.game_elements_group.add(b)
            
        #create enemies
        self.enemies_group = pygame.sprite.Group()
        for num_enemy in range(self.ENEMY_NUMBER):
            pi_enemy = Pisces(image="Asteroid.png", position_x=random.randint(self.WIDTH, 2*self.WIDTH), position_y=random.randint(4, self.HEIGHT-self.ENEMY_SIZE), height=self.ENEMY_SIZE, width=self.ENEMY_SIZE, speed_x=self.ENEMY_SPEED)
            self.enemies_group.add(pi_enemy)
            self.game_elements_group.add(pi_enemy)

        sc_enemy = Scorpion(image="Asteroid2.png", position_x=random.randint(2*self.WIDTH, 3*self.WIDTH), position_y=random.randint(4, self.HEIGHT-self.Scorpion_SIZE), height=self.Scorpion_SIZE, width=self.Scorpion_SIZE, speed_x=4)
        self.enemies_group.add(sc_enemy)
        self.game_elements_group.add(sc_enemy)

        ta_enemy = Taurus(image="Asteroid3.png", position_x=random.randint(3*self.WIDTH, 4*self.WIDTH), position_y=random.randint(4, self.HEIGHT-self.Taurus_SIZE), height=self.Taurus_SIZE, width=self.Taurus_SIZE, speed_x=2)
        self.enemies_group.add(ta_enemy)
        self.game_elements_group.add(ta_enemy)

        #create powerups
        self.powerup_group = pygame.sprite.Group()
        saturn_image = Saturn(image="Saturn.png", position_x=random.randint(6*self.WIDTH, 8*self.WIDTH), position_y=random.randint(4, self.HEIGHT-self.POWERUP_SIZE), height=self.POWERUP_SIZE, width=self.POWERUP_SIZE, speed_x=self.POWERUP_SPEED)
        self.powerup_group.add(saturn_image)
        self.game_elements_group.add(saturn_image)

        Bloody_Moon = BloodyMoon(image="BloodyMoon.png", position_x=random.randint(4*self.WIDTH, 6*self.WIDTH), position_y=random.randint(4, self.HEIGHT-self.POWERUP_SIZE), height=self.POWERUP_SIZE, width=self.POWERUP_SIZE, speed_x=self.POWERUP_SPEED)
        self.powerup_group.add(Bloody_Moon)
        self.game_elements_group.add(Bloody_Moon)

        print("\t #### GAME CREATED ####")
        for elem in self.game_elements_group:
            print(elem)

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                high_score = int(file.read())
        except FileNotFoundError:
            high_score = 0
        return high_score

    def save_high_score(self, high_score):
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

    def increase_difficulty(self, current_score):
        # Oyunun zorluğunu artırmak için kullanılacak fonksiyon
        if current_score >= 500 and len(self.enemies_group) < 2 * self.ENEMY_NUMBER:
            self.add_more_asteroids(2)

    def add_more_asteroids(self, count):
        # Belirtilen sayıda asteroid eklemek için kullanılacak bir fonksiyon
        for _ in range(count):
            new_asteroid = Pisces(image="Asteroid.png", position_x=random.randint(self.WIDTH, 2 * self.WIDTH),
                                  position_y=random.randint(4, self.HEIGHT - self.ENEMY_SIZE),
                                  height=self.ENEMY_SIZE, width=self.ENEMY_SIZE, speed_x=self.ENEMY_SPEED)
            self.enemies_group.add(new_asteroid)
            self.game_elements_group.add(new_asteroid)
    def pause(self):
        font = pygame.font.Font(None, 74)
        pause_text = font.render("Paused", True, Colors.WHITE)
        resume_text = font.render("Press 'P' to Resume", True, Colors.WHITE)

        self.screen.blit(pause_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50))
        self.screen.blit(resume_text, (self.WIDTH // 2 - 250, self.HEIGHT // 2 + 50))
        pygame.display.flip()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
        self.screen.fill((0, 0, 0))

    def run(self):
        print("\t #### GAME RUNNING ####")
        high_score = self.load_high_score()
        asteroid_spawn_timer = 0  # Asteroid(en basit olan için btw) spawn timer
        asteroid_spawn_interval = 120  # spawn interval(60 frames = 1 sn)

        while 1:
            self.clock.tick(60)  # FPS

            # update high score if needed
            if self.player.score > high_score:
                high_score = self.player.score
                self.save_high_score(high_score)

            # increase difficulty based on the current score
            self.increase_difficulty(self.player.score)

            # EVENTS (get input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                    # closing game
                    self.reset()
                    self.close()

                # event triggered only on key press
                if event.type == pygame.KEYDOWN:
                    player_pos = self.player.get_position()
                    # KEY is B (shoot) or SPACE
                    if event.key == pygame.K_b or event.key == pygame.K_SPACE:
                        for b in self.bullets_group:
                            if b.is_ready():
                                b.fire(player_pos[0] + self.PLAYER_SIZE, player_pos[1] + (self.PLAYER_SIZE - self.BULLET_SIZE) / 2)
                                break
                    # KEY is X (launch rocket)
                    if event.key == pygame.K_x:
                        if self.r.is_ready():
                            self.r.fire(player_pos[0] + self.PLAYER_SIZE, player_pos[1] + (self.PLAYER_SIZE - self.BULLET_SIZE) / 2)
                            break
                    if event.key == pygame.K_p:
                        self.pause()

            # get keyboard state to understand the keys kept pressed
            keyboardstate = pygame.key.get_pressed()
            if keyboardstate[K_RIGHT]:
                self.player.right()
            if keyboardstate[K_LEFT]:
                self.player.left()
            if keyboardstate[K_UP]:
                self.player.up()
            if keyboardstate[K_DOWN]:
                self.player.down()

            # MOVE (update)
            for elem in self.game_elements_group:
                elem.move_autonomously()

            # COLLISION DETECTION
            # update rectangle position for every game object
            for elem in self.game_elements_group:
                elem.update_rect()

            # check collisions player vs enemies
            enemy_collided_player = pygame.sprite.spritecollideany(self.player, self.enemies_group)
            if enemy_collided_player:
                print("Player hit. Health loss: {}".format(enemy_collided_player.damage))
                self.player.lose_health(enemy_collided_player.damage)
                self.player.gain_score(enemy_collided_player.MAX_HEALTH)
                enemy_collided_player.reset()

            # check collisions bullets vs enemies
            collisions_bull_enem = pygame.sprite.groupcollide(self.bullets_and_rocket_group, self.enemies_group, False, False)
            for bullet in collisions_bull_enem:
                for enemy in collisions_bull_enem[bullet]:
                    print("Enemy hit. Health loss: {}".format(bullet.damage))
                    enemy.lose_health(bullet.damage)
                    self.player.gain_score(bullet.damage)
                    bullet.reset()

            # check collisions bullets vs powerups
            collisions_bull_powerup = pygame.sprite.groupcollide(self.bullets_and_rocket_group, self.powerup_group, False, False)
            for bullet in collisions_bull_powerup:
                for powerup in collisions_bull_powerup[bullet]:
                    print("Powerup hit. Health loss: {}".format(bullet.damage))
                    powerup.lose_health(bullet.damage)
                    bullet.reset()

            # check collisions player vs powerup
            powerup_collided_player = pygame.sprite.spritecollideany(self.player, self.powerup_group)
            if powerup_collided_player:
                print("Powerup collected: health increase {} protection time: {}".format(powerup_collided_player.health_increase, powerup_collided_player.collision_protection_time))
                self.player.gain_health(powerup_collided_player.health_increase)
                self.player.set_protected_sec(powerup_collided_player.collision_protection_time)
                powerup_collided_player.reset()

            # check health
            if not self.player.is_alive():
                print("Player Dead")
                self.reset()

            # draw background
            self.background.move()
            self.background.draw(self.screen)
            # draw background particles
            self.backgr_particles.move()
            self.backgr_particles.draw(self.screen)
            # draw score
            score_surface = self.font.render(f"Score: {self.player.score}", True, Colors.WHITE)
            self.screen.blit(score_surface, (32, 10))
            # draw High score
            high_score_surface = self.font.render(f"High Score: {high_score}", True, Colors.WHITE)
            self.screen.blit(high_score_surface, (32, 40))
            # draw game_elements_group on self.screen
            for elem in self.game_elements_group:
                elem.draw(self.screen)

            # Asteroid spawn kontrolü
            asteroid_spawn_timer += 1
            if asteroid_spawn_timer >= asteroid_spawn_interval:
                self.add_more_asteroids(1)
                asteroid_spawn_timer = 0

            # makes everything we have drawn on the Screen
            pygame.display.flip()


    def reset(self):
        if pygame.mixer:
            pygame.mixer.music.fadeout(1000)
        #draw game over
        gameover_surface = self.font_big.render(f"GAME OVER", True, Colors.RED)
        gameover_rect = gameover_surface.get_rect(center=(self.WIDTH/2, self.HEIGHT/3))
        score_surface = self.font.render(f"Score: {self.player.score}", True, Colors.WHITE)
        score_rect = score_surface.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))
        fadeout = pygame.Surface(self.SIZE).convert()
        fadeout.fill(Colors.BLACK)
        for i in range(90):
            pygame.time.delay(25)
            self.screen.blit(gameover_surface, gameover_rect)
            self.screen.blit(score_surface, score_rect)
            fadeout.set_alpha(i)
            self.screen.blit(fadeout, (0, 0))
            pygame.display.update()
        print("Resetting")
        for elem in self.game_elements_group:
                elem.reset()
        pygame.mixer.music.play(-1) #-1 reapeat

    def close(self):
        print("Closing")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
