import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the sccreen
sceen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("myImage\\freepik.jpg")

# Background Sound
mixer.music.load("sounds\\background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load("myImage\\flaticon.png")
pygame.display.set_icon(icon)



# Player
playerImg = pygame.image.load("myImage\\space-invaders.png")
playerX = 360
playerY = 480

playerXChange = 0

# Enemy
enemyImg = pygame.image.load("myImage\\extraterrestrial.png")
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(0.4)
    enemyYChange.append(40)

#
# Ready = You can't see the bullet on the screen
# fire = The bullet is currently moving
bulletImg = pygame.image.load("myImage\\bullet.png")
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = .7
bulletState = "ready"

# Font
scoreValue = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# Game Over Text
gameOverFont = pygame.font.Font("freesansbold.ttf", 64)

def showScore(x, y):
     score = font.render("Score : " + str(scoreValue), True, (255, 255, 255))
     sceen.blit(score, (x, y))

def gameOverText():
    gameOverText = gameOverFont.render("Game Over", True, (255, 255, 255))
    sceen.blit(gameOverText, (200, 250))

def player(x, y):
    #Drawing the image on game window
    sceen.blit(playerImg, (x, y))

def enemy(x, y):
    sceen.blit(enemyImg, (x, y))

def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    sceen.blit(bulletImg, (x + 16, y + 10))

def isColision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((pow(enemyX - bulletX, 2)) + (pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # RGB = red, green, Blue
    sceen.fill((0, 0, 0))

    # Background image
    sceen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerXChange = -0.4
            if event.key == pygame.K_d:
                playerXChange = 0.4
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletSound = mixer.Sound("sounds\\laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                playerXChange = 0

    # checking for boundaries of player
    # it doesn't go out of bounds
    playerX += playerXChange

    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(numOfEnemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            else:
                gameOverText()
                break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] <= 0:
            enemyXChange[i] = 0.4
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= 736:
            enemyXChange[i] = - 0.4
            enemyY[i] += enemyYChange[i]

        # Collision
        collision = isColision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("sounds\\explosion.wav")
            explosionSound.play()
            bulletY = 480
            bulletState = "ready"
            scoreValue += 1
            print(scoreValue)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i])

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"

    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
