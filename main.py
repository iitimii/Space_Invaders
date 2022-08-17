import pygame as pyg
import random
import math
from pygame import mixer

#initialize pygame
pyg.init()
clock = pyg.time.Clock()

#create screen
screen = pyg.display.set_mode((800,600))
display = pyg.display

background = pyg.image.load('bg10.png') 

mixer.music.load('background.wav')
mixer.music.play(-1)

#caption and icon
display.set_caption('Space Invaders')
icon = pyg.image.load('ufo.png')
display.set_icon(icon)

#player
playerimg = pyg.image.load('spaceship.png')
playerX = 368
playerY = 480
dx = 0
dy = 0

enemyimg = []
enemyX = []
enemyY = []
ex = []
ey = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyimg.append(pyg.image.load('devil.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    ex.append(2)
    ey.append(40)



bulletimg = pyg.image.load('bullet.png')
bulletX = 0
bulletY = 480
bx = 0
by = 5
bullet_state = 'armed'

score = 0
font = pyg.font.Font('freesansbold.ttf',32)
textX= 10
textY = 10

overfont = pyg.font.Font('freesansbold.ttf',64)

def showscore(x,y,score):
    scor = font.render(f'Score: {score}', True, (255,255,255))
    screen.blit(scor, (x,y))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x+16, y+10))

def iScollision(enemyX, enemyY, bulletX, bulletY):
    dist =  math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    return True if dist < 30 else False

def game_over():
    gameover = overfont.render(f'GAME OVER', True, (255,255,255))
    screen.blit(gameover, (200,250))


#gameloop
running = True
while running:
    screen.fill((0, 0, 30))
    screen.blit(background, (0,0))

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_LEFT:  
                dx = -3
                print('left has been pressed')
            if event.key == pyg.K_RIGHT:     
                dx = 3
                print('right has been pressed')
            if event.key == pyg.K_SPACE:
                if bullet_state is 'armed':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pyg.KEYUP:
            if event.key == pyg.K_LEFT or event.key == pyg.K_RIGHT:
                dx = 0
                print('key released')

    playerX += dx

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    
    for i in range(no_of_enemies):
        if enemyY[i] > 200:
            for i in range(no_of_enemies):
                enemyY[i] = 2000
            dy = 0
            dx = 0
            by = 0 
            bx = 0
            playerX = 368
            playerY = 480 
            bulletX = 2000
            bulletY = 2000
            bullet_state = 'fire'
            game_over()
            break


        enemyX[i] += ex[i]

        if enemyX[i] <= 0:
            ex[i] = 2
            enemyY[i] += ey[i]
        elif enemyX[i] >= 736:
            ex[i] = -2
            enemyY[i] += ey[i]
        
        collision = iScollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            col_sound = mixer.Sound('explosion.wav')
            col_sound.play()
            bulletY = 480
            bullet_state = 'armed'
            score+=1
            
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY<=0:
        bulletY= 480
        bullet_state= 'armed'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY-=by


    player(playerX, playerY)
    
    showscore(textX, textY, score)

    display.update()
