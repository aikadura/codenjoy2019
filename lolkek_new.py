import pygame
import time
import random
import copy

pygame.init()

display_width = 800
display_height = 800

pole_x = 15
pole_y = 15

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Codenjoy Hackathon')

clock = pygame.time.Clock()

Game = True
game_over = False

STEPS = 30

MY_SCORE = 0

start_ = pygame.image.load('start.jpg')
zastavka_ = pygame.image.load('zastavka.png')
win_ = pygame.image.load('win.png')
gameover_ = pygame.image.load('go.png')

krolik_ = pygame.image.load('krolik.png')  # 35x39
lis_ = pygame.image.load('lis.png')  # 32x39
morozhenoe_ = pygame.image.load('ice.png')  # 19x40
morkovka_ = pygame.image.load('mork.png')  # 40x16

house_1 = pygame.image.load('dom11.png')  # 40x40
house_2 = pygame.image.load('dom22.png')  # 40x40
house_3 = pygame.image.load('dom33.png')  # 40x40
house_4 = pygame.image.load('dom44.png')  # 40x40
bush_ = pygame.image.load('bush.png')  # 40x30

start = True
zastavka = False
next_level = False

zoom = 40

lab = [[
    [-9, -9, -9, -9, -9, -9, -1, -9, -2, -3, -4, -2, -3, -2, -9],
    [-1, -2, -3, -4, -1, -9, -2, 1, 0, 0, 0, 0, -3, -4, -9],
    [-1, 0, 0, 0, -2, -9, -3, 0, -1, -2, -3, 0, 0, -4, -9],
    [-1, -2, -3, 0, -4, -1, -2, 0, 0, 0, 0, -1, 0, -2, -9],
    [-9, -9, -1, 0, 0, 0, 0, 0, -2, -3, 0, -4, 0, -1, -2],
    [-9, -9, -1, 0, -2, -3, -4, 0, -1, -2, 0, -3, 0, 0, -1],
    [-3, -2, -3, 0, -4, -1, -2, 0, 0, 0, 0, -3, 0, -4, -3],
    [-1, 0, 0, 0, -2, 0, 0, 0, -2, -3, 0, -4, 0, -1, -9],
    [-3, -2, -3, 0, 0, 0, -4, 0, -1, -2, 0, 0, 0, -3, -9],
    [-9, -1, -2, -3, -4, 0, -1, 0, -2, -3, -4, 0, -1, -2, -9],
    [-9, -1, 0, 0, 0, 0, -2, 0, 0, 0, -3, 0, -4, -9, -9],
    [-2, -1, 0, -1, -4, 0, -3, 0, -4, 0, 0, 0, -4, -3, -2],
    [-9, 0, 0, -4, -1, 0, -3, 0, -4, 0, -1, 0, 0, 0 - 1],
    [-3, -4, 0, 0, 0, 0, -1, 0, 0, 0, -3, -2, -4, -2, -4],
    [-9, -2, -4, -1, -3, -2, -4, -2, -3, -2, -4, -9, -9, -9, -9]
],
    [
        [-9, -1, -2, -3, -4, -1, -2, -9, -1, -2, -3, -4, -1, -2, -3],
        [-9, -1, 0, 0, 0, -3, -4, 1, -1, 0, 0, 0, 0, 0, -9],
        [-1, -2, 0, -3, 0, -1, -2, 0, -2, 0, -1, -3, -4, -2, -1],
        [-9, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, -1, -2, -3],
        [-1, 0, -2, -3, -4, -1, -2, 0, -2, 0, -3, 0, 0, 0, -1],
        [-9, 0, 0, 0, 0, 0, -3, 0, -4, 0, -1, -2, -3, -4, -1],
        [-1, -2, 0, -3, -4, 0, -1, 0, -2, 0, 0, 0, -4, -9, -9],
        [-1, -2, 0, -3, -4, 0, -1, 0, 0, 0, -4, 0, -2, -9, -9],
        [-2, 0, 0, 0, 0, 0, -1, -2, -3, -4, -1, 0, -1, -2, -3],
        [-1, 0, -2, -3, -4, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0, -1, -2, 0, -3, 0, -4, -1, -2, -3, -4, -1, -2],
        [-1, -2, 0, -3, -4, 0, 0, 0, -1, 0, 0, 0, -2, -4, -9],
        [-9, -1, 0, -2, -3, 0, -4, 0, -3, 0, -2, 0, -1, -2, -3],
        [-9, -4, 0, 0, 0, 0, -3, 0, 0, 0, -1, 0, 0, 0, -3],
        [-9, -1, -2, -3, -4, -1, -2, -3, -4, -1, -2, -3, -4, -1, -2]
    ]]


