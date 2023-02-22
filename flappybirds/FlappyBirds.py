import random
import time

import pygame, sys


def drawFloor():
    screen.blit(floorSurface, (floorXPos, 620))
    screen.blit(floorSurface, (floorXPos + 576, 620))


def createPipe():
    randomPipePos = random.choice(pipeHeight)
    bottomPipe = pipSurface.get_rect(midtop=(520, randomPipePos))
    topPipe = pipSurface.get_rect(midbottom=(520, randomPipePos - 190))

    return bottomPipe, topPipe


def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    # To delete the pipes which are out of the screen
    visiblePipes = [pipe for pipe in pipes if pipe.right > -50]
    return visiblePipes


def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 720:
            screen.blit(pipSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipSurface, False, True)
            screen.blit(flipPipe, pipe)


def checkCollisions(pipes):
    global increaseScore
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            deathSound.play()
            increaseScore = True
            return False
    if birdRect.top <= -50 or birdRect.bottom >= 620:
        increaseScore = True
        return False
    return True


def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird, -birdMovement * 3, 1)
    return newBird


def birdAnimation():
    newBird = birdFrames[birdIndex]
    newBirdRect = newBird.get_rect(center=(80, birdRect.centery))
    return newBird, newBirdRect


def scoreDisplay(gameState=""):
    scoreSueface = gameFont.render(f"Score: {int(score)}", True, (255, 255, 255))
    scoreRect = scoreSueface.get_rect(center=(240, 100))
    screen.blit(scoreSueface, scoreRect)
    if gameState == "GameOver":
        highScoreSueface = gameFont.render(f"HighScore: {int(highScore)}", True, (255, 255, 255))
        highScoreRect = highScoreSueface.get_rect(center=(240, 600))
        screen.blit(highScoreSueface, highScoreRect)

def updateScore(score, highScore):
    if score > highScore:
        highScore = score
    return highScore

def pipeScoreCheck():
    # To check if pipe in the position witch bird in
    global score, increaseScore
    if pipList:
        for pipe in pipList:
            if 78 < pipe.centerx < 82 and increaseScore:
                # This is triggered too often then whe use increase score
                score += 1
                scoreSound.play()
                increaseScore = False
            if pipe.centerx < 0:
                increaseScore = True

#pygame.mixer.pre_init(frequency=44100, size=32, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((480, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("FlappyBird!!")
gameFont = pygame.font.Font("freesansbold.ttf", 40)

# Game Variables
gravity = 0.15
birdMovement = 0
gameActive = True
score = 0
highScore = 0
increaseScore = True


bgSurface = pygame.image.load("assets\\background-day.png").convert()
bgSurface = pygame.transform.scale2x(bgSurface)

floorSurface = pygame.image.load("assets\\base.png").convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorXPos = 0

# Create animation from bird movement
birdDownFlap = pygame.image.load("assets\\bluebird-downflap.png").convert_alpha()
birdDownFlap = pygame.transform.scale2x(birdDownFlap)
birdMidFlap = pygame.image.load("assets\\bluebird-midflap.png").convert_alpha()
birdMidFlap = pygame.transform.scale2x(birdMidFlap)
birdUpFlaps = pygame.image.load("assets\\bluebird-upflap.png").convert_alpha()
birdUpFlaps = pygame.transform.scale2x(birdUpFlaps)
birdFrames = [birdDownFlap, birdMidFlap, birdUpFlaps]
birdIndex = 0
birdSurface = birdFrames[birdIndex]
birdRect = birdSurface.get_rect(center=(80, 320))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 150)

pipSurface = pygame.image.load("assets\\pipe-green.png").convert()
pipSurface = pygame.transform.scale2x(pipSurface)
pipList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipeHeight = [400, 300, 500, 250, 350]

gameOverSurface = pygame.image.load("assets\message.png").convert_alpha()
#gameOverSurface = pygame.transform.scale2x(gameOverSurface)
gameOverRect = gameOverSurface.get_rect(center=(240, 360))

flapSound = pygame.mixer.Sound("sound/sfx_wing.wav")
deathSound = pygame.mixer.Sound("sound/sfx_hit.wav")
scoreSound = pygame.mixer.Sound("sound/sfx_point.wav")

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                birdMovement = 0
                birdMovement -= 5
                flapSound.play()
            # Restart the game
            if event.key == pygame.K_r and (not gameActive):
                gameActive = True
                pipList.clear()
                birdRect.center = (80, 320)
                birdMovement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pygame.time.set_timer(SPAWNPIPE, random.randint(1000, 2200))
            pipList.extend(createPipe())

        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0
            birdSurface, birdRect = birdAnimation()
    screen.blit(bgSurface, (0, -250))
    if gameActive:
        # Bird
        birdMovement += gravity
        rotatedBird = rotateBird(birdSurface)
        birdRect.centery += birdMovement
        screen.blit(rotatedBird, birdRect)
        gameActive = checkCollisions(pipList)

        # Pipes
        pipList = movePipes(pipList)
        drawPipes(pipList)

        # Show Score
        pipeScoreCheck()
        scoreDisplay()
    else:
        screen.blit(gameOverSurface, gameOverRect)
        highScore = updateScore(score, highScore)
        scoreDisplay("GameOver")

    # Floor
    floorXPos -= 1
    drawFloor()
    if floorXPos <= -576:
        floorXPos = 0

    pygame.display.update()
    clock.tick(120)
