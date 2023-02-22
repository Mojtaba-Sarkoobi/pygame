import pygame, sys
import random

def ballAnimation():
    global ballSpeedX, ballSpeedY, playerScore, opponentScore, scoreTime

    ball.x += ballSpeedX
    ball.y += ballSpeedY

    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballSpeedY *= -1

    if ball.left <= 0:
        playerScore += 1
        scoreTime = pygame.time.get_ticks()

    if ball.right >= screenWidth:
        opponentScore += 1
        scoreTime = pygame.time.get_ticks()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ballSpeedX *= -1

def playerAnimation():
    player.y += playerSpeed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screenHeight:
        player.bottom = screenHeight

def opponentAnimation():
    opponent.y += opponentSpeed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screenHeight:
        opponent.bottom = screenHeight

def ballStart():
    global ballSpeedX, ballSpeedY, scoreTime

    currentTime = pygame.time.get_ticks()
    ball.center = (screenWidth / 2, screenHeight / 2)

    if currentTime - scoreTime < 2100:
        ballSpeedX, ballSpeedY = 0, 0
    else:
        ballSpeedY = 5 * random.choice((1, -1))
        ballSpeedX = 5 * random.choice((1, -1))
        scoreTime = None
# General Setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Pong")

# Game Rectangles
ball = pygame.Rect(screenWidth/2 - 15, screenHeight/2 - 15,30, 30)
player = pygame.Rect(screenWidth - 20, screenHeight/2 - 70, 10, 140)
opponent = pygame.Rect(10, screenHeight/2 - 70, 10, 140)

bgColor = pygame.Color("grey12")
lightGrey = (200, 200, 200)

ballSpeedX = 5 * random.choice((1, -1))
ballSpeedY = 5 * random.choice((1, -1))
playerSpeed = 0
opponentSpeed = 0

# Text variables
playerScore = 0
opponentScore = 0
gameFont = pygame.font.Font("freesansbold.ttf", 32)

# Score Timer
scoreTime = None


while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerSpeed += 7
            if event.key == pygame.K_UP:
                playerSpeed -= 7
            if event.key == pygame.K_w:
                opponentSpeed -= 7
            if event.key == pygame.K_s:
                opponentSpeed += 7
        if event.type == pygame.KEYUP:
            playerSpeed = 0
            opponentSpeed = 0
    ballAnimation()
    playerAnimation()
    opponentAnimation()

    #visuals
    screen.fill(bgColor)
    pygame.draw.rect(screen, lightGrey, player)
    pygame.draw.rect(screen, lightGrey, opponent)
    pygame.draw.ellipse(screen, lightGrey, ball)
    pygame.draw.aaline(screen, lightGrey, (screenWidth/2, 0), (screenWidth/2, screenHeight))

    if scoreTime:
        ballStart()

    playerText = gameFont.render(f"{playerScore}", False, lightGrey)
    screen.blit(playerText, (660, 360))

    opponentText = gameFont.render(f"{opponentScore}", False, lightGrey)
    screen.blit(opponentText, (600, 360))


    # Updating the window
    pygame.display.flip()
    clock.tick(60)