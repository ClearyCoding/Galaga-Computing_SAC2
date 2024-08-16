#!/usr/bin/env python3
#  Computing SAC2: Galaga Semi-Faithful Recreation by Alexander Cleary

import pygame
from random import randint, choice
from math import floor, sin
from os import path
from assets import arcadify

# THESE VARIABLES ARE TO BE EDITED BY MACHINE OPERATOR

# Fullscreen Mode
fullscreen = False
maximised = False

# Scores Where The Player Receives Extra Lives (First At, Second At, And Then Every)
life_bonus = [20000, 60000, 60000]

# Initial Lives Each Player Will Receive
initial_lives = 3

# Key Bindings
key_bindings = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,

    "shoot": pygame.K_SPACE,

    "select": pygame.K_RETURN,
    "quit": pygame.K_ESCAPE,
}

# END OPERATOR VARIABLES

# Terminates The Game When True
end_game = False

# Full Path To Assets Function
my_path = path.dirname(path.realpath(__file__))


def fetch(filename):
    return path.join(my_path, filename)


# Initialize Pygame
pygame.init()
infoObject = pygame.display.Info()
aspect_ratio = 7 / 9
if fullscreen:
    screen_width = infoObject.current_w
    screen_height = infoObject.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
else:
    if maximised:
        screen_height = infoObject.current_h
        screen_width = infoObject.current_w
        screen = pygame.display.set_mode((screen_width, screen_height))
    else:
        screen_height = infoObject.current_h * 0.85  # TODO: Screen Resizing
        screen_width = screen_height * aspect_ratio
        screen = pygame.display.set_mode((screen_width, screen_height))

sizeMultiplier = screen_height / 320

pygame.display.set_caption("Galaga - Computing 1/2 SAC #2")
pygame.mouse.set_visible(False)
window_icon = pygame.image.load(fetch('assets/icon.png'))
pygame.display.set_icon(window_icon)

# Arcadify Module Prints Text Onto Screen In Arcade Font. Find arcadify.py in assets.
arcadify = arcadify.Arcadify(screen, pygame)


