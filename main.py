# Galactic Invaders
# By Alexander Cleary
# Computing SAC #2

import pygame

highScores = {}

# Initialize Pygame
pygame.init()
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Galactic Invaders")
pygame.mouse.set_visible(False)
window_icon = pygame.image.load('assets/player.png')
pygame.display.set_icon(window_icon)


class Game:
    def __init__(self):
        self.level = 0
        self.player = Player()
        self.clock = pygame.time.Clock()
        self.tps = 30

    def run(self):
        running = True
        while running:
            self.clock.tick(self.tps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            self.player.tick()
            pygame.display.flip()

        self.finish()

    def finish(self):
        pygame.quit()


class Player:
    def __init__(self):
        self.lives = 0
        self.fighters = 1
        self.size = 50

        self.xCoord = screen_width / 2 - self.size / 2
        self.yCoord = screen_height - 80
        self.shotsFired = 0
        self.hits = 0

        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def tick(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-1)
        if keys[pygame.K_RIGHT]:
            self.move(1)
        screen.blit(self.image, (self.xCoord, self.yCoord))

    def move(self, direction):
        if direction == -1:
            if self.xCoord > 0 + 20:
                self.xCoord -= self.size / 4
        if direction == 1:
            if self.xCoord < screen_width - self.size - 20:
                self.xCoord += self.size / 4


myGame = Game()
myGame.run()
