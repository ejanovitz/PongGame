# Pong Game
# by Ethan Janovitz
# May 28, 2020 (High School - Grade 10)

import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()
pygame.mixer.init()

# setting colours and window measurements
BLACK = (0, 0, 0)
white = (255, 255, 255)
window_width = 1200
window_height = 800
myfont = pygame.font.SysFont("Cambria Math", 60)
window = pygame.display.set_mode((window_width, window_height))

FPS = 120
clock = pygame.time.Clock()
beep_sound = pygame.mixer.Sound("beep.wav")


# player class to keep track of players score
class Player:
    def __init__(self):
        self.score = 0

    def win(self):
        self.score += 1


class Ball:
    def __init__(self):
        # sets the starting attributes for the ball
        randomizer_speed = random.choice([-1, 1])  # adds a random element to speed
        randomizer_angle = random.choice([-1, 1])  # adds a random element to angle
        self.window = window
        self.x = window_width / 2
        self.y = window_height / 2
        self.radius = 10
        self.colour = BLACK
        self.speed = 2 * randomizer_speed
        self.angle = 1 * randomizer_angle

    def draw(self):
        pygame.draw.circle(self.window, self.colour, (int(self.x), int(self.y)), self.radius)

    def move(self):
        # stops ball from leaving screen at left and right
        if self.x + self.speed < 0:
            player2.win()
            ball.reset()
        elif self.x + self.radius > window_width:
            player1.win()
            ball.reset()

        # stops the ball from leaving at the top and bottom
        if self.y + self.angle - self.radius < 0 or self.y + self.angle + self.radius > window_height:
            self.angle = -self.angle

        self.x += self.speed
        self.y += self.angle

    def reset(self):
        # puts the ball back in the middle of the screen
        self.x = window_width / 2
        self.y = window_height / 2

    def check_collision(self):
        # checks if the ball hit the paddle
        if self.x < 20 + paddle1.width + self.radius:
            if paddle1.y < self.y < paddle1.y + paddle1.height:
                self.speed = -self.speed
                pygame.mixer.Sound.play(beep_sound)
        elif self.x > window_width - 20 - paddle2.width - self.radius:
            if paddle2.y < self.y < paddle2.y + paddle2.height:
                self.speed = -self.speed
                pygame.mixer.Sound.play(beep_sound)


class Paddle:
    # sets the starting attributes of a paddle
    def __init__(self, x):
        self.window = window
        if x == 'left':
            self.x = 20
        elif x == 'right':
            self.x = 1170
        self.y = 340
        self.height = 120
        self.width = 10
        self.colour = BLACK
        self.up = False
        self.down = False

    def draw(self):
        pygame.draw.rect(self.window, self.colour, (self.x, self.y, self.width, self.height))

    # moves each paddle up and down, stopping them at top and bottom of screen
    def move(self):
        if self.up and self.y > 0:
            self.y -= 10
        elif self.down and self.y + self.height < window_height:
            self.y += 10


# creates the game objects
paddle1 = Paddle('left')
paddle2 = Paddle('right')
player1 = Player()
player2 = Player()
ball = Ball()

# adds game objects to a list, so they can be iterated over in a for loop
game_objects = [paddle1, paddle2, ball]

game_over = False

# main game loop
while not game_over:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # allows the keys that get pressed to actually do something
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle2.up = True
            elif event.key == pygame.K_DOWN:
                paddle2.down = True
            elif event.key == pygame.K_w:
                paddle1.up = True
            elif event.key == pygame.K_s:
                paddle1.down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                paddle2.up = False
            elif event.key == pygame.K_DOWN:
                paddle2.down = False
            elif event.key == pygame.K_w:
                paddle1.up = False
            elif event.key == pygame.K_s:
                paddle1.down = False

    # clears the screen
    window.fill(white)
    # draws every item and lets them move
    for game_object in game_objects:
        game_object.draw()
        game_object.move()

    ball.check_collision()

    # prints the score at the top of the window
    player1_score = myfont.render(str(player1.score), True, BLACK)
    player2_score = myfont.render(str(player2.score), True, BLACK)
    window.blit(player1_score, (window_width / 4, 20))
    window.blit(player2_score, (window_width * 0.75, 20))

    # checks if either player has reached 5 points
    if player1.score == 5 or player2.score == 5:
        end = myfont.render("GAME OVER", True, BLACK)
        window.blit(end, ((window_width / 2) - 130, window_height / 2))
        pygame.display.update()
        time.sleep(3)
        game_over = True

    pygame.display.update()
