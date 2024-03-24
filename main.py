# Galactic Invaders
# By Alexander Cleary
# Computing SAC #2

import pygame
import random
import math

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
        self.players = 1
        self.player = Player(self)
        self.stars = []
        self.enemies = []
        self.enemy_missiles = []
        self.explosions = []
        self.clock = pygame.time.Clock()
        self.tps = 30
        self.tick_delay = 0

        self.icon_lives = pygame.image.load('assets/player.png')
        self.badge_sizes = [[7, 12], [7, 14], [13, 14], [15, 16], [15, 16], [15, 16]]
        for badge in range(len(self.badge_sizes)):
            for size in range(2):
                self.badge_sizes[badge][size] = round(self.badge_sizes[badge][size] * sizeMultiplier)
        self.icon_badge1 = pygame.image.load('assets/badge1.png')
        self.icon_badge1 = pygame.transform.scale(self.icon_badge1, (self.badge_sizes[0][0], self.badge_sizes[0][1]))
        self.icon_badge5 = pygame.image.load('assets/badge5.png')
        self.icon_badge5 = pygame.transform.scale(self.icon_badge5, (self.badge_sizes[1][0], self.badge_sizes[1][1]))
        self.icon_badge10 = pygame.image.load('assets/badge10.png')
        self.icon_badge10 = pygame.transform.scale(self.icon_badge10, (self.badge_sizes[2][0], self.badge_sizes[2][1]))
        self.icon_badge20 = pygame.image.load('assets/badge20.png')
        self.icon_badge20 = pygame.transform.scale(self.icon_badge20, (self.badge_sizes[3][0], self.badge_sizes[3][1]))
        self.icon_badge30 = pygame.image.load('assets/badge30.png')
        self.icon_badge30 = pygame.transform.scale(self.icon_badge30, (self.badge_sizes[4][0], self.badge_sizes[4][1]))
        self.icon_badge50 = pygame.image.load('assets/badge50.png')
        self.icon_badge50 = pygame.transform.scale(self.icon_badge50, (self.badge_sizes[5][0], self.badge_sizes[5][1]))
        self.gui_flash = True
        self.icon_1up = pygame.image.load('assets/1up.png')
        self.icon_1up = pygame.transform.scale(self.icon_1up, (23 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_2up = pygame.image.load('assets/2up.png')
        self.icon_2up = pygame.transform.scale(self.icon_2up, (23 * sizeMultiplier, 7 * sizeMultiplier))

        for star in range(0, 200):
            self.stars.append(Star())

    def run(self):
        running = True
        while running:
            self.clock.tick(self.tps)
            self.tick_delay += 1

            # Check if quit button has been pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        if self.player.ticking:
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
                if missile.y_coord < 3 or missile.y_coord > screen_height:
                    self.player.missiles.remove(missile)
                else:
                    missile.tick()
            for missile in self.enemy_missiles:
                if missile.y_coord < 3 or missile.y_coord > screen_height:
                    self.enemy_missiles.remove(missile)
                else:
                    missile.tick()

            # Draw Enemies
            for enemy in self.enemies:
                enemy.tick()

            for explosion in self.explosions:
                explosion.tick()

            self.tick_gui()

            # End Game If Player Dies
            if self.player.life < 1 and self.player.timeout < 60:
                running = False

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
                    y_coord = 80 + (45 * row)
                    x_coord = 97.5 + (45 * column)

                    self.enemies.append(Enemy(species, x_coord, y_coord, self))

    def tick_gui(self):
        if self.tick_delay % 15 == 0:
            self.gui_flash = not self.gui_flash

        for life in range(self.player.lives_remaining):
            self.icon_lives = pygame.transform.scale(self.icon_lives, (13 * sizeMultiplier, 14 * sizeMultiplier))
            screen.blit(self.icon_lives, (10 + (life * (13 * sizeMultiplier + 10)), screen_height -
                                          14 * sizeMultiplier - 10))

        margin_right = 10
        for i in range(math.floor(self.player.level / 50)):
            screen.blit(self.icon_badge50, (screen_width - margin_right - self.badge_sizes[5][0],
                                            screen_height - 10 - self.badge_sizes[5][1]))
            margin_right += self.badge_sizes[5][0] + 3
        for i in range(math.floor(self.player.level % 50 / 30)):
            screen.blit(self.icon_badge30, (screen_width - margin_right - self.badge_sizes[4][0],
                                            screen_height - 10 - self.badge_sizes[4][1]))
            margin_right += self.badge_sizes[4][0] + 3
        for i in range(math.floor(self.player.level % 50 % 30 / 20)):
            screen.blit(self.icon_badge20, (screen_width - margin_right - self.badge_sizes[3][0],
                                            screen_height - 10 - self.badge_sizes[3][1]))
            margin_right += self.badge_sizes[3][0] + 3
        for i in range(math.floor(self.player.level % 50 % 30 % 20 / 10)):
            screen.blit(self.icon_badge10, (screen_width - margin_right - self.badge_sizes[2][0],
                                            screen_height - 10 - self.badge_sizes[2][1]))
            margin_right += self.badge_sizes[2][0] + 3
        for i in range(math.floor(self.player.level % 50 % 30 % 20 % 10 / 5)):
            screen.blit(self.icon_badge5, (screen_width - margin_right - self.badge_sizes[1][0],
                                           screen_height - 10 - self.badge_sizes[1][1]))
            margin_right += self.badge_sizes[1][0] + 3
        for i in range(math.floor(self.player.level % 50 % 30 % 20 % 10 % 5)):
            screen.blit(self.icon_badge1, (screen_width - margin_right - self.badge_sizes[0][0],
                                           screen_height - 10 - self.badge_sizes[0][1]))
            margin_right += self.badge_sizes[0][0] + 3

        if self.player.player_number == 1:
            if self.gui_flash:
                screen.blit(self.icon_1up, (30, 10))
            if self.players == 2:
                screen.blit(self.icon_2up, (screen_width - 30 - (23 * sizeMultiplier), 10))
        elif self.player.player_number == 2:
            screen.blit(self.icon_1up, (30, 10))
            if self.gui_flash:
                screen.blit(self.icon_2up, (screen_width - 30 - (23 * sizeMultiplier), 10))


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
    def __init__(self, game=None, player_number=1):
        self.life = 3
        self.lives_remaining = self.life - 1
        self.level = 1
        self.player_number = player_number
        self.score = 0
        self.fighters = 1
        self.height = 16 * sizeMultiplier
        self.fighter_width = 15 * sizeMultiplier
        self.width = self.fighter_width * self.fighters
        self.game = game
        self.ticking = True
        self.timeout = 60
        self.tick_delay = 0
        self.respawning = False

        self.x_coord = screen_width / 2 - self.width / 2
        self.y_coord = screen_height - 80
        self.shotsFired = 0
        self.hits = 0

        self.missiles = []
        self.firing_sound = pygame.mixer.Sound('assets/sounds/firing.mp3')
        self.death_sound = pygame.mixer.Sound('assets/sounds/death_player.mp3')

        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (self.fighter_width, self.height))

    def tick(self):
        self.tick_delay += 1
        if self.ticking:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.move(-1)
            if keys[pygame.K_RIGHT]:
                self.move(1)
            self.check_collision()
            for fighter in range(self.fighters):
                screen.blit(self.image, (self.x_coord + self.fighter_width * fighter, self.y_coord - self.height / 2))
        else:
            if self.timeout < 60 and self.life >= 1:
                self.lives_remaining = self.life - 1
                if self.tick_delay % 10 == 0:
                    self.respawning = not self.respawning
                if self.respawning:
                    for fighter in range(self.fighters):
                        screen.blit(self.image,
                                    (self.x_coord + self.fighter_width * fighter, self.y_coord - self.height / 2))
            if self.timeout < 1:
                self.ticking = True
            else:
                self.timeout -= 1
                self.x_coord = screen_width / 2 - self.width / 2

    def move(self, direction):
        if direction == -1:
            if self.x_coord > 0 + 10:
                self.x_coord -= 8
        if direction == 1:
            if self.x_coord < screen_width - self.width - 10:
                self.x_coord += 8

    def shoot(self):
        if len(self.missiles) < 2 * self.fighters:
            self.firing_sound.play()
            for fighter in range(self.fighters):
                self.missiles.append(Missile(self.x_coord + self.fighter_width / 2 + fighter * self.fighter_width,
                                             self.y_coord, "player", self.game))

    def check_collision(self):
        for missile in self.game.enemy_missiles:
            if (abs(self.x_coord + self.width / 2 - missile.x_coord) <
                    self.width / 2 + missile.width / 2 and abs(
                        self.y_coord - missile.y_coord) <
                    self.height / 2 + missile.height / 2):
                self.game.enemy_missiles.remove(missile)
                self.die()

    def die(self):
        self.ticking = False
        self.life -= 1
        self.death_sound.play()
        self.game.explosions.append(Explosion(
            self.x_coord + self.width, self.y_coord + self.height / 2, "player", self.game))
        self.timeout = 120

    def add_fighters(self, operator=1):
        self.fighters += operator
        self.x_coord -= operator * (self.fighter_width / 2)


class Missile:
    def __init__(self, x_coord, y_coord, team="player", game=None):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.team = team
        self.game = game

        self.width = 3 * sizeMultiplier
        self.height = 8 * sizeMultiplier

        if self.team == "player":
            self.image = pygame.image.load('assets/missile_player.png')
        elif self.team == "enemy":
            self.image = pygame.image.load('assets/missile_enemy.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def tick(self):
        if self.y_coord > 3:
            if self.team == "player":
                self.y_coord -= 30
            elif self.team == "enemy":
                self.y_coord += 30

        screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord - self.height / 2))


