# Galactic Invaders
# By Alexander Cleary
# Computing SAC #2

import pygame
import random

highScores = {}

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
        self.clock = pygame.time.Clock()
        self.tps = 30

        for i in range(0, 200):
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

            # Reset Screen
            screen.fill((0, 0, 0))

            # Draw Stars
            for i in range(0, len(self.stars)):
                if self.stars[i].y_coord > screen_height - 3:
                    self.stars[i].y_coord = 0
                else:
                    self.stars[i].tick()

            # Draw Player
            self.player.tick()

            # Refresh Screen
            pygame.display.flip()

        pygame.quit()


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


class Player:
    def __init__(self):
        self.lives = 0
        self.fighters = 1
        self.sizeMultiplier = 2.5
        self.height = 19 * self.sizeMultiplier
        self.width = 15 * self.sizeMultiplier

        self.x_coord = screen_width / 2 - self.width / 2
        self.y_coord = screen_height - 80
        self.shotsFired = 0
        self.hits = 0

        self.image = pygame.image.load('assets/player.png')
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


class Missile:
    def __init__(self):
        self.x_coord = 0
        self.y_coord = 0


myGame = Game()
myGame.run()