class Player():
    level = 0
    game_state = "intro"
    x = 0
    y = 0
    lab = None
    labs = None
    score = 0
    steps = 0

    def game_start(self,lab):
        self.labs = lab
        if self.game_state == "intro":
            self.game_state = "game"
            self.score = 0
            self.level = 0
            self.switch_level(self.level)

    def switch_level(self, level):
        self.lab = copy.deepcopy(self.labs[level])
        self.steps = 30
        for i in range(len(self.lab)):
            for j in range(len(self.lab[i])):
                if self.lab[i][j] == 1:
                    self.x = i
                    self.y = j
                    self.lab[i][j] = 0
                elif self.lab[i][j] == 0:
                    if random.randint(1, 100) > 80:
                        self.lab[i][j] = 7
                    else:
                        self.lab[i][j] = 8

    def move(self, direction):
        if direction == "left":
            nx = self.x
            ny = self.y - 1
            if ny < 0:
                return False
        elif direction == "right":
            nx = self.x
            ny = self.y + 1
            if ny > len(self.lab[nx]):
                return False
        elif direction == "up":
            nx = self.x - 1
            ny = self.y
            if nx < 0:
                return False
        elif direction == "down":
            nx = self.x + 1
            ny = self.y
            if nx > len(self.lab):
                return False
        else:
            return False

        if self.lab[nx][ny] < 0:
            return False

        self.x = nx
        self.y = ny
        self.steps -= 1

        if self.lab[self.x][self.y] == 7:
            self.score += 30
            self.lab[self.x][self.y] = 0
        elif self.lab[self.x][self.y] == 8:
            self.score += 10
            self.lab[self.x][self.y] = 0

        if self.steps == 0:
            self.level += 1
            self.switch_level(self.level)


players = [Player()]

x = 7  # 280
y = 1  # 40

x0 = 0
y0 = 0

bonus2 = [[], []]
bonus1 = [[], []]
level = 0

dy = 0
dx = 0

bushes = [[], []]
house1 = [[], []]
house2 = [[], []]
house3 = [[], []]
house4 = [[], []]

# координаты домов, кустов, главного героя
for lev in range(2):
    for row in range(len(lab[lev])):
        for col in range(len(lab[lev][row])):

            if lab[lev][row][col] == 0:
                a = random.randint(1, 100)
                if a <= 50:
                    bonus1[lev].append((col, row))
                elif a <= 100:
                    bonus2[lev].append((col, row))

            if lab[lev][row][col] == -1:
                house1[lev].append((col, row))

            if lab[lev][row][col] == -2:
                house2[lev].append((col, row))

            if lab[lev][row][col] == -3:
                house3[lev].append((col, row))

            if lab[lev][row][col] == -4:
                house4[lev].append((col, row))

            if lab[lev][row][col] == -9:
                bushes[lev].append((col, row))

            if lab[lev][row][col] == 1:
                x = col
                y = row
                x0 = x
                y0 = y

while Game:
    for player in players:
        if player.game_state == "intro":
            player.game_start(lab)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                Game = False

            # кнопка нажата

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.game_start(lab)

                if event.key == pygame.K_LEFT:
                    player.move("left")

                if event.key == pygame.K_RIGHT:
                    player.move("right")

                if event.key == pygame.K_UP:
                    player.move("up")

                if event.key == pygame.K_DOWN:
                    player.move("down")

        gameDisplay.fill((255, 250, 232))
        # разные заставки
        if player.game_state == "intro":
            gameDisplay.blit(start_, (0, 0))

        elif player.game_state == "game":

            for i in range(len(player.lab)):
                for j in range(len(player.lab[i])):
                    cell = player.lab[i][j]
                    img = None
                    if cell == -1:
                        img = house_1
                    elif cell == -2:
                        img = house_2
                    elif cell == -3:
                        img = house_3
                    elif cell == -4:
                        img = house_4
                    elif cell == -9:
                        img = bush_
                    elif cell == 7:
                        img = morozhenoe_
                    elif cell == 8:
                        img = morkovka_
                    elif i == player.x and j == player.y:
                        img = krolik_
                    if img is not None:
                        gameDisplay.blit(img, (j * 40 + 100, i * 40 + 100))

            font = pygame.font.Font(None, 30)
            text = font.render("Score: " + str(player.score), True, (0, 0, 0))
            gameDisplay.blit(text, [20, 20])
            text = font.render("Steps: " + str(player.steps), True, (0, 0, 0))
            gameDisplay.blit(text, [20, 55])

        pygame.display.update()
        clock.tick(20)

pygame.quit()
quit()