class Enemy:
    def __init__(self, species=0, x_coord=screen_width / 2, y_coord=60, game=None):
        self.species = species
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.game = game
        self.diving = False
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
                                            ['assets/enemy2b.png', 'assets/enemy2d.png'][self.health < 2]]
                                           [self.species])
        else:
            self.image = pygame.image.load(['assets/enemy0a.png', 'assets/enemy1a.png',
                                            ['assets/enemy2a.png', 'assets/enemy2c.png'][self.health < 2]]
                                           [self.species])

        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if random.randint(1, 1000) == 1 and self.game.player.ticking:
            self.shoot()
        screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord - self.height / 2))

    def check_collision(self):
        for missile in self.game.player.missiles:
            if (abs(self.x_coord - missile.x_coord) <
                    self.width / 2 + missile.width / 2 and abs(
                        self.y_coord - missile.y_coord) <
                    self.height / 2 + missile.height / 2):
                self.game.player.missiles.remove(missile)
                self.health -= 1
                if self.health <= 0:
                    self.die()
                else:
                    self.hurt_sound.play()

    def shoot(self):
        self.game.enemy_missiles.append(Missile(self.x_coord, self.y_coord, "enemy"))

    def die(self):
        self.game.player.score += [[50, 100], [80, 160], [150, 400]][self.species][self.diving]
        self.death_sound.play()
        self.game.explosions.append(Explosion(
            self.x_coord + self.width / 2, self.y_coord + self.height / 2, "enemy", self.game))
        if self in self.game.enemies:
            self.game.enemies.remove(self)


