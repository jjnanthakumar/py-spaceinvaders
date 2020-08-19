import pygame
import random, math
from pygame import mixer
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption('SpaceInvaders')
pygame.display.set_icon(pygame.image.load('space.png'))
playerImg = pygame.image.load('space.png')
playerx = 370
playery = 480
playerx_ch = 0

enemyImg = []
enemyx = []
enemyy = []
enemyx_ch = []
enemyy_ch = []

for i in range(7):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_ch.append(3)
    enemyy_ch.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_ch = 4
bullety_ch = 10
bullet_state = "ready"
game_score = 0

font = pygame.font.Font('freesansbold.ttf', 32)
game_over = pygame.font.Font('freesansbold.ttf', 64)


def game_over1():
    txt = game_over.render("GAME OVER ", True, (255, 0, 255))
    txt1 = game_over.render("Your Final Score : " + str(game_score), True, (255, 0, 255))
    screen.blit(txt, (200, 250))
    screen.blit(txt1, (50, 230))


def show_score():
    score = font.render("SCORE  " + str(game_score), True, (255, 0, 0))
    screen.blit(score, (10, 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def enemy(ex, ey, i):
    screen.blit(enemyImg[i], (ex[i], ey[i]))


def isCollison(enemyx, enemyy, bulletx, bullety):
    res = math.sqrt(math.pow(bulletx - enemyx, 2) + math.pow(bullety - enemyy, 2))
    if res < 27:
        return True
    else:
        return False


background = pygame.image.load('bgimage.jpg')
run = True

while run:
    pygame.time.Clock()
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for eve in pygame.event.get():
        if eve.type == pygame.KEYDOWN:
            if eve.key == pygame.K_LEFT:
                playerx_ch = -5
            if eve.key == pygame.K_RIGHT:
                playerx_ch = 5
            if eve.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    mixer.Sound('laser.wav').play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if eve.type == pygame.KEYUP:
            if eve.key == pygame.K_LEFT or eve.key == pygame.K_RIGHT:
                playerx_ch = 0
        if eve.type == pygame.QUIT:
            run = False
    playerx += playerx_ch
    if playerx >= 736:
        playerx = 736
    elif playerx <= 0:
        playerx = 0
    # bullet movement
    if bullety <= 0:
        bullet_state = "ready"
        bullety = 480

    if bullet_state is "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_ch

    # enemy movement
    for i in range(7):

        enemyx[i] += enemyx_ch[i]
        if enemyy[i] > 440:
            for j in range(7):
                enemyy[j] = 2000
            game_over1()
            break
        if enemyx[i] >= 736:
            enemyx_ch[i] = -3
            enemyy[i] += enemyy_ch[i]
        elif enemyx[i] <= 0:
            enemyx_ch[i] = 3
            enemyy[i] += enemyy_ch[i]

        if isCollison(enemyx[i], enemyy[i], bulletx, bullety):
            mixer.Sound('explosion.wav').play()
            bullety = 480
            bullet_state = "ready"
            game_score += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx, enemyy, i)
        # print(game_score)
    player(playerx, playery)
    show_score()

    pygame.display.update()
pygame.quit()