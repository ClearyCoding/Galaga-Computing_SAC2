# Galactic Invaders
# By Alexander Cleary
# Computing SAC #2

import pygame
import random

highScores = {}
sizeMultiplier = 2.5

# Initialize Pygame
pygame.init()
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Galaga - Computing 1/2 SAC #2")
pygame.mouse.set_visible(False)
window_icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(window_icon)


class Game:
    def __init__(self):
        self.level = 0
        self.player = Player()
        self.stars = []
        self.enemies = []
        self.clock = pygame.time.Clock()
        self.tps = 30

        for star in range(0, 200):
            self.stars.append(Star())

    def run(self):
        running = True
        while running:
            self.clock.tick(self.tps)

            # Check if quit button has been pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

            # Reset Screen
            screen.fill((0, 0, 0))

            # Draw Stars
            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick()

            # Draw Player
            self.player.tick()

            # Draw Missiles
            for missile in self.player.missiles:
                if missile.y_coord < 3:
                    self.player.missiles.remove(missile)
                else:
                    missile.tick()

            # Draw Enemies
            for enemy in self.enemies:
                enemy.tick()

            # Refresh Screen
            pygame.display.flip()

        pygame.quit()

    def spawn_enemies(self):
        key = [[3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8],
               [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
        for row in range(5):
            for column in range(10):
                if column in key[row]:
                    species = [2, 1, 1, 0, 0][row]
                    y_coord = 60 + (45 * row)
                    x_coord = 97.5 + (45 * column)

                    self.enemies.append(Enemy(species, x_coord, y_coord, self))


class Star:
    def __init__(self):
        self.x_coord = random.randint(0, screen_width)
        self.y_coord = random.randint(0, screen_height)
        self.colour = [random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)]
        self.display_colour = random.choice([True, False])
        self.tick_delay = random.randint(0, 4)

        self.image = pygame.Surface((3, 3))

    def tick(self):
        if self.y_coord < screen_height:
            self.y_coord += 10

        self.tick_delay += 1
        if self.tick_delay % 5 == 0:
            self.display_colour = not self.display_colour

        if self.display_colour:
            self.image.fill((self.colour[0], self.colour[1], self.colour[2]))
        else:
            self.image.fill((0, 0, 0))
        screen.blit(self.image, (self.x_coord, self.y_coord))

    def regenerate(self):
        self.y_coord = 0
        self.x_coord = random.randint(0, screen_width)


class Player:
    def __init__(self):
        self.lives = 3
        self.fighters = 10
        self.height = 15 * sizeMultiplier
        self.fighter_width = 15 * sizeMultiplier
        self.width = self.fighter_width * self.fighters

        self.x_coord = screen_width / 2 - self.width / 2
        self.y_coord = screen_height - 80
        self.shotsFired = 0
        self.hits = 0

        self.missiles = []
        self.firing_sound = pygame.mixer.Sound('assets/sounds/firing.mp3')

        self.image = pygame.image.load(['assets/player0a.png', 'assets/player0b.png', 'assets/player0c.png'][self.fighters - 1])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def tick(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-1)
        if keys[pygame.K_RIGHT]:
            self.move(1)
        screen.blit(self.image, (self.x_coord, self.y_coord))

    def move(self, direction):
        if direction == -1:
            if self.x_coord > 0 + 10 + self.width / 2:
                self.x_coord -= 8
        if direction == 1:
            if self.x_coord < screen_width - self.width - 10 - self.width / 2:
                self.x_coord += 8

    def shoot(self):
        if len(self.missiles) < 2 * self.fighters:
            self.firing_sound.play()
            for fighter in range(self.fighters):
                self.missiles.append(Missile(self.x_coord + self.fighter_width / 2 + fighter * self.fighter_width))


class Missile:
    def __init__(self, x_coord):
        self.x_coord = x_coord
        self.y_coord = screen_height - 80

        self.width = 3 * sizeMultiplier
        self.height = 8 * sizeMultiplier

        self.image = pygame.image.load('assets/missile.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def tick(self):
        if self.y_coord > 3:
            self.y_coord -= 30

        screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord))


class Enemy:
    def __init__(self, species=0, x_coord=screen_width/2, y_coord=60, game=None):
        self.species = species
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.game = game
        self.tick_delay = 0
        self.health = [1, 1, 2][self.species]
        self.death_sound = pygame.mixer.Sound(['assets/sounds/enemy_death_a.mp3', 'assets/sounds/enemy_death_b.mp3',
                                               'assets/sounds/enemy_death_c.mp3'][self.species])
        self.hurt_sound = pygame.mixer.Sound('assets/sounds/enemy_hurt.mp3')

        self.width = sizeMultiplier * [13, 13, 15][self.species]
        self.height = sizeMultiplier * [10, 10, 16][self.species]

        self.image = pygame.image.load(['assets/enemy0a.png', 'assets/enemy1a.png',
                                        ['assets/enemy2c.png', 'assets/enemy2a.png'][self.health - 1]][self.species])
        self.animated = False
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def tick(self):
        self.tick_delay += 1
        self.check_collision()
        if self.tick_delay % 15 == 0:
            self.animated = not self.animated

        if self.animated:
            self.image = pygame.image.load(['assets/enemy0b.png', 'assets/enemy1b.png',
                                            ['assets/enemy2d.png', 'assets/enemy2b.png'][self.health - 1]]
                                           [self.species])
        else:
            self.image = pygame.image.load(['assets/enemy0a.png', 'assets/enemy1a.png',
                                            ['assets/enemy2c.png', 'assets/enemy2a.png'][self.health - 1]]
                                           [self.species])

        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord))

    def check_collision(self):
        for missile in self.game.player.missiles:
            if (abs(self.x_coord - missile.x_coord) <
                    self.width / 2 + missile.width / 2 and abs(
                    self.y_coord - missile.y_coord) <
                    self.height / 2 + missile.height / 2):
                self.game.player.missiles.remove(missile)
                self.health -= 1
                if self.health <= 0:
                    self.death_sound.play()
                    if self in self.game.enemies:
                        self.game.enemies.remove(self)
                else:
                    self.hurt_sound.play()


myGame = Game()
myGame.spawn_enemies()
myGame.run()