class Explosion:
    def __init__(self, x_coord, y_coord, target, game):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.game = game
        self.tick_delay = 0
        self.animation = 0
        self.target = target
        if self.target == "player":
            self.size = 64
            self.image = pygame.image.load('assets/player_explosion0.png')
            self.animation_speed = 6
            self.size_shift = 1.25
        elif self.target == "enemy":
            self.size = 32
            self.image = pygame.image.load('assets/explosion0.png')
            self.animation_speed = 3
            self.size_shift = 1

    def tick(self):
        self.tick_delay += 1
        self.animation = math.floor(self.tick_delay / self.animation_speed)
        if self.animation > 4:
            self.game.explosions.remove(self)
        else:
            if self.target == "player":
                self.image = pygame.image.load(
                    ['assets/player_explosion0.png', 'assets/player_explosion1.png', 'assets/player_explosion2.png',
                     'assets/player_explosion3.png', 'assets/player_explosion3.png']
                    [self.animation])
            elif self.target == "enemy":
                self.image = pygame.image.load(
                    ['assets/explosion0.png', 'assets/explosion1.png', 'assets/explosion2.png',
                     'assets/explosion3.png', 'assets/explosion4.png']
                    [self.animation])
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        screen.blit(self.image,
                    (self.x_coord - self.size / self.size_shift, self.y_coord - self.size / self.size_shift))


myGame = Game()
myGame.spawn_enemies()
myGame.run()
