__author__ = 'Pradyumn Vikram'

# some imports
import pygame
import random

# setting screen dimesnions and declaring variables
pygame.font.init()

WIDTH, HEIGHT = 650, 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping-Pong')

# player class


class Pad():
    def __init__(self, x, y, color, height, width, points=0):
        self.x = x
        self.y = y
        self.points = points
        self.color = color
        self.height = height
        self.width = width

    def draw(self, window):
        # window.blit(RED_BASE, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)
        pygame.draw.rect(window, self.color, self.rect)

    def move(self, player_vel, commands):
        keys = pygame.key.get_pressed()
        if keys[commands[0]] and self.y + player_vel > 7:
            self.y -= player_vel
        if keys[commands[1]] and self.y + player_vel + self.width + 7 < HEIGHT:
            self.y += player_vel


def collide(obj1, obj2):
    if obj1.rect.colliderect(obj2.circle_rect):
        return True

# ping-pong ball class


class Ball():
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.ball_vel = [random.randint(4, 8), random.randint(-8, 8)]

    def draw(self, window):
        self.circle_rect = pygame.draw.circle(window,
                                              (255, 32, 82),
                                              (self.dx, self.dy), 20)

    def move(self, player1, player2):
        # moving ball
        self.dx += self.ball_vel[0]
        self.dy += self.ball_vel[1]
        # moving in opposite direction if any wall is hit and reducing respective player points
        if self.dx >= WIDTH - 10:
            if player2.points > 0:
                player2.points -= 1

            self.ball_vel[0] = -self.ball_vel[0]
        if self.dx <= 10:
            if player1.points > 0:
                player1.points -= 1
            self.ball_vel[0] = -self.ball_vel[0]
        if self.dy >= HEIGHT - 10:
            self.ball_vel[1] = -self.ball_vel[1]
        if self.dy <= 10:
            self.ball_vel[1] = -self.ball_vel[1]

    def rebound(self):
        self.ball_vel[0] = -self.ball_vel[0]
        self.ball_vel[1] += random.randint(-8, 8)

# the main loop


def main():
    # some variables
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    main_font = pygame.font.SysFont('comicsans', 50)
    # function to redraw window every frame

    def redraw_window():
        WIN.fill((0, 0, 0))
        p1.draw(WIN)
        p2.draw(WIN)
        ball.draw(WIN)
        point_p1 = main_font.render(f'{p1.points}', 1, (255, 255, 255))
        WIN.blit(point_p1, (10, 10))
        point_p2 = main_font.render(f'{p2.points}', 1, (255, 255, 255))

        WIN.blit(point_p2, (WIDTH - point_p1.get_width() - 15, 10))
        # checking for collisions
        if collide(p1, ball):
            ball.rebound()
            p1.points += 1
        if ball.ball_vel[0] > 8:
            ball.ball_vel[0] = 8
        if ball.ball_vel[1] > 8:
            ball.ball_vel[1] = 8
        if collide(p2, ball):
            ball.rebound()
            p2.points += 1
        if ball.ball_vel[0] > 8:
            ball.ball_vel[0] = 8
        if ball.ball_vel[1] > 8:
            ball.ball_vel[1] = 8

        pygame.display.update()

    p1 = Pad(2, 450, (255, 0, 0), 10, 150)
    p2 = Pad(WIDTH - 15, 450, (0, 0, 255), 10, 150)
    ball = Ball(WIDTH//2, HEIGHT//2)
    player_vel = 10
    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit(1)
        p1.move(player_vel, [pygame.K_w, pygame.K_s])
        p2.move(player_vel, [pygame.K_UP, pygame.K_DOWN])
        ball.move(p1, p2)

# creating the main menu


def main_menu():
    title_font = pygame.font.SysFont('comicsans', 70)
    run = True
    while run:
        WIN.fill((0, 0, 0))
        title_label = title_font.render('Press the mouse to start!',
                                        1,
                                        (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