class Game:
    def __init__(self):
        self.sounds = {
            'start': pygame.mixer.Sound(fetch('assets/sounds/start.wav')),
            'stage_up': pygame.mixer.Sound(fetch('assets/sounds/stage_up.wav')),
            'game_over': pygame.mixer.Sound(fetch('assets/sounds/game_over.wav')),
            'initials': pygame.mixer.Sound(fetch('assets/sounds/initials.wav')),
            'challenging': pygame.mixer.Sound(fetch('assets/sounds/challenging.wav')),
            'bonus': pygame.mixer.Sound(fetch('assets/sounds/challenging_music.wav')),

            'player_firing': pygame.mixer.Sound(fetch('assets/sounds/firing.wav')),
            'player_death': pygame.mixer.Sound(fetch('assets/sounds/death_player.wav')),
            'player_respawn': pygame.mixer.Sound(fetch('assets/sounds/respawn_player.wav')),
            'player_bonus_life': pygame.mixer.Sound(fetch('assets/sounds/bonus_life.wav')),

            'enemy_death_a': pygame.mixer.Sound(fetch('assets/sounds/enemy_death_a.wav')),
            'enemy_death_b': pygame.mixer.Sound(fetch('assets/sounds/enemy_death_b.wav')),
            'enemy_death_c': pygame.mixer.Sound(fetch('assets/sounds/enemy_death_c.wav')),
            'enemy_hurt': pygame.mixer.Sound(fetch('assets/sounds/enemy_hurt.wav')),
        }

        self.sprites = {
            'player': pygame.image.load(fetch('assets/sprites/player.png')),
            'missile_player': pygame.image.load(fetch('assets/sprites/missile_player.png')),
            'missile_enemy': pygame.image.load(fetch('assets/sprites/missile_enemy.png')),
            'player_explosion': [
                pygame.image.load(fetch('assets/sprites/player_explosion0.png')),
                pygame.image.load(fetch('assets/sprites/player_explosion1.png')),
                pygame.image.load(fetch('assets/sprites/player_explosion2.png')),
                pygame.image.load(fetch('assets/sprites/player_explosion3.png')),
                pygame.image.load(fetch('assets/sprites/player_explosion3.png')),
            ],
            'enemy_explosion': [
                pygame.image.load(fetch('assets/sprites/explosion0.png')),
                pygame.image.load(fetch('assets/sprites/explosion1.png')),
                pygame.image.load(fetch('assets/sprites/explosion2.png')),
                pygame.image.load(fetch('assets/sprites/explosion3.png')),
                pygame.image.load(fetch('assets/sprites/explosion4.png')),
            ],
            'enemy': {
                '0': {
                    '0': pygame.image.load(fetch('assets/sprites/enemy0/0.png')),
                    'animated': pygame.image.load(fetch('assets/sprites/enemy0/animated.png')),
                },
                '1': {
                    '0': pygame.image.load(fetch('assets/sprites/enemy1/0.png')),
                    'animated': pygame.image.load(fetch('assets/sprites/enemy1/animated.png')),
                },
                '2a': {
                    '0': pygame.image.load(fetch('assets/sprites/enemy2a/0.png')),
                    'animated': pygame.image.load(fetch('assets/sprites/enemy2a/animated.png')),
                },
                '2b': {
                    '0': pygame.image.load(fetch('assets/sprites/enemy2b/0.png')),
                    'animated': pygame.image.load(fetch('assets/sprites/enemy2b/animated.png')),
                },
            },
        }

        self.gui = {
            'lives': pygame.transform.scale(pygame.image.load(fetch('assets/gui/life.png')),
                                            (13 * sizeMultiplier, 14 * sizeMultiplier)),
            'badge1': pygame.transform.scale(pygame.image.load(fetch('assets/gui/badge1.png')),
                                             (7 * sizeMultiplier, 12 * sizeMultiplier)),
            'badge5': pygame.transform.scale(pygame.image.load(fetch('assets/gui/badge5.png')),
                                             (7 * sizeMultiplier, 14 * sizeMultiplier)),
            'badge10': pygame.transform.scale(pygame.image.load(fetch('assets/gui/badge10.png')),
                                              (13 * sizeMultiplier, 14 * sizeMultiplier)),
            'badge20': pygame.transform.scale(pygame.image.load(fetch('assets/gui/badge20.png')),
                                              (15 * sizeMultiplier, 16 * sizeMultiplier)),
            'badge30': pygame.transform.scale(pygame.image.load(fetch('assets/gui/badge30.png')),
                                              (15 * sizeMultiplier, 16 * sizeMultiplier)),
            'badge50': pygame.transform.scale(pygame.image.load(fetch('assets/gui/badge50.png')),
                                              (15 * sizeMultiplier, 16 * sizeMultiplier)),
            '1up': pygame.transform.scale(pygame.image.load(fetch('assets/gui/1up.png')),
                                          (23 * sizeMultiplier, 7 * sizeMultiplier)),
            '2up': pygame.transform.scale(pygame.image.load(fetch('assets/gui/2up.png')),
                                          (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'high_score': pygame.transform.scale(pygame.image.load(fetch('assets/gui/high_score.png')),
                                                 (79 * sizeMultiplier, 7 * sizeMultiplier)),
            'stage': pygame.transform.scale(pygame.image.load(fetch('assets/gui/stage.png')),
                                            (38 * sizeMultiplier, 7 * sizeMultiplier)),
            'game_over': pygame.transform.scale(pygame.image.load(fetch('assets/gui/game_over.png')),
                                                (67 * sizeMultiplier, 7 * sizeMultiplier)),
            'results': pygame.transform.scale(pygame.image.load(fetch('assets/gui/results.png')),
                                              (72 * sizeMultiplier, 7 * sizeMultiplier)),
            'hits': pygame.transform.scale(pygame.image.load(fetch('assets/gui/hits.png')),
                                           (128 * sizeMultiplier, 7 * sizeMultiplier)),
            'shots': pygame.transform.scale(pygame.image.load(fetch('assets/gui/shots_fired.png')),
                                            (128 * sizeMultiplier, 7 * sizeMultiplier)),
            'accuracy': pygame.transform.scale(pygame.image.load(fetch('assets/gui/accuracy.png')),
                                               (128 * sizeMultiplier, 7 * sizeMultiplier)),
            'underline': pygame.transform.scale(pygame.image.load(fetch('assets/gui/underline.png')),
                                                (7 * sizeMultiplier, 1 * sizeMultiplier)),
            'start': pygame.transform.scale(pygame.image.load(fetch('assets/gui/start.png')),
                                            (37 * sizeMultiplier, 7 * sizeMultiplier)),
            'player_1': pygame.transform.scale(pygame.image.load(fetch('assets/gui/player_1.png')),
                                               (58 * sizeMultiplier, 7 * sizeMultiplier)),
            'player_2': pygame.transform.scale(pygame.image.load(fetch('assets/gui/player_2.png')),
                                               (58 * sizeMultiplier, 7 * sizeMultiplier)),
            'ready': pygame.transform.scale(pygame.image.load(fetch('assets/gui/ready.png')),
                                            (37 * sizeMultiplier, 7 * sizeMultiplier)),
            'push_start': pygame.transform.scale(pygame.image.load(fetch('assets/gui/push_start.png')),
                                                 (135 * sizeMultiplier, 7 * sizeMultiplier)),
            'first_bonus': pygame.transform.scale(pygame.image.load(fetch('assets/gui/bonus_1.png')),
                                                  (208 * sizeMultiplier, 16 * sizeMultiplier)),
            'second_bonus': pygame.transform.scale(pygame.image.load(fetch('assets/gui/bonus_2.png')),
                                                   (208 * sizeMultiplier, 16 * sizeMultiplier)),
            'third_bonus': pygame.transform.scale(pygame.image.load(fetch('assets/gui/bonus_3.png')),
                                                  (208 * sizeMultiplier, 16 * sizeMultiplier)),
            'free_play': pygame.transform.scale(pygame.image.load(fetch('assets/gui/free_play.png')),
                                                (64 * sizeMultiplier, 7 * sizeMultiplier)),
            'initials': pygame.transform.scale(pygame.image.load(fetch('assets/gui/initials.png')),
                                               (164 * sizeMultiplier, 7 * sizeMultiplier)),
            'top': pygame.transform.scale(pygame.image.load(fetch('assets/gui/top.png')),
                                          (88 * sizeMultiplier, 7 * sizeMultiplier)),
            'score': pygame.transform.scale(pygame.image.load(fetch('assets/gui/score.png')),
                                            (39 * sizeMultiplier, 7 * sizeMultiplier)),
            'name': pygame.transform.scale(pygame.image.load(fetch('assets/gui/name.png')),
                                           (31 * sizeMultiplier, 7 * sizeMultiplier)),
            'first': pygame.transform.scale(pygame.image.load(fetch('assets/gui/1st.png')),
                                            (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'second': pygame.transform.scale(pygame.image.load(fetch('assets/gui/2nd.png')),
                                             (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'third': pygame.transform.scale(pygame.image.load(fetch('assets/gui/3rd.png')),
                                            (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'fourth': pygame.transform.scale(pygame.image.load(fetch('assets/gui/4th.png')),
                                             (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'fifth': pygame.transform.scale(pygame.image.load(fetch('assets/gui/5th.png')),
                                            (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'first_yellow': pygame.transform.scale(pygame.image.load(fetch('assets/gui/1st_yellow.png')),
                                                   (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'second_yellow': pygame.transform.scale(pygame.image.load(fetch('assets/gui/2nd_yellow.png')),
                                                    (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'third_yellow': pygame.transform.scale(pygame.image.load(fetch('assets/gui/3rd_yellow.png')),
                                                   (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'fourth_yellow': pygame.transform.scale(pygame.image.load(fetch('assets/gui/4th_yellow.png')),
                                                    (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'fifth_yellow': pygame.transform.scale(pygame.image.load(fetch('assets/gui/5th_yellow.png')),
                                                   (23 * sizeMultiplier, 7 * sizeMultiplier)),
            'heroes': pygame.transform.scale(pygame.image.load(fetch('assets/gui/galactic_heroes.png')),
                                             (150 * sizeMultiplier, 7 * sizeMultiplier)),
            'select_players': pygame.transform.scale(pygame.image.load(fetch('assets/gui/select_players.png')),
                                                     (108 * sizeMultiplier, 7 * sizeMultiplier)),
            '1_player': pygame.transform.scale(pygame.image.load(fetch('assets/gui/one_player.png')),
                                               (58 * sizeMultiplier, 7 * sizeMultiplier)),
            '2_players': pygame.transform.scale(pygame.image.load(fetch('assets/gui/two_players.png')),
                                                (66 * sizeMultiplier, 7 * sizeMultiplier)),
            'pointer': pygame.transform.scale(pygame.image.load(fetch('assets/gui/pointer.png')),
                                              (8 * sizeMultiplier, 7 * sizeMultiplier)),
            'challenging_stage': pygame.transform.scale(pygame.image.load(fetch('assets/gui/challenging_stage.png')),
                                                        (129 * sizeMultiplier, 7 * sizeMultiplier)),
            'challenging_perfect': pygame.transform.scale(pygame.image.load(fetch('assets/gui/challenge_perfect.png')),
                                                          (64 * sizeMultiplier, 7 * sizeMultiplier)),
            'challenging_bonus': pygame.transform.scale(pygame.image.load(fetch('assets/gui/challenge_bonus.png')),
                                                        (39 * sizeMultiplier, 7 * sizeMultiplier)),
            'challenging_special_bonus': pygame.transform.scale(pygame.image.load(
                fetch('assets/gui/challenge_special_bonus.png')),
                (100 * sizeMultiplier, 7 * sizeMultiplier)),
            'challenging_hits': pygame.transform.scale(pygame.image.load(fetch('assets/gui/challenge_hits.png')),
                                                       (111 * sizeMultiplier, 7 * sizeMultiplier)),
        }

        self.players = 1
        self.current_player = 1
        self.player1 = Player(self, 1)
        self.player2 = None
        self.player = self.player1
        self.stars = []
        for star in range(0, round(266 * (screen_width / screen_height))):
            self.stars.append(Star())
        self.explosions = []

        self.clock = pygame.time.Clock()
        self.tps = 30
        self.current_tick = 0
        self.score_1up = 0
        self.score_2up = 0
        self.time_out = 0
        self.menu_open = True
        self.save_score = False
        self.save_action = None
        self.high_score_flash = False
        self.running = False
        self.select_players = False
        self.last_interaction = 0
        self.gui_flash = True

        self.high_scores = {}
        try:
            with open('high_scores', 'r') as load_highScoreFile:
                for line in load_highScoreFile:
                    load_player, load_score = line.strip().split(':')
                    self.high_scores[load_player] = int(load_score)
                self.high_scores = {k: v for k, v in sorted(self.high_scores.items(),
                                                            key=lambda item: item[1], reverse=True)}
        except FileNotFoundError:
            with open('high_scores', 'w') as file:
                file.write("")

        if list(self.high_scores.values()):
            self.local_high_score = list(self.high_scores.values())[0]
        else:
            self.local_high_score = 0

    def save_high_score(self, player, score):
        if not self.high_scores.get(player) or self.high_scores[player] < score:
            self.high_scores[player] = score
        self.high_scores = {k: v for k, v in sorted(self.high_scores.items(), key=lambda item: item[1], reverse=True)}
        with open('high_scores', 'w') as save_highScoreFile:
            for save_player, save_score in self.high_scores.items():
                save_highScoreFile.write(f'{save_player}:{save_score}\n')

    def start(self):
        menu_position = 0
        while self.menu_open:
            self.clock.tick(self.tps)
            self.current_tick += 1

            # Check if quit button has been pressed
            self.check_events(mode="menu")
            if end_game:
                return

            if self.current_tick % 400 == 0:
                menu_position = (menu_position + 1) % 2

            screen.fill((0, 0, 0))

            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick()

            self.tick_gui("limited")

            if self.select_players:
                if self.current_tick - self.last_interaction > self.tps * 30:
                    self.players = 1
                    self.select_players = False

                screen.blit(self.gui['select_players'],
                            ((screen_width - 108 * sizeMultiplier) / 2,
                             (screen_height - 16 * sizeMultiplier) / 2 - 32 * sizeMultiplier))
                screen.blit(self.gui['1_player'],
                            ((screen_width - 82 * sizeMultiplier) / 2 + 16 * sizeMultiplier,
                             (screen_height - 16 * sizeMultiplier) / 2))
                screen.blit(self.gui['2_players'],
                            ((screen_width - 82 * sizeMultiplier) / 2 + 16 * sizeMultiplier,
                             (screen_height - 16 * sizeMultiplier) / 2 + 32 * sizeMultiplier))
                if self.players == 1:
                    screen.blit(self.gui['pointer'],
                                ((screen_width - 82 * sizeMultiplier) / 2,
                                 (screen_height - 16 * sizeMultiplier) / 2))
                elif self.players == 2:
                    screen.blit(self.gui['pointer'],
                                ((screen_width - 82 * sizeMultiplier) / 2,
                                 (screen_height - 16 * sizeMultiplier) / 2 + 32 * sizeMultiplier))
            else:
                if menu_position == 0:
                    screen.blit(self.gui['first_bonus'],
                                ((screen_width - 208 * sizeMultiplier) / 2,
                                 (screen_height - 16 * sizeMultiplier) / 2))
                    screen.blit(self.gui['second_bonus'],
                                ((screen_width - 208 * sizeMultiplier) / 2,
                                 (screen_height - 16 * sizeMultiplier) / 2 + 32 * sizeMultiplier))
                    screen.blit(self.gui['third_bonus'],
                                ((screen_width - 208 * sizeMultiplier) / 2,
                                 (screen_height - 16 * sizeMultiplier) / 2 + 64 * sizeMultiplier))
                    if -10 < life_bonus[0] < 10:
                        arcadify.render(life_bonus[0], (screen_width + 82 * sizeMultiplier) / 2,
                                        (screen_height - 8 * sizeMultiplier) / 2,
                                        "yellow", sizeMultiplier, 99999, 2)
                    else:
                        arcadify.render(life_bonus[0], (screen_width + 66 * sizeMultiplier) / 2,
                                        (screen_height - 8 * sizeMultiplier) / 2,
                                        "yellow", sizeMultiplier, 99999, 2)
                    if -10 < life_bonus[1] < 10:
                        arcadify.render(life_bonus[1], (screen_width + 82 * sizeMultiplier) / 2,
                                        (screen_height - 8 * sizeMultiplier) / 2 + 32 * sizeMultiplier,
                                        "yellow", sizeMultiplier, 99999, 2)
                    else:
                        arcadify.render(life_bonus[1], (screen_width + 66 * sizeMultiplier) / 2,
                                        (screen_height - 8 * sizeMultiplier) / 2 + 32 * sizeMultiplier,
                                        "yellow", sizeMultiplier, 99999, 2)
                    if -10 < life_bonus[2] < 10:
                        arcadify.render(life_bonus[2], (screen_width + 82 * sizeMultiplier) / 2,
                                        (screen_height - 8 * sizeMultiplier) / 2 + 64 * sizeMultiplier,
                                        "yellow", sizeMultiplier, 99999, 2)
                    else:
                        arcadify.render(life_bonus[2], (screen_width + 66 * sizeMultiplier) / 2,
                                        (screen_height - 8 * sizeMultiplier) / 2 + 64 * sizeMultiplier,
                                        "yellow", sizeMultiplier, 99999, 2)
                elif menu_position == 1:
                    screen.blit(self.gui['top'], ((screen_width - 88 * sizeMultiplier) / 2, screen_height / 2))
                    screen.blit(self.gui['heroes'], (screen_width / 2 - 75 * sizeMultiplier,
                                                     screen_height - 200 * sizeMultiplier))
                    screen.blit(self.gui['name'], (screen_width / 2 + 59 * sizeMultiplier, screen_height - 140 *
                                                   sizeMultiplier))
                    screen.blit(self.gui['score'], (screen_width / 2 - 55 * sizeMultiplier,
                                                    screen_height - 140 * sizeMultiplier))

                    for i, (name, score) in enumerate(self.high_scores.items()):
                        if i > 4:
                            break
                        screen.blit(
                            [self.gui['first'], self.gui['second'], self.gui['third'],
                             self.gui['fourth'], self.gui['fifth']][i],
                            (screen_width / 2 - 90 * sizeMultiplier, screen_height - (120 - i * 20) * sizeMultiplier))
                        arcadify.render(score,
                                        screen_width / 2 - 55 * sizeMultiplier
                                        + (6 - len(str(score))) * 8 * sizeMultiplier,
                                        screen_height - (120 - i * 20) * sizeMultiplier,
                                        "blue", sizeMultiplier, 999999, 2)
                        arcadify.render(name, screen_width / 2 + 66 * sizeMultiplier,
                                        screen_height - (120 - i * 20) * sizeMultiplier,
                                        "blue", sizeMultiplier)

                if self.gui_flash:
                    screen.blit(self.gui['push_start'],
                                ((screen_width - 135 * sizeMultiplier) / 2,
                                 screen_height / 4))
                screen.blit(self.gui['free_play'],
                            (5 * sizeMultiplier, screen_height - 2 * sizeMultiplier - 7 * sizeMultiplier))

            pygame.display.flip()

        self.select_players = False
        if self.players == 2 and not self.player2:
            self.player2 = Player(self, 2)
            self.player = [self.player1, self.player2][self.current_player - 1]

        starting = True
        self.sounds['start'].play()
        while starting:
            self.clock.tick(self.tps)
            self.current_tick += 1

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

            if self.player.score >= self.local_high_score:
                self.local_high_score = self.player.score
                self.high_score_flash = True
            else:
                self.high_score_flash = False

            screen.blit(self.gui['start'],
                        ((screen_width - 37 * sizeMultiplier) / 2,
                         (screen_height - 7 * sizeMultiplier) / 2 - 7 * sizeMultiplier))
            if self.player.player_number == 1:
                screen.blit(self.gui['player_1'],
                            ((screen_width - 58 * sizeMultiplier) / 2,
                             (screen_height - 7 * sizeMultiplier) / 2 + 7 * sizeMultiplier))
                self.tick_gui("starting")
            if self.player.player_number == 2:
                screen.blit(self.gui['player_2'],
                            ((screen_width - 58 * sizeMultiplier) / 2,
                             (screen_height - 7 * sizeMultiplier) / 2 + 7 * sizeMultiplier))
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
            self.current_tick += 1

            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick(0.01 * (100 - stage_time_out))

            self.player.tick()

            if 10 < stage_time_out <= 70:
                screen.blit(self.gui['stage'],
                            (screen_width / 2 - (38 * sizeMultiplier + 4 * 8 * sizeMultiplier) / 2,
                             screen_height / 2 - 3.5 * sizeMultiplier))
                arcadify.render(start_stage,
                                screen_width / 2 - (38 * sizeMultiplier - 4 * 8 * sizeMultiplier) / 2
                                + 38 * sizeMultiplier - sizeMultiplier * 8 * len(str(start_stage)),
                                screen_height / 2 - 3.5 * sizeMultiplier,
                                "blue", sizeMultiplier, 999999, 2)
            if stage_time_out == 55:
                self.sounds['stage_up'].play()
                start_stage += 1

            if stage_time_out <= 55:
                self.tick_gui()
            else:
                self.tick_gui("stage_animation")

            if stage_time_out > 0:
                stage_time_out -= 1

            pygame.display.flip()

            if stage_time_out == 1:
                self.spawn_enemies(False)
                stage_animation = False
        ready_time_out = 100
        while ready_time_out > 0:
            self.clock.tick(self.tps)
            self.current_tick += 1
            ready_time_out -= 1

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
            for enemy in self.player.enemies:
                enemy.tick()

            self.player.tick()

            self.tick_gui(mode="all")

            screen.blit(self.gui['ready'],
                        ((screen_width - 37 * sizeMultiplier) / 2, (screen_height - 7 * sizeMultiplier) / 2))

            pygame.display.flip()

        for enemy in self.player.enemies:
            enemy.ticking = True

        self.player.started = True
        self.run()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.tps)
            self.current_tick += 1

            # Check if quit button has been pressed
            self.check_events(True)
            if end_game:
                return

            if self.players == 2:
                self.player = [self.player1, self.player2][self.current_player - 1]
                if self.current_player == 2 and not self.player.started:
                    self.start()

            # Reset Screen
            screen.fill((0, 0, 0))

            # Draw Stars
            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick()

            # New Stage Animations
            if self.time_out == 350:
                self.sounds['bonus'].play()
            if 100 < self.time_out <= 330:
                screen.blit(self.gui['challenging_hits'],
                            (((screen_width - 128 * sizeMultiplier) - 7 * 8 * sizeMultiplier) / 2,
                             (screen_height - 7 * sizeMultiplier) / 2))
            if 100 < self.time_out <= 260:
                arcadify.render(self.player.challenge_hits,
                                ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                                + (5 - len(str(self.player.challenge_hits))) * 8 * sizeMultiplier
                                + 128 * sizeMultiplier,
                                ((screen_height - 7 * sizeMultiplier) / 2),
                                "blue", sizeMultiplier, 999999, 2)
                if self.player.challenge_hits >= 40:
                    screen.blit(self.gui['challenging_perfect'],
                                ((screen_width - 64 * sizeMultiplier) / 2,
                                 (screen_height - 7 * sizeMultiplier) / 2 - 16 * sizeMultiplier))
            if 100 < self.time_out <= 230:
                if self.player.challenge_hits >= 40:
                    screen.blit(self.gui['challenging_special_bonus'],
                                (((screen_width - 128 * sizeMultiplier) - 7 * 8 * sizeMultiplier) / 2,
                                 (screen_height - 7 * sizeMultiplier) / 2 + 16 * sizeMultiplier))
                else:
                    screen.blit(self.gui['challenging_bonus'],
                                ((screen_width - 39 * sizeMultiplier) / 2,
                                 (screen_height - 7 * sizeMultiplier) / 2 + 16 * sizeMultiplier))
            if self.time_out == 160:
                if self.player.challenge_hits >= 40:
                    self.player.score += 10000
                else:
                    self.player.score += self.player.challenge_hits * 100
            if 100 < self.time_out <= 160:
                if self.player.challenge_hits >= 40:
                    arcadify.render(10000,
                                    ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                                    + 128 * sizeMultiplier,
                                    ((screen_height - 7 * sizeMultiplier) / 2 + 16 * sizeMultiplier),
                                    "yellow", sizeMultiplier, 999999, 2)
                else:
                    arcadify.render(self.player.challenge_hits * 100,
                                    ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                                    + (5 - len(str(self.player.challenge_hits * 100))) * 8 * sizeMultiplier
                                    + 128 * sizeMultiplier,
                                    ((screen_height - 7 * sizeMultiplier) / 2 + 16 * sizeMultiplier),
                                    "blue", sizeMultiplier, 999999, 2)
            if self.time_out == 60 and self.player.challenging_stage:
                self.sounds['challenging'].play()
            if 10 < self.time_out <= 70:
                if self.player.challenging_stage:
                    screen.blit(self.gui['challenging_stage'],
                                ((screen_width - 129 * sizeMultiplier) / 2,
                                 (screen_height - 7 * sizeMultiplier) / 2))
                else:
                    screen.blit(self.gui['stage'],
                                (screen_width / 2 - (38 * sizeMultiplier + 4 * 8 * sizeMultiplier) / 2,
                                 screen_height / 2 - 3.5 * sizeMultiplier))
                    arcadify.render(self.player.stage,
                                    screen_width / 2 - (38 * sizeMultiplier - 4 * 8 * sizeMultiplier) / 2
                                    + 38 * sizeMultiplier - sizeMultiplier * 8 * len(str(self.player.stage)),
                                    screen_height / 2 - 3.5 * sizeMultiplier,
                                    "blue", sizeMultiplier, 999999, 2)
            if self.time_out == 55:
                if not self.player.challenging_stage:
                    self.sounds['stage_up'].play()
                self.player.stage = (self.player.stage + 1) % 256
            if self.time_out == 1:
                self.spawn_enemies()
            if self.time_out == 0:
                if len(self.player.enemies) == 0:  # Checks if stage progression is needed
                    self.player.enemies_in_formation = False
                    if self.player.challenging_stage:
                        self.time_out = 370
                    else:
                        self.time_out = 100
                    if (self.player.stage - 2) % 4 == 0:
                        self.player.challenging_stage = True
                        self.player.challenge_hits = 0
                    else:
                        self.player.challenging_stage = False
            if self.time_out > 0:
                self.time_out -= 1

            # Update Scores
            if self.player.player_number == 1:
                self.score_1up = self.player.score
            elif self.player.player_number == 2:
                self.score_2up = self.player.score

            if self.player.score >= self.local_high_score:
                self.local_high_score = self.player.score
                self.high_score_flash = True
            else:
                self.high_score_flash = False

            # Draw Player
            self.player.tick()

            # Draw Missiles
            for missile in self.player.missiles:
                if missile.y_coord < 3 or missile.y_coord > screen_height:
                    try:
                        self.player.missiles.remove(missile)
                    except ValueError:
                        continue
                else:
                    missile.tick()
            for missile in self.player.enemy_missiles:
                if missile.y_coord < 3 or missile.y_coord > screen_height:
                    try:
                        self.player.enemy_missiles.remove(missile)
                    except ValueError:
                        continue
                else:
                    missile.tick()

            # Draw Enemies
            for enemy in self.player.enemies:
                enemy.tick()

            for explosion in self.explosions:
                explosion.tick()

            # Draw GUI
            self.tick_gui(mode="all")

            # End Game If Player Dies
            if self.player.life < 1 and self.player.timeout < 200:
                self.player.ticking = False
                if self.players == 2:
                    screen.blit(self.gui['game_over'],
                                ((screen_width - 67 * sizeMultiplier) / 2,
                                 (screen_height - 7 * sizeMultiplier) / 2 - 7 * sizeMultiplier))
                    if self.player.player_number == 1:
                        screen.blit(self.gui['player_1'],
                                    ((screen_width - 58 * sizeMultiplier) / 2,
                                     (screen_height - 7 * sizeMultiplier) / 2 + 7 * sizeMultiplier))
                    if self.player.player_number == 2:
                        screen.blit(self.gui['player_2'],
                                    ((screen_width - 58 * sizeMultiplier) / 2,
                                     (screen_height - 7 * sizeMultiplier) / 2 + 7 * sizeMultiplier))
                else:
                    screen.blit(self.gui['game_over'],
                                ((screen_width - 67 * sizeMultiplier) / 2, (screen_height - 7 * sizeMultiplier) / 2))
                if self.player.timeout < 100 and not self.player.game_end:
                    self.player.game_end = True
                    self.save_score = False
                    self.game_over()

            # Refresh Screen
            if not self.player.game_end:
                pygame.display.flip()

    def spawn_enemies(self, ticking=True):
        key = [[-2, -1, 1, 2], [-4, -3, -2, -1, 1, 2, 3, 4], [-4, -3, -2, -1, 1, 2, 3, 4],
               [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]]
        for row in range(len(key)):
            for column in key[row]:
                self.player.enemies.append(Enemy(column, row, self, ticking))
        self.player.enemy_pulse = 1
        self.player.enemies_in_formation = True

    def check_events(self, missiles=False, mode="normal"):
        global end_game
        # Check if quit button has been pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.score_1up > 0:
                    self.save_high_score("???", self.score_1up)
                if self.score_2up > 0:
                    self.save_high_score("???", self.score_2up)
                end_game = True

            if event.type in {pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN}:
                self.last_interaction = self.current_tick

            if event.type == pygame.KEYDOWN:
                if event.key == key_bindings["quit"]:
                    if self.score_1up > 0:
                        self.save_high_score("???", self.score_1up)
                    if self.score_2up > 0:
                        self.save_high_score("???", self.score_2up)
                    end_game = True

                # Shoot Button
                if event.key == key_bindings["shoot"] and missiles:
                    if self.player.ticking:
                        self.player.shoot()

                if event.key == key_bindings["select"] and self.select_players:
                    self.menu_open = False
                if event.key == key_bindings["up"] and self.select_players and self.players == 2:
                    self.players = self.players % 2 + 1
                if event.key == key_bindings["down"] and self.select_players and self.players == 1:
                    self.players = self.players % 2 + 1

                if event.key == key_bindings["select"] and mode == "menu":
                    self.select_players = True
                if event.key == key_bindings["select"] and mode == "save":
                    self.save_score = True
                if event.key == key_bindings["up"] and mode == "save":
                    self.save_action = "up"
                if event.key == key_bindings["down"] and mode == "save":
                    self.save_action = "down"
                if event.key == key_bindings["left"] and mode == "save":
                    self.save_action = "left"
                if event.key == key_bindings["right"] and mode == "save":
                    self.save_action = "right"

    def tick_gui(self, mode="all"):
        if self.current_tick % 15 == 0:
            self.gui_flash = not self.gui_flash

        if mode == "all" or mode == "stage_animation" or mode == "starting":
            for life in range([self.player.lives_remaining, self.player.life][mode == "starting"]):
                if life >= 8:
                    break
                screen.blit(self.gui['lives'],
                            (4 * sizeMultiplier + (life * (13 * sizeMultiplier + 4 * sizeMultiplier)),
                             screen_height - 14 * sizeMultiplier - 4 * sizeMultiplier))

        if mode == "all":
            margin_right = 4 * sizeMultiplier
            for i in range(floor(self.player.stage / 50)):
                screen.blit(self.gui['badge50'], (screen_width - margin_right - 15 * sizeMultiplier,
                                                  screen_height - 4 * sizeMultiplier - 16 * sizeMultiplier))
                margin_right += 15 * sizeMultiplier + 1.2 * sizeMultiplier
            for i in range(floor(self.player.stage % 50 / 30)):
                screen.blit(self.gui['badge30'], (screen_width - margin_right - 15 * sizeMultiplier,
                                                  screen_height - 4 * sizeMultiplier - 16 * sizeMultiplier))
                margin_right += 15 * sizeMultiplier + 1.2 * sizeMultiplier
            for i in range(floor(self.player.stage % 50 % 30 / 20)):
                screen.blit(self.gui['badge20'], (screen_width - margin_right - 15 * sizeMultiplier,
                                                  screen_height - 4 * sizeMultiplier - 16 * sizeMultiplier))
                margin_right += 15 * sizeMultiplier + 1.2 * sizeMultiplier
            for i in range(floor(self.player.stage % 50 % 30 % 20 / 10)):
                screen.blit(self.gui['badge10'], (screen_width - margin_right - 13 * sizeMultiplier,
                                                  screen_height - 4 * sizeMultiplier - 14 * sizeMultiplier))
                margin_right += 13 * sizeMultiplier + 1.2 * sizeMultiplier
            for i in range(floor(self.player.stage % 50 % 30 % 20 % 10 / 5)):
                screen.blit(self.gui['badge5'], (screen_width - margin_right - 7 * sizeMultiplier,
                                                 screen_height - 4 * sizeMultiplier - 14 * sizeMultiplier))
                margin_right += 7 * sizeMultiplier + 1.2 * sizeMultiplier
            for i in range(floor(self.player.stage % 50 % 30 % 20 % 10 % 5)):
                screen.blit(self.gui['badge1'], (screen_width - margin_right - 7 * sizeMultiplier,
                                                 screen_height - 4 * sizeMultiplier - 12 * sizeMultiplier))
                margin_right += 7 * sizeMultiplier + 1.2 * sizeMultiplier

        if self.player.player_number == 1:
            if self.gui_flash or mode == "limited":
                screen.blit(self.gui['1up'], (12 * sizeMultiplier + (48 * sizeMultiplier - 23 * sizeMultiplier) / 2,
                                              4 * sizeMultiplier))
            if self.players == 2:
                screen.blit(self.gui['2up'],
                            (screen_width - 23 * sizeMultiplier -
                             (12 * sizeMultiplier + (48 * sizeMultiplier - 23 * sizeMultiplier) / 2),
                             4 * sizeMultiplier))
        elif self.player.player_number == 2:
            screen.blit(self.gui['1up'],
                        (12 * sizeMultiplier + (48 * sizeMultiplier - 23 * sizeMultiplier) / 2, 4 * sizeMultiplier))
            if self.gui_flash or mode == "limited":
                screen.blit(self.gui['2up'],
                            (screen_width - 23 * sizeMultiplier -
                             (12 * sizeMultiplier + (48 * sizeMultiplier - 23 * sizeMultiplier) / 2),
                             4 * sizeMultiplier))
        if not self.high_score_flash or self.gui_flash or mode == "limited" or self.local_high_score <= 0:
            screen.blit(self.gui['high_score'], (screen_width / 2 - (39.5 * sizeMultiplier), 4 * sizeMultiplier))

        arcadify.render(
            self.score_1up, 12 * sizeMultiplier + sizeMultiplier * 8 * (6 - len(str(self.score_1up))),
            4 * sizeMultiplier + 8 * sizeMultiplier, "white", sizeMultiplier, 999999, 2)
        if self.players == 2 or self.player.player_number == 2:
            arcadify.render(
                self.score_2up, screen_width - 12 * sizeMultiplier - sizeMultiplier * 8 * len(str(self.score_2up)),
                4 * sizeMultiplier + 8 * sizeMultiplier, "white", sizeMultiplier, 999999, 2)
        arcadify.render(self.local_high_score,
                        screen_width / 2 + sizeMultiplier * 8 * (3 - len(str(self.local_high_score))),
                        4 * sizeMultiplier + 8 * sizeMultiplier, "white", sizeMultiplier, 999999, 2)

    def game_over(self):
        self.player.ticking = False
        self.sounds['game_over'].play()
        game_over_loop = True
        while game_over_loop:
            self.clock.tick(self.tps)
            self.current_tick += 1

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

            # Results GUI
            screen.blit(self.gui['results'],
                        ((screen_width - 72 * sizeMultiplier) / 2,
                         (screen_height - 7 * sizeMultiplier) / 2 - 21 * sizeMultiplier))

            screen.blit(self.gui['shots'],
                        (((screen_width - 128 * sizeMultiplier) - 7 * 8 * sizeMultiplier) / 2,
                         (screen_height - 7 * sizeMultiplier) / 2))
            arcadify.render(self.player.shotsFired,
                            ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                            + (5 - len(str(self.player.shotsFired))) * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height - 7 * sizeMultiplier) / 2,
                            "yellow", sizeMultiplier, 999999, 2)

            screen.blit(self.gui['hits'],
                        (((screen_width - 128 * sizeMultiplier) - 7 * 8 * sizeMultiplier) / 2,
                         (screen_height + 7 * sizeMultiplier) / 2 + 14 * sizeMultiplier))
            arcadify.render(self.player.hits,
                            ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                            + (5 - len(str(self.player.hits))) * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height + 7 * sizeMultiplier) / 2 + 14 * sizeMultiplier,
                            "yellow", sizeMultiplier, 999999, 2)

            screen.blit(self.gui['accuracy'],
                        (((screen_width - 128 * sizeMultiplier) - 7 * 8 * sizeMultiplier) / 2,
                         (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier))
            if self.player.shotsFired != 0:
                accuracy = 100 / self.player.shotsFired * self.player.hits
            else:
                accuracy = 0
            accuracy_decimal = accuracy * 10 % 10
            accuracy = round(accuracy)
            arcadify.render(accuracy,
                            ((screen_width - 128 * sizeMultiplier) - 6 * 8 * sizeMultiplier) / 2
                            + (4 - len(str(accuracy))) * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier,
                            "white", sizeMultiplier, 999999, 2)
            arcadify.render(floor(accuracy_decimal),
                            ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                            + 3 * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier,
                            "white", sizeMultiplier, 9)
            arcadify.render(".",
                            ((screen_width - 128 * sizeMultiplier) - 6 * 8 * sizeMultiplier) / 2
                            + 4 * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier,
                            "white", sizeMultiplier)
            arcadify.render("%",
                            ((screen_width - 128 * sizeMultiplier) - 3 * 8 * sizeMultiplier) / 2
                            + 4 * 8 * sizeMultiplier + 128 * sizeMultiplier,
                            (screen_height + 7 * sizeMultiplier) / 2 + 35 * sizeMultiplier,
                            "white", sizeMultiplier)

            # Scores GUI
            self.tick_gui(mode="end")

            # Update Screen
            pygame.display.flip()

            if not pygame.mixer.get_busy():
                game_over_loop = False

        scoreboard = False
        if len(self.high_scores) < 5:
            scoreboard = True
        else:
            for i, value in enumerate(list(self.high_scores.values())):
                if self.player.score > value and i < 5:
                    scoreboard = True
        if self.player.score <= 0:
            scoreboard = False

        selected_letter = 0
        player_name = [0, 0, 0]
        letter_selection = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.']
        while scoreboard:
            self.clock.tick(self.tps)
            self.current_tick += 1

            # Reset Screen
            screen.fill((0, 0, 0))

            # Check if quit button has been pressed
            self.check_events(mode="save")
            if end_game:
                return

            # Edits Initials
            if self.save_action:
                if self.save_action == "right":
                    selected_letter = (selected_letter + 1) % 3
                if self.save_action == "left":
                    selected_letter = (selected_letter - 1) % 3
                if self.save_action == "up":
                    player_name[selected_letter] -= 1
                    if player_name[selected_letter] < 0:
                        player_name[selected_letter] = len(letter_selection) - 1
                if self.save_action == "down":
                    player_name[selected_letter] += 1
                    if player_name[selected_letter] >= len(letter_selection):
                        player_name[selected_letter] = 0
                self.player.name = (letter_selection[player_name[0]] + letter_selection[player_name[1]]
                                    + letter_selection[player_name[2]])
                self.save_action = None

            # Star Field
            for star in self.stars:
                if star.y_coord > screen_height - 3:
                    star.regenerate()
                else:
                    star.tick()

            self.tick_gui(mode="end")

            if self.gui_flash:
                screen.blit(self.gui['underline'],
                            (screen_width / 2 + 80 * sizeMultiplier - (3 - selected_letter) * 8 * sizeMultiplier,
                             120 * sizeMultiplier + 9 * sizeMultiplier))

            screen.blit(self.gui['initials'],
                        ((screen_width - 164 * sizeMultiplier) / 2,
                         55 * sizeMultiplier))
            screen.blit(self.gui['score'],
                        (screen_width / 2 - 72 * sizeMultiplier,
                         105 * sizeMultiplier))
            screen.blit(self.gui['name'],
                        (screen_width / 2 + 49 * sizeMultiplier,
                         105 * sizeMultiplier))
            arcadify.render(self.player.score, screen_width / 2 - 80 * sizeMultiplier +
                            (6 - len(str(self.player.score))) * 8 * sizeMultiplier,
                            120 * sizeMultiplier, "blue", sizeMultiplier, 999999, 2)
            for i in range(3):
                if i == selected_letter:
                    arcadify.render(letter_selection[player_name[i]],
                                    screen_width / 2 + 80 * sizeMultiplier - (3 - i) * 8 * sizeMultiplier,
                                    120 * sizeMultiplier, "white", sizeMultiplier)
                else:
                    arcadify.render(letter_selection[player_name[i]],
                                    screen_width / 2 + 80 * sizeMultiplier - (3 - i) * 8 * sizeMultiplier,
                                    120 * sizeMultiplier, "blue", sizeMultiplier)

            screen.blit(self.gui['score'],
                        (screen_width / 2 - 55 * sizeMultiplier, screen_height - 140 * sizeMultiplier))
            screen.blit(self.gui['name'],
                        (screen_width / 2 + 55 * sizeMultiplier, screen_height - 140 * sizeMultiplier))

            inclusive_high_scores = self.high_scores.copy()
            inclusive_high_scores[self.player.name] = self.player.score
            inclusive_high_scores = {k: v for k, v in sorted(inclusive_high_scores.items(),
                                                             key=lambda item: item[1], reverse=True)}

            for i, (name, score) in enumerate(inclusive_high_scores.items()):
                if i > 4:
                    break
                if name == self.player.name and score == self.player.score:
                    screen.blit(
                        [self.gui['first_yellow'], self.gui['second_yellow'], self.gui['third_yellow'],
                         self.gui['fourth_yellow'], self.gui['fifth_yellow'], ][i],
                        (screen_width / 2 - 90 * sizeMultiplier, screen_height - (120 - i * 20) * sizeMultiplier))
                    arcadify.render(name, screen_width / 2 + 66 * sizeMultiplier,
                                    screen_height - (120 - i * 20) * sizeMultiplier, "yellow", sizeMultiplier)
                    arcadify.render(score,
                                    screen_width / 2 - 55 * sizeMultiplier + (6 - len(str(score))) * 8 * sizeMultiplier,
                                    screen_height - (120 - i * 20) * sizeMultiplier,
                                    "yellow", sizeMultiplier, 999999, 2)
                else:
                    screen.blit(
                        [self.gui['first'], self.gui['second'], self.gui['third'],
                         self.gui['fourth'], self.gui['fifth'], ][i],
                        (screen_width / 2 - 90 * sizeMultiplier, screen_height - (120 - i * 20) * sizeMultiplier))
                    arcadify.render(name, screen_width / 2 + 66 * sizeMultiplier,
                                    screen_height - (120 - i * 20) * sizeMultiplier, "blue", sizeMultiplier)
                    arcadify.render(score,
                                    screen_width / 2 - 55 * sizeMultiplier + (6 - len(str(score))) * 8 * sizeMultiplier,
                                    screen_height - (120 - i * 20) * sizeMultiplier,
                                    "blue", sizeMultiplier, 999999, 2)

            screen.blit(self.gui['top'],
                        ((screen_width - 88 * sizeMultiplier) / 2,
                         screen_height / 2))

            pygame.display.flip()

            if not pygame.mixer.get_busy():
                self.sounds['initials'].play()

            if self.save_score:
                self.save_high_score(self.player.name, self.player.score)
                scoreboard = False
        self.sounds['initials'].stop()
        if self.players == 2:
            if self.player.player_number == 1 and not self.player2.game_end:
                self.current_player = 2
            if self.player.player_number == 2 and not self.player1.game_end:
                self.current_player = 1
        if (self.players == 2 and self.player1.game_end and self.player2.game_end
                or self.players == 1 and self.player.game_end):
            self.running = False


class Star:
    def __init__(self):
        self.x_coord = randint(0, floor(screen_width))
        self.y_coord = randint(0, floor(screen_height))
        self.max_brightness = 110
        self.colour = [randint(0, self.max_brightness),
                       randint(0, self.max_brightness), randint(0, self.max_brightness)]
        self.display_colour = choice([True, False])
        self.tick_delay = randint(0, 4)
        self.velocity = randint(2, 8)

        self.image = pygame.Surface((1.2 * sizeMultiplier, 1.2 * sizeMultiplier))

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
        self.x_coord = randint(0, floor(screen_width))


class Player:
    def __init__(self, game=None, player_number=1, lives=initial_lives):
        self.life = lives
        self.lives_remaining = self.life - 1
        self.stage = 1
        self.player_number = player_number
        self.score = 0
        self.fighters = 1

        self.enemies_in_formation = False
        self.enemy_pulse = 1
        self.enemy_pulse_tick = 4.71
        self.enemies = []
        self.enemy_missiles = []

        self.name = "AAA"
        self.upgrades_reached = 0
        self.height = 16 * sizeMultiplier
        self.fighter_width = 15 * sizeMultiplier
        self.width = self.fighter_width * self.fighters
        self.game = game
        self.ticking = True
        self.timeout = 60
        self.tick_delay = 0
        self.respawning = False
        self.started = False
        self.game_end = False
        self.challenging_stage = False
        self.challenge_hits = 0

        self.x_coord = screen_width / 2 - self.width / 2
        self.y_coord = screen_height - 32 * sizeMultiplier
        self.shotsFired = 0
        self.hits = 0

        self.missiles = []

        self.image = pygame.transform.scale(self.game.sprites['player'], (self.fighter_width, self.height))

    def tick(self):
        global life_bonus
        self.tick_delay += 1
        self.width = self.fighter_width * self.fighters

        if self.enemies_in_formation:
            self.enemy_pulse = sin(self.enemy_pulse_tick) / 10 + 1.1
            self.enemy_pulse_tick += 0.015

        if self.score >= life_bonus[0] and self.upgrades_reached == 0:
            self.upgrades_reached += 1
            self.life += 1
            self.game.sounds['player_bonus_life'].play()

        if self.score >= life_bonus[1] + life_bonus[2] * (abs(self.upgrades_reached - 1)):
            self.upgrades_reached += 1
            self.life += 1
            self.game.sounds['player_bonus_life'].play()

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
                if (self.game.players == 2 and self.life >= 1 and not
                   [self.game.player1, self.game.player2][self.player_number % 2].game_end):
                    self.game.current_player = self.game.current_player % 2 + 1
            if self.timeout == 219:
                if self.life > 0:
                    self.game.sounds['player_respawn'].play()
            if self.timeout < 120 and self.life >= 1:
                self.lives_remaining = self.life - 1
                if self.tick_delay % 10 == 0:
                    self.respawning = not self.respawning
                if self.respawning:
                    for fighter in range(self.fighters):
                        screen.blit(self.image,
                                    (self.x_coord + self.fighter_width * fighter, self.y_coord - self.height / 2))
            if (self.timeout < 75 and self.life >= 1 and self.game.players == 1 or
                    self.timeout < 210 and self.life >= 1 and self.game.players == 2):
                screen.blit(self.game.gui['ready'],
                            ((screen_width - 37 * sizeMultiplier) / 2, (screen_height - 12 * sizeMultiplier) / 2))
                if self.player_number == 1 and self.game.players == 2:
                    screen.blit(self.game.icon_player_1,
                                ((screen_width - 58 * sizeMultiplier) / 2,
                                 (screen_height - 7 * sizeMultiplier) / 2 + 12 * sizeMultiplier))
                if self.player_number == 2:
                    screen.blit(self.game.icon_player_2,
                                ((screen_width - 58 * sizeMultiplier) / 2,
                                 (screen_height - 7 * sizeMultiplier) / 2 + 12 * sizeMultiplier))
            if self.timeout < 1:
                self.game.sounds['player_respawn'].stop()
                self.ticking = True
            else:
                self.timeout -= 1
                self.x_coord = screen_width / 2 - self.width / 2

    def move(self, direction):
        if direction == -1:
            if self.x_coord > screen_width / 2 - screen_height * 7 / 18 + 6 * sizeMultiplier:
                self.x_coord -= round(3.2 * sizeMultiplier)
        if direction == 1:
            if self.x_coord < screen_width / 2 + screen_height * 7 / 18 - self.width - 6 * sizeMultiplier:
                self.x_coord += round(3.2 * sizeMultiplier)

    def shoot(self):
        if len(self.missiles) < 2 * self.fighters:
            self.game.sounds['player_firing'].play()
            for fighter in range(self.fighters):
                self.missiles.append(Missile(self.x_coord + self.fighter_width / 2 + fighter * self.fighter_width,
                                             self.y_coord, "player", self.game))
                self.shotsFired += 1

    def check_collision(self):
        for missile in self.enemy_missiles:
            if (abs(self.x_coord + self.width / 2 - missile.x_coord) <
                    self.width / 2 + missile.width / 2 and abs(
                        self.y_coord - missile.y_coord) <
                    self.height / 2 + missile.height / 2):
                try:
                    self.enemy_missiles.remove(missile)
                except ValueError:
                    continue
                if self.fighters <= 1:
                    self.die()
                else:
                    self.game.sounds['player_death'].play()
                    self.game.explosions.append(Explosion(
                        missile.x_coord, self.y_coord + self.height / 2, "player", self.game))
                    self.add_fighters(-1)

    def die(self):
        self.ticking = False
        self.life -= 1
        self.game.sounds['player_death'].play()
        self.game.explosions.append(Explosion(
            self.x_coord + self.width, self.y_coord + self.height / 2, "player", self.game))
        if self.game.players == 2 and self.life > 0:
            self.timeout = 325
        else:
            self.timeout = 250

    def add_fighters(self, operator=1):
        self.fighters += operator
        self.x_coord -= operator * (self.fighter_width / 2)


class Missile:
    def __init__(self, x_coord, y_coord, team="player", game=None, target_x=screen_width / 2):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.team = team
        self.game = game
        self.ticking = True
        self.target = target_x
        if team == "enemy":
            self.arc = randint(15, 40)
        self.width = 3 * sizeMultiplier
        self.height = 8 * sizeMultiplier

        if self.team == "player":
            self.image = pygame.transform.scale(self.game.sprites['missile_player'], (self.width, self.height))
        elif self.team == "enemy":
            self.image = pygame.transform.scale(self.game.sprites['missile_enemy'], (self.width, self.height))

    def tick(self):
        if self.ticking:
            self.check_collision()
            if self.y_coord > 3:
                if self.team == "player":
                    self.y_coord -= round(12 * sizeMultiplier)
                elif self.team == "enemy":
                    self.y_coord += round(7 * sizeMultiplier)
                    self.x_coord += round((self.target - self.x_coord) / self.arc)

            screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord - self.height / 2))

    def check_collision(self):
        if self.team == "player":
            for enemy in self.game.player.enemies:
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
                        self.game.sounds['enemy_hurt'].play()
                    try:
                        self.game.player.missiles.remove(self)
                    except ValueError:
                        continue
            for missile in self.game.player.enemy_missiles:
                if (abs(self.x_coord - missile.x_coord) <
                        self.width / 2 + missile.width / 2 and abs(
                            self.y_coord - missile.y_coord) <
                        self.height / 2 + missile.height / 2):
                    self.ticking = False
                    missile.ticking = False
                    self.game.player.hits += 1
                    self.game.explosions.append(Explosion(
                        self.x_coord + self.width / 2, self.y_coord + self.height / 2, "enemy", self.game))
                    try:
                        self.game.player.enemy_missiles.remove(missile)
                        self.game.player.missiles.remove(self)
                    except ValueError:
                        continue


class Enemy:
    def __init__(self, column=0, row=0, game=None, ticking=True):
        self.species = [2, 1, 1, 0, 0][row]
        self.column = column
        self.row = row

        self.side_shift = self.column / abs(self.column) * 9 * sizeMultiplier
        self.y_coord = 40 * sizeMultiplier + (18 * sizeMultiplier * self.row)
        self.x_coord = screen_width / 2 - self.side_shift + (18 * sizeMultiplier * self.column)
        self.rotation = '0'
        self.game = game
        self.diving = False
        self.ticking = ticking
        self.tick_delay = 0
        self.health = [1, 1, 2][self.species]
        self.death_sound = ['enemy_death_a', 'enemy_death_b', 'enemy_death_c'][self.species]

        self.width = sizeMultiplier * [13, 13, 15][self.species]
        self.height = sizeMultiplier * [10, 10, 16][self.species]

        self.image = self.game.sprites['enemy'][
            ['0', '1', ['2a', '2b'][self.health < 2]][self.species]
        ][self.rotation]
        self.animated = False
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def tick(self):
        self.tick_delay += 1

        if not self.diving:
            self.y_coord = 40 * sizeMultiplier + (18 * sizeMultiplier * self.row * self.game.player.enemy_pulse)
            self.x_coord = screen_width / 2 - self.side_shift + (18 * sizeMultiplier * self.column *
                                                                 self.game.player.enemy_pulse)

        if self.tick_delay % 15 == 0:
            self.animated = not self.animated

        if self.animated and self.rotation == '0':
            self.image = self.game.sprites['enemy'][
                ['0', '1', ['2a', '2b'][self.health < 2]][self.species]
            ]['animated']
        else:
            self.image = self.game.sprites['enemy'][
                ['0', '1', ['2a', '2b'][self.health < 2]][self.species]
            ][self.rotation]

        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, (self.x_coord - self.width / 2, self.y_coord - self.height / 2))

        if (randint(1, 1000) == 1 and self.game.player.ticking and self.ticking
                and not self.game.player.challenging_stage):
            self.shoot()

    def shoot(self):
        self.game.player.enemy_missiles.append(Missile(self.x_coord, self.y_coord,
                                                       "enemy", game=self.game, target_x=self.game.player.x_coord))

    def die(self):
        self.game.player.score += [[50, 100], [80, 160], [150, 400]][self.species][self.diving]
        if self.game.player.challenging_stage:
            self.game.player.challenge_hits += 1
        self.game.sounds[self.death_sound].play()
        self.game.explosions.append(Explosion(
            self.x_coord + self.width / 2, self.y_coord + self.height / 2, "enemy", self.game))
        if self in self.game.player.enemies:
            try:
                self.game.player.enemies.remove(self)
            except ValueError:
                return


class Explosion:
    def __init__(self, x_coord, y_coord, target, game):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.game = game
        self.tick_delay = 0
        self.animation = 0
        self.target = target
        if self.target == "player":
            self.size = 26 * sizeMultiplier
            self.image = self.game.sprites['player_explosion'][0]
            self.animation_speed = 6
            self.size_shift = 1.25
        elif self.target == "enemy":
            self.size = 12 * sizeMultiplier
            self.image = self.game.sprites['enemy_explosion'][0]
            self.animation_speed = 3
            self.size_shift = 1

    def tick(self):
        self.tick_delay += 1
        self.animation = floor(self.tick_delay / self.animation_speed)
        if self.animation > 4:
            self.game.explosions.remove(self)
        else:
            if self.target == "player":
                self.image = self.game.sprites['player_explosion'][self.animation]
            elif self.target == "enemy":
                self.image = self.game.sprites['enemy_explosion'][self.animation]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        screen.blit(self.image,
                    (self.x_coord - self.size / self.size_shift, self.y_coord - self.size / self.size_shift))


while not end_game:
    galaga = Game()
    galaga.start()
    del galaga
