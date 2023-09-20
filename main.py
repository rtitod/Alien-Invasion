import pygame
import random
import math
from pygame import mixer

# initialization

pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 620))

# background

background = pygame.image.load('background.jpg')

# bg sound
mixer.music.load('background.mp3')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('battleship.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('transport.png')
playerwidth = 75
playerheight = 79
playerx = 370
playery = 520
playerx_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
number_of_enemies = 8
enemy_speed_x = 1.0  # Velocidad inicial de los enemigos
enemy_speed_y = 1.0  # Velocidad inicial de los enemigos
enemywidth = 94
enemyheight = 80
itsover = False

# variable para el estado de los proyectiles de los enemigos
enemy_bullet_state = []
enemy_bullet_width = 30
enemy_bullet_height = 32

# lista para las posiciones de los proyectiles de los enemigos
enemy_bulletx = []
enemy_bullety = []

enemy_bulletx_change = []
enemy_bullety_change = []

# enemy_bullet
enemybulletimg = []

for i in range(number_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(0, 150))
    enemyx_change.append(6.0)
    enemyy_change.append(40)
    enemy_bullet_state.append("ready")
    enemy_bulletx.append(0)
    enemy_bullety.append(0)
    enemy_bulletx_change.append(0)
    enemybulletimg.append(pygame.image.load('enemybullet.png'))

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 45 * enemy_speed_x
bullet_state = "ready"
bullet_auto_state = "ready"
bulletwidth = 12
bulletheight = 49

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# game over txt
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_txt = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_txt, (200, 250))


# for display player img
def player(x, y):
    screen.blit(playerimg, (x, y))


# foe desplaing enemy img

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_enemy_bullet(x, y, i):
    global enemy_bullet_state
    enemy_bullet_state[i] = "fire"
    screen.blit(enemybulletimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 32, y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow((enemyx + enemywidth/2.0) - (bulletx + bulletwidth/2.0), 2)) +
                         (math.pow((enemyy + enemyheight/2.0) - (bullety + bulletheight/2.0), 2)))
    if distance < 50:
        return True
    else:
        return False


def iscollision_player(x, y, bulletx, bullety):
    distance = math.sqrt((math.pow((x + playerwidth/2.0) - (bulletx + enemy_bullet_width/2.0), 2)) +
                         (math.pow((y + playerheight/2.0) - (bullety + enemy_bullet_height/2.0), 2)))
    #print (distance)
    if distance < 40:
        return True
    else:
        return False


def iscollision_enemy(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
clock = pygame.time.Clock()  # Crear un reloj para controlar el framerate
while running:

    screen.fill((0, 0, 0))
    # for bg img
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke in pressed whether it is right of left
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                playerx_change = -12.0
            if (event.key == pygame.K_RIGHT):
                playerx_change = 12.0

            if (event.key == pygame.K_SPACE):
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
                # Activar el autodisparo
                bullet_auto_state = "fire"

        if (event.type == pygame.KEYUP):
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
            if event.key == pygame.K_SPACE:
                bullet_auto_state = "ready"

    playerx += playerx_change
    # create boundry for player
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    if not itsover:
        for i in range(number_of_enemies):


            # game over
            if enemyy[i] > 470:
                for j in range(number_of_enemies):
                    enemyy[j] = 2000
                itsover = True

            enemyx[i] += enemyx_change[i] * enemy_speed_x
            # create boundry for enemy
            if enemyx[i] <= 0:
                enemyx_change[i] = 6.0 * enemy_speed_x
                enemyy[i] += enemyy_change[i] * enemy_speed_y
            elif enemyx[i] >= 736:
                enemyx_change[i] = -6.0 * enemy_speed_x
                enemyy[i] += enemyy_change[i] * enemy_speed_y

            # Comprueba si el enemigo está listo para disparar, y un número aleatorio cumple con la condición
            if enemy_bullet_state[i] == "ready" and random.randint(1, 100) == 1:
                values_random = [-2, 0, 2]
                enemy_bulletx[i] = enemyx[i] + 32
                enemy_bullety[i] = enemyy[i] + 32
                enemy_bulletx_change[i] = random.choice(values_random)
                fire_enemy_bullet(enemy_bulletx[i], enemy_bullety[i], i)
            elif enemy_bullet_state[i] == "fire":
                enemy_bulletx[i] += enemy_bulletx_change[i]
                enemy_bullety[i] += 4 * enemy_speed_y
                fire_enemy_bullet(enemy_bulletx[i], enemy_bullety[i], i)
                if iscollision_player(playerx, playery, enemy_bulletx[i], enemy_bullety[i]):
                    itsover = True

            if enemy_bullety[i] >= 620:
                enemy_bullet_state[i] = "ready"

            # collision
            collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
            if collision:
                explossion_sound = mixer.Sound('explosion.wav')
                explossion_sound.play()
                bullety = 480
                bullet_state = "ready"
                score_value += 1
                if score_value % 40 == 0:
                    enemy_speed_x += 0.10
                    enemy_speed_y += 0.05
                enemyx[i] = random.randint(0, 736)
                enemyy[i] = random.randint(50, 150)

            enemy(enemyx[i], enemyy[i], i)

    else:
        game_over_text()

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_auto_state == "fire":
        if bullet_state == "ready":
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()
            bulletx = playerx
            bullet_state = "fire"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textx, texty)

    clock.tick(60)  # Limitar el framerate a 60 FPS
    pygame.display.update()