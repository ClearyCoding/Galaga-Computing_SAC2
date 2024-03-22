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
            for star in range(0, len(self.stars)):
                if self.stars[star].y_coord > screen_height - 3:
                    self.stars[star].regenerate()
                else:
                    self.stars[star].tick()

            # Draw Player
            self.player.tick()

            # Draw Missiles
            for missile in range(len(self.player.missiles) - 1, -1, -1):
                if self.player.missiles[missile].y_coord < 3:
                    del self.player.missiles[missile]
                else:
                    self.player.missiles[missile].tick()

            # Draw Enemies
            for enemy in range(len(self.enemies) - 1, -1, -1):
                for missile in range(len(self.player.missiles) - 1, -1, -1):
                    try:
                        if abs(self.enemies[enemy].x_coord - self.player.missiles[missile].x_coord) < self.enemies[
                                enemy].width / 2 + self.player.missiles[missile].width / 2 and abs(
                                self.enemies[enemy].y_coord - self.player.missiles[missile].y_coord) < self.enemies[
                                enemy].height / 2 + self.player.missiles[missile].height / 2:
                            del self.enemies[enemy]
                            del self.player.missiles[missile]
                    except IndexError:
                        continue

            for enemy in range(len(self.enemies)):
                self.enemies[enemy].tick()

            # Refresh Screen
            pygame.display.flip()

        pygame.quit()

    def spawn_enemies(self):
        for row in range(5):
            for column in range(10):
                species = [2, 1, 1, 0, 0][row]
                y_coord = 45 * (row + 2)
                x_coord = 50 * (column + 1)

                self.enemies.append(Enemy(species, x_coord, y_coord))


class Star:
    def __init__(self):
        self.x_coord = random.randint(0, screen_width)
        self.y_coord = random.randint(0, screen_height)
        self.colour = [random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)]
        self.display_colour = random.choice([True, False])
        self.tick_delay = random.randint(0, 4)

        self.image = pygame.Surface((3, 3))

    def tick(self):
        if self.y_coord < screen_height:
            self.y_coord += 7

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
        self.lives = 0
        self.fighters = 1
        self.height = 19 * sizeMultiplier
        self.width = 15 * sizeMultiplier

        self.x_coord = screen_width / 2 - self.width / 2
        self.y_coord = screen_height - 80
        self.shotsFired = 0
        self.hits = 0

        self.missiles = []
        self.firing_sound = pygame.mixer.Sound('assets/sounds/firing.mp3')

        self.image = pygame.image.load('assets/player1.png')
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
            if self.x_coord > 0 + 20:
                self.x_coord -= self.width / 3.5
        if direction == 1:
            if self.x_coord < screen_width - self.width - 20:
                self.x_coord += self.width / 3.5

    def shoot(self):
        self.firing_sound.play()
        self.missiles.append(Missile(self.x_coord + self.width / 2))


class Missile:
    def __init__(self, x_coord):
        self.x_coord = x_coord
        self.y_coord = screen_height - 100

        self.width = 3 * sizeMultiplier
        self.height = 8 * sizeMultiplier

        self.image = pygame.image.load('assets/missile.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def tick(self):
        if self.y_coord > 3:
            self.y_coord -= 7

        screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord))


class Enemy:
    def __init__(self, species=0, x_coord=screen_width/2, y_coord=60):
        self.species = species
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.tick_delay = 0

        self.width = sizeMultiplier * [13, 13, 15, 15][self.species]
        self.height = sizeMultiplier * [10, 10, 16, 16][self.species]

        self.image = pygame.image.load(['assets/enemy0a.png', 'assets/enemy1a.png',
                                        'assets/enemy2a.png', 'assets/enemy3a.png'][self.species])
        self.animated = False
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def tick(self):
        self.tick_delay += 1
        if self.tick_delay % 15 == 0:
            self.animated = not self.animated

        if self.animated:
            self.image = pygame.image.load(['assets/enemy0b.png', 'assets/enemy1b.png',
                                            'assets/enemy2b.png', 'assets/enemy3b.png'][self.species])
        else:
            self.image = pygame.image.load(['assets/enemy0a.png', 'assets/enemy1a.png',
                                            'assets/enemy2a.png', 'assets/enemy3a.png'][self.species])

        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord))


myGame = Game()
myGame.spawn_enemies()
myGame.run()
