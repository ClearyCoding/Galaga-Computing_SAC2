# Galactic Invaders
# By Alexander Cleary
# Computing SAC #2

import pygame
import random
import math

# The number of lives the player starts with
initial_lives = 3

def save_high_score():
    with open('high_score.txt', 'w') as high_score_file:
        high_score_file.write(str(high_score))


scores = {}
with open('high_score.txt', 'r') as file:
    high_score = int(file.read())
sizeMultiplier = 2.5
end_game = False

# Scores Where The Player Receives Extra Lives (First At, Second At, And Then Every)
life_bonus = [20000, 60000, 60000]

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
        self.player = Player(self, 1)
        self.stars = []
        self.enemies = []
        self.enemy_missiles = []
        self.explosions = []
        self.clock = pygame.time.Clock()
        self.tps = 30
        self.tick_delay = 0
        self.score_1up = 0
        self.score_2up = 0
        self.time_out = 0
        self.game_end = False
        self.menu_open = True

        self.start_sound = pygame.mixer.Sound('assets/sounds/start.mp3')
        self.stage_up_sound = pygame.mixer.Sound('assets/sounds/stage_up.mp3')
        self.game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.mp3')

        self.icon_lives = pygame.image.load('assets/gui/life.png')
        self.icon_lives = pygame.transform.scale(self.icon_lives, (13 * sizeMultiplier, 14 * sizeMultiplier))
        self.badge_sizes = [[7, 12], [7, 14], [13, 14], [15, 16], [15, 16], [15, 16]]
        for badge in range(len(self.badge_sizes)):
            for size in range(2):
                self.badge_sizes[badge][size] = round(self.badge_sizes[badge][size] * sizeMultiplier)
        self.icon_badge1 = pygame.image.load('assets/gui/badge1.png')
        self.icon_badge1 = pygame.transform.scale(self.icon_badge1, (self.badge_sizes[0][0], self.badge_sizes[0][1]))
        self.icon_badge5 = pygame.image.load('assets/gui/badge5.png')
        self.icon_badge5 = pygame.transform.scale(self.icon_badge5, (self.badge_sizes[1][0], self.badge_sizes[1][1]))
        self.icon_badge10 = pygame.image.load('assets/gui/badge10.png')
        self.icon_badge10 = pygame.transform.scale(self.icon_badge10, (self.badge_sizes[2][0], self.badge_sizes[2][1]))
        self.icon_badge20 = pygame.image.load('assets/gui/badge20.png')
        self.icon_badge20 = pygame.transform.scale(self.icon_badge20, (self.badge_sizes[3][0], self.badge_sizes[3][1]))
        self.icon_badge30 = pygame.image.load('assets/gui/badge30.png')
        self.icon_badge30 = pygame.transform.scale(self.icon_badge30, (self.badge_sizes[4][0], self.badge_sizes[4][1]))
        self.icon_badge50 = pygame.image.load('assets/gui/badge50.png')
        self.icon_badge50 = pygame.transform.scale(self.icon_badge50, (self.badge_sizes[5][0], self.badge_sizes[5][1]))
        self.gui_flash = True
        self.icon_1up = pygame.image.load('assets/gui/1up.png')
        self.icon_1up = pygame.transform.scale(self.icon_1up, (23 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_2up = pygame.image.load('assets/gui/2up.png')
        self.icon_2up = pygame.transform.scale(self.icon_2up, (23 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_high_score = pygame.image.load('assets/gui/high_score.png')
        self.icon_high_score = pygame.transform.scale(self.icon_high_score, (79 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_stage = pygame.image.load('assets/gui/stage.png')
        self.icon_stage = pygame.transform.scale(self.icon_stage, (38 * sizeMultiplier, 7 * sizeMultiplier))
        self.number_textures = [pygame.image.load(f'assets/font/{i}.png') for i in range(10)]
        for i in range(len(self.number_textures)):
            self.number_textures[i] = pygame.transform.scale(
                self.number_textures[i], (7 * sizeMultiplier, 7 * sizeMultiplier))
        self.blue_number_textures = [pygame.image.load(f'assets/font/{i}b.png') for i in range(10)]
        for i in range(len(self.blue_number_textures)):
            self.blue_number_textures[i] = pygame.transform.scale(
                self.blue_number_textures[i], (7 * sizeMultiplier, 7 * sizeMultiplier))
        self.yellow_number_textures = [pygame.image.load(f'assets/font/{i}y.png') for i in range(10)]
        for i in range(len(self.yellow_number_textures)):
            self.yellow_number_textures[i] = pygame.transform.scale(
                self.yellow_number_textures[i], (7 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_game_over = pygame.image.load('assets/gui/game_over.png')
        self.icon_game_over = pygame.transform.scale(self.icon_game_over, (67 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_results = pygame.image.load('assets/gui/results.png')
        self.icon_results = pygame.transform.scale(self.icon_results, (72 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_hits = pygame.image.load('assets/gui/hits.png')
        self.icon_hits = pygame.transform.scale(self.icon_hits, (128 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_shots = pygame.image.load('assets/gui/shots_fired.png')
        self.icon_shots = pygame.transform.scale(self.icon_shots, (128 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_accuracy = pygame.image.load('assets/gui/accuracy.png')
        self.icon_accuracy = pygame.transform.scale(self.icon_accuracy, (128 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_percentage = pygame.image.load('assets/gui/percentage.png')
        self.icon_percentage = pygame.transform.scale(self.icon_percentage, (7 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_decimal = pygame.image.load('assets/gui/decimal_point.png')
        self.icon_decimal = pygame.transform.scale(self.icon_decimal, (7 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_start = pygame.image.load('assets/gui/start.png')
        self.icon_start = pygame.transform.scale(self.icon_start, (37 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_ready = pygame.image.load('assets/gui/ready.png')
        self.icon_ready = pygame.transform.scale(self.icon_ready, (37 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_push_start = pygame.image.load('assets/gui/push_start.png')
        self.icon_push_start = pygame.transform.scale(self.icon_push_start, (135 * sizeMultiplier, 7 * sizeMultiplier))
        self.icon_first_bonus = pygame.image.load('assets/gui/bonus_1.png')
        self.icon_first_bonus = pygame.transform.scale(self.icon_first_bonus,
                                                       (208 * sizeMultiplier, 16 * sizeMultiplier))
        self.icon_second_bonus = pygame.image.load('assets/gui/bonus_2.png')
        self.icon_second_bonus = pygame.transform.scale(self.icon_second_bonus,
                                                        (208 * sizeMultiplier, 16 * sizeMultiplier))
        self.icon_third_bonus = pygame.image.load('assets/gui/bonus_3.png')
        self.icon_third_bonus = pygame.transform.scale(self.icon_third_bonus,
                                                       (208 * sizeMultiplier, 16 * sizeMultiplier))

        for star in range(0, 200):
            self.stars.append(Star())

    def start(self):
        while self.menu_open:
            self.clock.tick(self.tps)
            self.tick_delay += 1

            # Check if quit button has been pressed
            self.check_events(mode="menu")
            if end_game:
                return

            screen.fill((0, 0, 0))

            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick()

            self.tick_gui("limited")

            if self.gui_flash:
                screen.blit(self.icon_push_start,
                            ((screen_width - 135 * sizeMultiplier) / 2,
                             (screen_height - 7 * sizeMultiplier) / 2 - 32 * sizeMultiplier))
            screen.blit(self.icon_first_bonus,
                        ((screen_width - 208 * sizeMultiplier) / 2,
                         (screen_height - 16 * sizeMultiplier) / 2 + sizeMultiplier))
            screen.blit(self.icon_second_bonus,
                        ((screen_width - 208 * sizeMultiplier) / 2,
                         (screen_height - 16 * sizeMultiplier) / 2 + 32 * sizeMultiplier))
            screen.blit(self.icon_third_bonus,
                        ((screen_width - 208 * sizeMultiplier) / 2,
                         (screen_height - 16 * sizeMultiplier) / 2 + 64 * sizeMultiplier))

            pygame.display.flip()


        starting = True
        self.start_sound.play()
        while starting:
            self.clock.tick(self.tps)
            self.tick_delay += 1

            # Check if quit button has been pressed
            self.check_events()
            if end_game:
                return

            screen.fill((0, 0, 0))

            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick(0)

            screen.blit(self.icon_start,
                        ((screen_width - 37 * sizeMultiplier) / 2, (screen_height - 7 * sizeMultiplier) / 2))
            self.tick_gui("starting")

            pygame.display.flip()

            if not pygame.mixer.get_busy():
                starting = False

        stage_time_out = 100
        start_stage = self.player.stage - 1
        stage_animation = True
        while stage_animation:
            self.clock.tick(self.tps)

            # Check if quit button has been pressed
            self.check_events()
            if end_game:
                return

            screen.fill((0, 0, 0))
            self.tick_delay += 1

            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick(0.01 * (100 - stage_time_out))

            self.tick_gui("stage_animation")

            self.player.tick()

            if 10 < stage_time_out <= 70:
                screen.blit(self.icon_stage,
                            (screen_width / 2 - (38 * sizeMultiplier + 4 * 8 * sizeMultiplier) / 2,
                             screen_height / 2 - 3.5 * sizeMultiplier))
                self.blit_score(start_stage,
                                screen_width / 2 - (38 * sizeMultiplier - 4 * 8 * sizeMultiplier) / 2
                                + 38 * sizeMultiplier - sizeMultiplier * 8 * len(str(start_stage)),
                                screen_height / 2 - 3.5 * sizeMultiplier, "blue")
            if stage_time_out == 55:
                self.stage_up_sound.play()
                start_stage += 1

            if stage_time_out <= 55:
                self.tick_gui()

            if stage_time_out > 0:
                stage_time_out -= 1

            pygame.display.flip()

            if stage_time_out == 1:
                self.spawn_enemies(False)
                stage_animation = False
        ready_time_out = 100
        while ready_time_out > 0:
            # Check if quit button has been pressed
            self.check_events()
            if end_game:
                return

            screen.fill((0, 0, 0))

            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick()

            # Draw Enemies
            for enemy in self.enemies:
                enemy.tick()

            self.player.tick()

            self.tick_gui("all")

            screen.blit(self.icon_ready,
                        ((screen_width - 37 * sizeMultiplier) / 2, (screen_height - 7 * sizeMultiplier) / 2))

            pygame.display.flip()
            ready_time_out -= 1

        for enemy in self.enemies:
            enemy.ticking = True

        self.run()

    def run(self):
        global high_score
        running = True
        while running:
            self.clock.tick(self.tps)
            self.tick_delay += 1

            # Check if quit button has been pressed
            self.check_events(True)
            if end_game:
                return

            # Reset Screen
            screen.fill((0, 0, 0))

            # Draw Stars
            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick()

            # New Stage Animations
            if self.player.stage > 255:
                self.player.stage = 255
            if 10 < self.time_out <= 70:
                screen.blit(self.icon_stage,
                            (screen_width / 2 - (38 * sizeMultiplier + 4 * 8 * sizeMultiplier) / 2,
                             screen_height / 2 - 3.5 * sizeMultiplier))
                self.blit_score(self.player.stage,
                                screen_width / 2 - (38 * sizeMultiplier - 4 * 8 * sizeMultiplier) / 2
                                + 38 * sizeMultiplier - sizeMultiplier * 8 * len(str(self.player.stage)),
                                screen_height / 2 - 3.5 * sizeMultiplier, "blue")
            if self.time_out == 55:
                self.stage_up_sound.play()
                self.player.stage += 1
            if self.time_out == 1:
                self.spawn_enemies()
            if self.time_out == 0:
                if len(self.enemies) == 0:  # Checks if stage progression is needed
                    self.time_out = 100
            if self.time_out > 0:
                self.time_out -= 1

            # Update Scores
            if self.player.score > 999999:
                self.player.score = 999999
            if self.player.player_number == 1:
                self.score_1up = self.player.score
            elif self.player.player_number == 2:
                self.score_2up = self.player.score

            if self.player.score > high_score:
                high_score = self.player.score
                save_high_score()

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

            # Draw GUI
            self.tick_gui(mode="all")

            # End Game If Player Dies
            if self.player.life < 1 and self.player.timeout < 200:
                self.game_end = True

            if self.game_end:
                self.player.ticking = False
                screen.blit(self.icon_game_over,
                            ((screen_width - 67 * sizeMultiplier) / 2, (screen_height - 7 * sizeMultiplier) / 2))
                if self.player.timeout < 100:
                    running = False

            # Refresh Screen
            pygame.display.flip()

        self.game_over()

    def spawn_enemies(self, ticking=True):
        key = [[3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8],
               [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
        for row in range(5):
            for column in range(10):
                if column in key[row]:
                    species = [2, 1, 1, 0, 0][row]
                    y_coord = 100 + (45 * row)
                    x_coord = 97.5 + (45 * column)

                    self.enemies.append(Enemy(species, x_coord, y_coord, self, ticking))

    def check_events(self, missiles=False, mode="normal"):
        global end_game
        # Check if quit button has been pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end_game = True

                # Shoot Button
                if event.key == pygame.K_SPACE and missiles:
                    if self.player.ticking:
                        self.player.shoot()

                if event.key == pygame.K_RETURN and mode == "menu":
                    self.menu_open = False

    def tick_gui(self, mode="all"):
        global high_score

        if self.tick_delay % 15 == 0:
            self.gui_flash = not self.gui_flash

        if mode == "all" or mode == "stage_animation":
            for life in range(self.player.lives_remaining):
                if life >= 8:
                    break
                screen.blit(self.icon_lives, (10 + (life * (13 * sizeMultiplier + 10)), screen_height -
                                              14 * sizeMultiplier - 10))

        if mode == "all":
            margin_right = 10
            for i in range(math.floor(self.player.stage / 50)):
                screen.blit(self.icon_badge50, (screen_width - margin_right - self.badge_sizes[5][0],
                                                screen_height - 10 - self.badge_sizes[5][1]))
                margin_right += self.badge_sizes[5][0] + 3
            for i in range(math.floor(self.player.stage % 50 / 30)):
                screen.blit(self.icon_badge30, (screen_width - margin_right - self.badge_sizes[4][0],
                                                screen_height - 10 - self.badge_sizes[4][1]))
                margin_right += self.badge_sizes[4][0] + 3
            for i in range(math.floor(self.player.stage % 50 % 30 / 20)):
                screen.blit(self.icon_badge20, (screen_width - margin_right - self.badge_sizes[3][0],
                                                screen_height - 10 - self.badge_sizes[3][1]))
                margin_right += self.badge_sizes[3][0] + 3
            for i in range(math.floor(self.player.stage % 50 % 30 % 20 / 10)):
                screen.blit(self.icon_badge10, (screen_width - margin_right - self.badge_sizes[2][0],
                                                screen_height - 10 - self.badge_sizes[2][1]))
                margin_right += self.badge_sizes[2][0] + 3
            for i in range(math.floor(self.player.stage % 50 % 30 % 20 % 10 / 5)):
                screen.blit(self.icon_badge5, (screen_width - margin_right - self.badge_sizes[1][0],
                                               screen_height - 10 - self.badge_sizes[1][1]))
                margin_right += self.badge_sizes[1][0] + 3
            for i in range(math.floor(self.player.stage % 50 % 30 % 20 % 10 % 5)):
                screen.blit(self.icon_badge1, (screen_width - margin_right - self.badge_sizes[0][0],
                                               screen_height - 10 - self.badge_sizes[0][1]))
                margin_right += self.badge_sizes[0][0] + 3

        if mode == "starting":
            for life in range(self.player.life):
                if life >= 8:
                    break
                screen.blit(self.icon_lives, (10 + (life * (13 * sizeMultiplier + 10)), screen_height -
                                              14 * sizeMultiplier - 10))

        if self.player.player_number == 1:
            if self.gui_flash or mode == "limited":
                screen.blit(self.icon_1up, (30 + (48 * sizeMultiplier - 23 * sizeMultiplier) / 2, 10))
            if self.players == 2:
                screen.blit(self.icon_2up,
                            (screen_width - 23 * sizeMultiplier -
                             (30 + (48 * sizeMultiplier - 23 * sizeMultiplier) / 2), 10))
        elif self.player.player_number == 2:
            screen.blit(self.icon_1up,
                        (30 + (48 * sizeMultiplier - 23 * sizeMultiplier) / 2, 10))
            if self.gui_flash or mode == "limited":
                screen.blit(self.icon_2up,
                            (screen_width - 23 * sizeMultiplier -
                             (30 + (48 * sizeMultiplier - 23 * sizeMultiplier) / 2), 10))
        screen.blit(self.icon_high_score, (screen_width / 2 - (39.5 * sizeMultiplier), 10))

        self.blit_score(
            self.score_1up, 30 + sizeMultiplier * 8 * (6 - len(str(self.score_1up))), 10 + 8 * sizeMultiplier)
        if self.players == 2 or self.player.player_number == 2:
            self.blit_score(
                self.score_2up, screen_width - 30 - sizeMultiplier * 8 * len(str(self.score_2up)),
                10 + 8 * sizeMultiplier)
        self.blit_score(high_score, screen_width / 2 + sizeMultiplier * 8 * (3 - len(str(high_score))),
                        10 + 8 * sizeMultiplier)

    def blit_score(self, score, x_coord, y_coord, colour="white", skip=False):
        score_str = str(score)
        if len(score_str) == 1 and not skip:
            score_str = "0" + score_str
            x_coord -= 8 * sizeMultiplier
        for i, digit in enumerate(score_str):
            if colour == "white":
                screen.blit(self.number_textures[int(digit)], (x_coord + i * 8 * sizeMultiplier, y_coord))
            elif colour == "blue":
                screen.blit(self.blue_number_textures[int(digit)], (x_coord + i * 8 * sizeMultiplier, y_coord))
            elif colour == "yellow":
                screen.blit(self.yellow_number_textures[int(digit)], (x_coord + i * 8 * sizeMultiplier, y_coord))

    def game_over(self):
        self.player.ticking = False
        self.game_over_sound.play()
        game_over_loop = True
        while game_over_loop:
            self.clock.tick(self.tps)

            # Check if quit button has been pressed
            self.check_events()
            if end_game:
                return

            # Reset Screen
            screen.fill((0, 0, 0))

            # Star Field
            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick()

            # Scores GUI
            self.tick_gui(mode="limited")

            # Results GUI
            screen.blit(self.icon_results,
                        ((screen_width - 72 * sizeMultiplier) / 2,
                         (screen_height - 7 * sizeMultiplier) / 2 - 21 * sizeMultiplier))

            screen.blit(self.icon_shots,
                        (((screen_width - 128 * sizeMultiplier) - 7 * 8 * sizeMultiplier) / 2,
                         (screen_height - 7 * sizeMultiplier) / 2))
            self.blit_score(self.player.shotsFired,
                            ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                            + (5 - len(str(self.player.shotsFired))) * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height - 7 * sizeMultiplier) / 2, "yellow")

            screen.blit(self.icon_hits,
                        (((screen_width - 128 * sizeMultiplier) - 7 * 8 * sizeMultiplier) / 2,
                         (screen_height + 7 * sizeMultiplier) / 2 + 14 * sizeMultiplier))
            self.blit_score(self.player.hits,
                            ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                            + (5 - len(str(self.player.hits))) * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height + 7 * sizeMultiplier) / 2 + 14 * sizeMultiplier, "yellow")

            screen.blit(self.icon_accuracy,
                        (((screen_width - 128 * sizeMultiplier) - 7 * 8 * sizeMultiplier) / 2,
                         (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier))
            if self.player.shotsFired != 0:
                accuracy = 100 / self.player.shotsFired * self.player.hits
            else:
                accuracy = 0
            accuracy_decimal = accuracy * 10 % 10
            accuracy = round(accuracy)
            self.blit_score(accuracy,
                            ((screen_width - 128 * sizeMultiplier) - 6 * 8 * sizeMultiplier) / 2
                            + (4 - len(str(accuracy))) * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier, "yellow")
            self.blit_score(round(accuracy_decimal),
                            ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                            + 3 * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier, "yellow", True)
            screen.blit(self.icon_decimal,
                        (((screen_width - 128 * sizeMultiplier) - 6 * 8 * sizeMultiplier) / 2
                         + 4 * 8 * sizeMultiplier + 128 * sizeMultiplier,
                         (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier))
            screen.blit(self.icon_percentage,
                        (((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                            + 4 * 8 * sizeMultiplier + 128 * sizeMultiplier,
                         (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier))

            # Update Screen
            pygame.display.flip()

            if not pygame.mixer.get_busy():
                game_over_loop = False


class Star:
    def __init__(self):
        self.x_coord = random.randint(0, screen_width)
        self.y_coord = random.randint(0, screen_height)
        self.colour = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
        self.display_colour = random.choice([True, False])
        self.tick_delay = random.randint(0, 4)
        self.velocity = random.randint(2, 8)

        self.image = pygame.Surface((3, 3))

    def tick(self, speed=float(1)):
        if self.y_coord < screen_height:
            self.y_coord += self.velocity * speed

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
        self.life = initial_lives
        self.lives_remaining = self.life - 1
        self.stage = 1
        self.player_number = player_number
        self.score = 0
        self.fighters = 1
        self.upgrades_reached = 0
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
        self.respawn_sound = pygame.mixer.Sound('assets/sounds/respawn_player.mp3')

        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (self.fighter_width, self.height))

    def tick(self):
        global life_bonus
        self.tick_delay += 1
        self.width = self.fighter_width * self.fighters

        if self.score >= life_bonus[0] and self.upgrades_reached == 0:
            self.upgrades_reached += 1
            self.life += 1

        if self.score >= life_bonus[1] + life_bonus[2] * (abs(self.upgrades_reached - 1)):
            self.upgrades_reached += 1
            self.life += 1

        if self.ticking:
            self.lives_remaining = self.life - 1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.move(-1)
            if keys[pygame.K_RIGHT]:
                self.move(1)
            self.check_collision()
            for fighter in range(self.fighters):
                screen.blit(self.image, (self.x_coord + self.fighter_width * fighter, self.y_coord - self.height / 2))
        else:
            if self.timeout == 220:
                if self.life > 0:
                    self.respawn_sound.play()
            if self.timeout < 120 and self.life >= 1:
                self.lives_remaining = self.life - 1
                if self.tick_delay % 10 == 0:
                    self.respawning = not self.respawning
                if self.respawning:
                    for fighter in range(self.fighters):
                        screen.blit(self.image,
                                    (self.x_coord + self.fighter_width * fighter, self.y_coord - self.height / 2))
            if self.timeout < 1:
                self.respawn_sound.stop()
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
                self.shotsFired += 1

    def check_collision(self):
        for missile in self.game.enemy_missiles:
            if (abs(self.x_coord + self.width / 2 - missile.x_coord) <
                    self.width / 2 + missile.width / 2 and abs(
                        self.y_coord - missile.y_coord) <
                    self.height / 2 + missile.height / 2):
                self.game.enemy_missiles.remove(missile)
                if self.fighters <= 1:
                    self.die()
                else:
                    self.death_sound.play()
                    self.game.explosions.append(Explosion(
                        missile.x_coord, self.y_coord + self.height / 2, "player", self.game))
                    self.add_fighters(-1)

    def die(self):
        self.ticking = False
        self.life -= 1
        self.death_sound.play()
        self.game.explosions.append(Explosion(
            self.x_coord + self.width, self.y_coord + self.height / 2, "player", self.game))
        self.timeout = 250

    def add_fighters(self, operator=1):
        self.fighters += operator
        self.x_coord -= operator * (self.fighter_width / 2)


class Missile:
    def __init__(self, x_coord, y_coord, team="player", game=None):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.team = team
        self.game = game
        self.ticking = True

        self.width = 3 * sizeMultiplier
        self.height = 8 * sizeMultiplier

        if self.team == "player":
            self.image = pygame.image.load('assets/missile_player.png')
        elif self.team == "enemy":
            self.image = pygame.image.load('assets/missile_enemy.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def tick(self):
        if self.ticking:
            self.check_collision()
            if self.y_coord > 3:
                if self.team == "player":
                    self.y_coord -= 30
                elif self.team == "enemy":
                    self.y_coord += 30

            screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord - self.height / 2))

    def check_collision(self):
        if self.team == "player":
            for enemy in self.game.enemies:
                if (abs(self.x_coord - enemy.x_coord) <
                        self.width / 2 + enemy.width / 2 and abs(
                            self.y_coord - enemy.y_coord) <
                        self.height / 2 + enemy.height / 2):
                    self.ticking = False
                    enemy.health -= 1
                    self.game.player.hits += 1
                    if enemy.health <= 0:
                        enemy.die()
                    else:
                        enemy.hurt_sound.play()
                    self.game.player.missiles.remove(self)
            for missile in self.game.enemy_missiles:
                if (abs(self.x_coord - missile.x_coord) <
                        self.width / 2 + missile.width / 2 and abs(
                            self.y_coord - missile.y_coord) <
                        self.height / 2 + missile.height / 2):
                    self.ticking = False
                    missile.ticking = False
                    self.game.player.hits += 1
                    self.game.explosions.append(Explosion(
                        self.x_coord + self.width / 2, self.y_coord + self.height / 2, "enemy", self.game))
                    self.game.enemy_missiles.remove(missile)
                    try:
                        self.game.player.missiles.remove(self)
                    except ValueError:
                        continue


class Enemy:
    def __init__(self, species=0, x_coord=screen_width / 2, y_coord=60, game=None, ticking=True):
        self.species = species
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.game = game
        self.diving = False
        self.ticking = ticking
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
        if random.randint(1, 1000) == 1 and self.game.player.ticking and self.ticking:
            self.shoot()
        screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord - self.height / 2))

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
myGame.start()
